---
layout: post
title: "More Functional Context Free Grammar Parsing"
summary: "Functional programming improvements to parsing of context free grammars."
date:   2026-05-01 08:03:00 -0700
---

# A Functional Stack

In the [last
version](https://github.com/mspandit/rust-binary-tree-generator/tree/2026-04-14)
of our context free grammar parser, we represented the stack as a `Vec`. This is
not well-aligned with functional programming principles, especially considering
the `push` and `pop` methods perform in-place modifications (mutations) of the
`Vec`.

In the spirit of treating functions as "first-class citizens," we replace the
`Vec` with an `Option` of a function. The idea is that the stack is either empty
(represented by `None`) or a function that requires no arguments but returns an
element of type `S` and the stack "below" it.

```rust
struct Stack<S>(Option<Rc<dyn Fn() -> (S, Self)>>);
```

`top` and `pop` methods are no longer useful on this representation. They are
meaningless on an empty stack, and calling the function of a non-empty stack
effectively returns the top element and the popped stack&mdash;without mutating
the original stack.

One consequence of this is that the `tops` and `filter_stacks` functions become
slightly more complicated:
```rust
    pub fn tops(self: Self) -> Vec<BinaryTree<T>> {
        self.0.into_iter().flat_map(|stack| stack.0.map_or(
            Vec::default(), // Empty stack --> return empty vector
            // Non-empty stack --> return vector with element
            |ref f| vec![f().0]
        ))
        .collect()
    }

    pub fn filter_stacks(self: Self) -> Self {
        Self(
            self.0.into_iter().filter(|stack| match stack.0 {
                None => false, // Filter out empty stacks
                Some(ref f) => match f() {
                    (_, Stack(None)) => true,
                    // Filter out stacks with more than one element
                    (_, Stack(Some(_))) => false
                }
            })
            .collect()
        )
    }
```

The `push` method on a stack creates a closure that returns the pushed element
and the current stack when called.
```rust
    fn push(self: Self, element: BinaryTree<T>) -> Self {
        Stack(
            Some(Rc::new(
                move || (element.clone(), self.clone())
            ))
        )
    }
```

# Shift/Reduce with Functional Stack

`shift_reduce` establishes an accumulator for the new stacks and then calls
`shift_reduce0`, a recursive function.

```rust
    fn shift_reduce0(
        self: Self,
        tree: BinaryTree<T>,
        grammar: &Grammar<T>,
        mut acc: Vec<Self>) -> Vec<Self> {
        self.0.map_or(
            acc.clone(), // Empty stack --> return accumulated stacks
            |ref f| {
                let (popped, rest) = f();
                grammar
                .lookup_nonterminals(&(popped.label(), tree.label()))
                .map_or(
                    // No matching nonterminals --> return accumulated stacks
                    acc.clone(),
                    |new_nonterminal_labels| {
                        new_nonterminal_labels.iter()
                        .flat_map(|new_nonterminal_label| {
                            let new_nonterminal = BinaryTree::Nonterminal {
                                label: new_nonterminal_label.clone(),
                                left: Box::new(popped.clone()),
                                right: Box::new(tree.clone())
                            };
                            acc.push(
                                rest
                                .clone()
                                .push(new_nonterminal.clone())
                            );
                            rest.clone().shift_reduce0(
                                new_nonterminal,
                                grammar,
                                acc.clone()
                            )
                        })
                        .collect()
                    }
                )
            }
        )
    }

    pub fn shift_reduce(self: Self, tree: BinaryTree<T>, grammar: &Grammar<T>)
    -> Vec<Self> {
        self
        .clone()
        .shift_reduce0(tree.clone(), grammar, vec![self.push(tree)])
    }
```

We used the `fold` method in three places.

1. In `shift_reduce`, we folded nonterminal labels looked up from the grammar
   into a list of stacks.
2. In `process_fn` we folded terminal labels looked up from the grammar into a
   list of stacks.
3. In `process` we folded the stacks of the current state into a new state.

It turns out that all three of these functions are actually instances of
_[bind](https://en.wikipedia.org/wiki/Monad_(functional_programming))._ Bind
takes a function that transforms a type into a composite type (in our case a
`String` label into a `Vec<Stack>` or a `Stack` into a `Vec<Stack>`) and applies
it to a composite type (in our case, a `Vec<String>` or
a&mdash;smaller&mdash;`Vec<Stack>`).

To make this explicit, we replace `fold` with `flat_map` in the other two cases:

```rust
    pub fn process(self: Self, token: T, grammar: &Grammar<T>) -> Self {
        Self(
            self.0.iter().flat_map(|current_stack| {
                grammar.lookup_terminals(& token).map_or(
                    Vec::default(),
                    |t_labels| {
                        t_labels.iter().flat_map(|terminal_label| {
                            current_stack.clone()
                                .shift_reduce(
                                    BinaryTree::Terminal {
                                        label: terminal_label.clone(),
                                        token: token.clone()
                                    },
                                    grammar
                                )
                        }).collect()
                    }
                )
            }).collect()
        )
    }
```

The latest version of the code, incorporating the above changes, is [here](https://github.com/mspandit/rust-binary-tree-generator/tree/2026-05-01).