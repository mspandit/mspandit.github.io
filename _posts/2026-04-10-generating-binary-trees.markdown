---
layout: post
title: "Generating Binary Trees"
summary: "How would you generate all possible binary trees from a sequence of inputs?"
date:   2026-04-10 19:43:00 -0700
---

How would you generate all possible binary trees from a sequence of inputs?

## Trees and Binary Trees

First, what even is a binary tree? In computer science, a tree data structure
models "one-to-many" relationships. For example, a mother can have multiple
children, but a child can have only one (biological) mother. The branch of an
actual tree might have many leaves, but any leaf is connected to a single
branch. Abstractly, some "nodes" in a tree are "parents" or "branches" to other
nodes, their "children" (which can themselves be "parents" or "branches").
Eventually, there are "children" with no children of their own, the "leaves" of
the tree.

In a binary tree, a parent has exactly two children. Binary trees are
interesting because they are recursively defined, but still very simple. A tree
in which parents might have more than two children (an "$$n$$-ary tree") can
always be converted into a binary tree by introducing "intermediate" or "latent"
parents. This is related to the fact that context-free grammars can always be
converted to [Chomsky normal
form](https://en.wikipedia.org/wiki/Chomsky_normal_form). For this reason, I'll
be referring to "branch" nodes as "nonterminal" and "leaf" nodes as "terminal."

Tree data structures are valuable for modeling component-part relationships.
Therefore, when we generate "all possible binary trees from a sequence of
inputs," we are generating "all possible _decompositions_ of a sequence of
inputs."

## Generating Trees

This is a non-trivial task. There are
[solutions](https://leetcode.com/problems/all-possible-full-binary-trees/description/)
for a sequence of a given length. But I am more interested in an _incremental_
solution where you don't know the length of the sequence in advance. Let's
consider various cases:

* For an empty sequence of inputs, no binary trees are possible.
* For the first input, for example `a`, a tree consisting of a terminal is
  possible. I'll simply write this tree as `a`.
* For the second input, for example `b`, a tree consisting of a nonterminal,
  with the two inputs as its children, is possible. I'll write this tree as `(a
  b)` The parentheses signal the presence of a nonterminal with the children
  between them.

For more than two inputs, things get complicated.

* For a sequence of three inputs, two trees are possible: `(a (b c))` and `((a b) c)`
* For a sequence of four inputs, five trees are possible: `(a (b (c
  d)))`, `((a (b c)) d)`, `(a ((b c) d))`, `((a b) (c d))`, and `(((a b) c ) d)`

You can see that the idea is to "connect" an input to, or "pair" an input with
its prior (left) or subsequent (right) neighbor at different times during the
construction of the neighbor. In the most "eager" case, we pair every input with
its left neighbor immediately and get a tree like `(((a b) c) d)`. In the most
"lazy" case, we pair every input with its right neighbor, if there is one. _This
means we must wait to do any connections until the last input is read._ This
gives us a tree like `(a (b (c d)))`.

Every time we get an input, there is a choice of being eager or lazy. A
different sequence of choices will result in a different tree, so all possible
sequences must be generated. This means that for intermediate inputs, we need to
"split" the state of the tree generation to represent both choices.

## An Algorithmic Approach

A [_stack_](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) is a
suitable data structure in which to store a sequence of choices. Our approach
will be to create multiple stacks representing different sequences of choices in
tree generation:

* We will start with a single empty stack
* For the first input, we will create a terminal and put it on top of the stack
  for later use. This represents the choice to be lazy. (There is no possibility
  to be eager with the first input because there is no prior input to pair
  with.)
* For any subsequent input, we will create a terminal for the input and a copy
  of the stack. The original ("lazy stack") will represent the choice to be lazy
  for this input. The copy ("eager stack") will represent the choice to be
  eager.
    1. We will put the new terminal on top of the lazy stack.
    2. We will pop a prior tree off the top of the eager stack, and create a
       nonterminal combining the tree and the new terminal
    3. With this new nonterminal, too, there is a choice to be eager or lazy.
       So we will create a copy of the _popped_ stack. The original will represent
       the choice to be lazy. The copy will represent the choice to be eager, so
       we will do the above _iteratively_ until we cannot pop any more trees off the stack.
* For the second input, we will end up with two stacks. For additional inputs,
  we will do the above for _all the stacks._

Once the last input is processed as described above, there will be a large
number of stacks:

* Some will have multiple trees stacked on them. These were created in
  anticipation of additional input that would pair the trees. These stacks can
  be filtered out.
* The remainder will have a single binary tree on top,
  representing a different sequence of decisions. These will be the possible
  binary trees on the input.

This process is illustrated below for four inputs. Commas separate trees on a
stack. Grey lines trace which stacks are copies of which other stacks.

<img src="/images/2026-04-09-generating-binary-trees.JPG" />

## Implementation in Rust

We can try to represent a binary tree data structure corresponding to characters
in Rust as follows:

```rust
enum BinaryTree {
    Terminal(char),
    Nonterminal(BinaryTree, BinaryTree)
}
```

Unfortunately, this causes the compiler error `recursive type BinaryTree has
infinite size`.

The reason is that when a function creates a local variable of type
`BinaryTree`, Rust needs to know its size at compilation time so it can be put
on the stack.

The compiler suggests storing _references_ to other binary trees, because the
size of any reference _is_ known at compilation time:

```rust
enum BinaryTree {
    Terminal(char),
    Nonterminal(Box<BinaryTree>, Box<BinaryTree>),
}
```

At the top level, we have a function that borrows a string (because it won't
need to modify it), generates stacks, filters them, and returns the top of the
remaining stacks.
```rust
fn generate(input_sequence: &str) -> Vec<BinaryTree> {
    tops(filter_stacks(generate_stacks(input_sequence)))
}
```

Stacks are represented using Rust's standard
[`Vec`](https://doc.rust-lang.org/std/vec/struct.Vec.html) type, which supports
[`push`](https://doc.rust-lang.org/std/vec/struct.Vec.html#method.push) and
[`pop`](https://doc.rust-lang.org/std/vec/struct.Vec.html#method.pop) operations
as you would expect a stack to support:
```rust
struct Stack(Vec<BinaryTree>);
```

The `generate_stacks` function uses the
[`chars`](https://doc.rust-lang.org/std/primitive.str.html#method.chars) method
to acquire a [character
iterator](https://doc.rust-lang.org/std/str/struct.Chars.html#impl-Iterator-for-Chars%3C'a%3E)
on the input string.
[`Iterator`](https://doc.rust-lang.org/std/iter/trait.Iterator.html) types have
a powerful method,
[`fold`](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.fold).
The idea of `fold` is to "fold" all elements of the iterator into some result,
which can be of any type. `fold` takes two arguments:

* an initial value for the result (which would be returned if the iterator was
  empty)
* a closure or function. This must accept two arguments: the current value for
  the result, and the next element from the iterator. It must return an updated
  value for the result.

(A similar method,
[`reduce`](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.reduce),
is more restrictive. You need not provide an initial value, because it uses the
first element as the initial value. However, because the iterator might be
empty, `reduce` returns an
[`Option`](https://doc.rust-lang.org/std/option/enum.Option.html) of the same
type as the iterator.)

By using `fold` wherever possible, you will find that your code becomes more
comprehensible, better organized, and more amenable to parallel processing.

In the case of `generate_stacks`, the result to generate is a list of
stacks.

The closure, in turn, acquires an iterator on the current list of stacks and
`fold`s it into a new list of stacks. The function used in this `fold` is
generated at run-time by a higher-order function `lazy_eager_fn` which takes the
current character as input.

```rust
fn generate_stacks(input_sequence: & str) -> Vec<Stack> {
    input_sequence.chars().fold(
        vec![Stack::default()],
        |stacks, input| {
            stacks.into_iter().fold(
                Vec::default(),
                lazy_eager_fn(input)
            )
        }
    )
}
```
`lazy_eager_fn` returns a function that takes the list of stacks being generated
and one of the prior stacks generated from the previous input. Based on the
"eager" choice, multiple stacks may be added to the list, so the work of
generating them is delegated to `eager`. Based on the "lazy" choice from the
prior stack, a new stack is added to the list with a terminal containing the
current input.

```rust
fn lazy_eager_fn(current: char) -> impl Fn(Vec<Stack>, Stack)
-> Vec<Stack> {
    move |mut new_stacks, mut stack| {
        // eager may produce multiple stacks
        new_stacks.append(& mut eager(stack.clone(), current));
        // lazy
        stack.0.push(BinaryTree::Terminal(current));
        new_stacks.push(stack); // transfer ownership
        new_stacks
    }
}
```

Recall that `eager` must pop trees off the stack iteratively. For this reason,
we define a new method on a `Stack` called `popping_iter` which consumes (takes
ownership of) the stack and returns an `PoppingIterator` for it. The
`PoppingIterator` implements the `Iterator` trait. Each of its elements is a
tuple consisting of a stack element and a copy of the stack that element was
just popped off.

```rust
struct PoppingIterator(Stack);

impl Iterator for PoppingIterator {
    type Item = (BinaryTree, Stack);

    fn next(&mut self) -> Option<Self::Item> {
        self.0.0.pop().and_then(|tree| Some((
            tree, // The tree that was just popped off the stack
            self.0.clone(), // Copy of the stack after pop
        )))
    }
}

impl Stack {
    fn popping_iter(self: Self) -> PoppingIterator {
        PoppingIterator(self)
    }
}
```

The tuples returned by the `PoppingIterator` can now be `fold`ed into a new list
of stacks. However, a nonterminal must also be updated in every iteration. So
`eager` starts with an initial tuple consisting of an empty list of stacks, and
a terminal for the current input. In every iteration, the list of stacks
(initially empty) is updated and the binary tree (initially a terminal for the
current input) gets updated.

You can see that for the first input, the `PoppingIterator` immediately returns
`None` because the stack is empty. `eager` returns an empty list of stacks. It
is as if `lazy_eager_fn` only created a lazy version of the stack, which is the
behavior we want.

```rust
fn eager0(new: (Vec<Stack>, BinaryTree), popped: (BinaryTree, Stack))
-> (Vec<Stack>, BinaryTree) {
    let mut new_stacks = new.0;
    let new_tree = new.1;
    let tree = popped.0;
    let stack = popped.1;
    let new_nonterminal = BinaryTree::Nonterminal(
        Box::new(tree),
        Box::new(new_tree),
    );
    let mut new_stack = stack;
    new_stack.0.push(new_nonterminal.clone());
    new_stacks.push(new_stack);
    (new_stacks, new_nonterminal)
}

fn eager(stack: Stack, current: char) -> Vec<Stack> {
    stack.popping_iter().fold(
        (Vec::default(), BinaryTree::Terminal(current)),
        eager0
    ).0
}
```

Once stacks have been generated for all of the inputs, `filter_stacks` returns the ones with a single element:
```rust
fn filter_stacks(stacks: Vec<Stack>) -> Vec<Stack> {
    stacks.into_iter()
        .filter(|stack| 1 == stack.0.len())
        .collect()
}
```
`tops` returns the binary trees on the top of those stacks:
```rust
fn tops(stacks: Vec<Stack>) -> Vec<BinaryTree> {
    stacks.iter()
        .map(|stack| stack.0[0].clone())
        .collect()
}
```

Once trees are generated, they can be printed out by implementing the `Display` trait for `BinaryTree`. The `main` function prints out the 14 trees for the sequence `abcde`.

```rust
impl Display for BinaryTree {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            BinaryTree::Terminal(c) => write!(f, "{c}"),
            BinaryTree::Nonterminal(left, right) =>
                write!(f, "({left} {right})"),
        }
    }
}

fn main() {
    let x = generate("abcde");
    println!("{} trees", x.len());
    for t in x {
        println!("{}", t);
    }
}
```

```
14 trees
((((a b) c) d) e)
(((a b) c) (d e))
((a b) ((c d) e))
(((a b) (c d)) e)
((a b) (c (d e)))
(a (((b c) d) e))
((a ((b c) d)) e)
(a ((b c) (d e)))
(((a (b c)) d) e)
((a (b c)) (d e))
(a (b ((c d) e)))
(a ((b (c d)) e))
((a (b (c d))) e)
(a (b (c (d e))))
```

The repository containing the full code is [here](https://github.com/mspandit/rust-binary-tree-generator).