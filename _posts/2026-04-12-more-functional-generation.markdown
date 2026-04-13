---
layout: post
title: "More Functional Binary Tree Generation"
summary: "Functional programming improvements to binary tree generation."
date:   2026-04-13 08:40:00 -0700
---

# Generator State
In the [last version](/2026/04/11/binary-tree-parse-derivation.html) of our
binary tree generator, `generate_stacks` was iterating over the input sequence,
and updating a `Vec<Stack>` in every iteration. This `Vec<Stack>` represents the
_state_ of the generator. To make our code more functional, we represent this
state using its own type, and provide a default state consisting of a single
empty stack:
```rust
pub struct GeneratorState<T: Token>(Vec<Stack<T>>);

impl<T: Token> Default for GeneratorState<T> {
    fn default() -> Self {
        Self(vec![Stack::default()])
    }
}
```

The state has a method to `process` a `Token` to produce a new state.

This method calls the higher-order `process_fn` to create a new function
`stack_fn` to process stacks with the token. `process` starts with a default (empty)
`Vec<Stack>`, and iterates over the stacks in the current state. At each
iteration, it calls `stack_fn` which produces one or more new stacks. The set of
new stacks produced from all of the current stacks forms the new state.

```rust
    pub fn process(self: Self, token: T) -> Self {
        let stack_fn = process_fn(token);
        Self(
            self.0.into_iter().fold(
                Vec::default(),
                stack_fn
            )
        )
    }
```

The function returned by `process_fn` creates a new `BinaryTree::Terminal` from
the token and passes it to `shift_reduce` on the current stack. The stacks
returned by `shift_reduce` are appended to the set of new stacks.

```rust
fn process_fn<T: Token>(token: T) -> impl Fn(Vec<Stack<T>>, Stack<T>) -> Vec<Stack<T>> {
    move |mut new_stacks, current_stack| {
        new_stacks.append(& mut current_stack
            .shift_reduce(BinaryTree::Terminal(token.clone()))
        );
        new_stacks
    }
}
```

`shift_reduce` replaces `PoppingIterator` with recursion over the stack. It
accepts a new tree which, when initially called, is the `Terminal` for the new
token.

It attempts to pop a tree off the stack. If there was none, then it pushes the
new tree on the stack and returns a `Vec` containing only itself. This is all
that happens for the first input token in the sequence.

If there was a tree on the stack, the method must put the stack representing the
lazy (shift) choice and one or more stacks representing eager (reduce) choices
in the new state.

The shift choice restores the tree that was popped and also pushes the new tree
on the stack, and adds it to the new stacks for the new state.

The reduce choice creates a new nonterminal containing the tree that was popped
and the new tree. It then recursively calls `shift_reduce`, passing the new
nonterminal.

```rust
    pub fn shift_reduce(mut self: Self, tree: BinaryTree<T>)
    -> Vec<Self> {
        match self.pop() {
            None => {
                self.push(tree); // shift only
                vec![self]
            },
            Some(popped_tree) => {
                let r = self.clone(); // for recursion later
                // restore the popped tree
                self.push(popped_tree.clone());
                self.push(tree.clone()); // shift
                let mut new_stacks = vec![self.clone()];

                let new_nonterminal = BinaryTree::Nonterminal(
                    Box::new(popped_tree),
                    Box::new(tree),
                );
                new_stacks.append(&mut r
                    .shift_reduce(new_nonterminal)
                ); // reduce
                new_stacks
            }
        }
    }
```

Finally, we make `filter_stacks` and `tops` into methods on `GeneratorState`

```rust
    pub fn tops(self: Self) -> Vec<BinaryTree<T>> {
        self.0.into_iter().map(|stack| stack.top()).collect()
    }

    pub fn filter_stacks(self: Self) -> Self {
        Self(
            self.0.into_iter()
                .filter(|stack| 1 == stack.len())
                .collect()
        )
    }
```

`generate_stacks` was calling the `chars` method, but that method is only
suitable for character sequences. We replace its argument with any sequence that
implements an iterator over `Token` types. Starting with the default
`GeneratorState`, it folds the input sequence into new states iteratively by
calling the `process` method.

```rust
fn generate_stacks<T: Token>(input_sequence: impl Iterator<Item = T>)
-> GeneratorState<T> {
    input_sequence.fold(
        GeneratorState::default(),
        |gen_state, input| {
            gen_state.process(input)
        }
    )
}
```
We generalize the argument of
`generate` similarly, and use the new methods on the `GeneratorState`:
```rust
fn generate<T: Token>(input_sequence: impl Iterator<Item = T>)
-> Vec<BinaryTree<T>> {
    generate_stacks(input_sequence)
        .filter_stacks()
        .tops()
}
```

[These
changes](https://github.com/mspandit/rust-binary-tree-generator/releases/tag/2026-04-13)
make the design more functional without altering the operation of the program.
