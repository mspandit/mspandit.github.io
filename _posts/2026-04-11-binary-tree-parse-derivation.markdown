---
layout: post
title: "From Binary Trees to Grammar Derivations"
summary: "From binary tree generator to parse derivation generator."
date:   2026-04-11 09:46:00 -0700
---

# Déjà Vu

If you have studied [natural language
processing](https://en.wikipedia.org/wiki/Natural_language_processing#Syntactic_analysis)
(NLP) then [generation of binary
trees](/2026/04/11/generating-binary-trees.html) might have given you a feeling
of déjà vu. Here's why:

NLP often involves using a [context-free
grammar](https://en.wikipedia.org/wiki/Context-free_grammar) (CFG) to decompose
a sentence. We use the rules ("productions") of the grammar to generate a [parse
tree](https://en.wikipedia.org/wiki/Parse_tree), also called a _derivation_. In
general, CFGs are non-deterministic or ambiguous, meaning multiple derivations
can be produced. (It is certainly for a CFG to be
[deterministic](https://en.wikipedia.org/wiki/Deterministic_context-free_grammar),
in which case a single derivation can be produced&mdash;computer programming
languages, unlike natural languages, conform to a deterministic CFG.)

[Shift-reduce parsing](https://en.wikipedia.org/wiki/Shift-reduce_parser) is a
flexible method for generating derivations of a CFG from an input text. Remember
the choices in the generation of binary trees: "lazy" to put something on the
stack, and "eager" to create new non-terminals and put them on copies of the
stack. The "lazy choice" directly corresponds to the "shift" step of a
shift-reduce parser. The "eager" choice corresponds to the "reduce" step.

In the latest version of the Rust code, I've replaced use of the term `eager`
with `reduce`, and use of the term `lazy` with `shift`.

# From Characters to Tokens

The code currently generates binary trees from sequences of _characters._ In
NLP, derivations of CFGs are usually generated from sequences of _words._ We'd
like to accommodate these possibilities&mdash;and more.

For example, we might expect a speech recognition system to produce a sequence
of words from an audio signal. However, there can be uncertainty about which
word was uttered, because different words can sound similar, especially in the
presence of background noise. Therefore, the speech recognition system is likely
to produce a sequence of _probability distributions over words._

For this reason, I've modified the code to treat the input as a sequence of
_tokens._ In Rust, we can allow tokens to be of non-character types using
[generics](https://doc.rust-lang.org/rust-by-example/generics.html). However, we
do need to display and clone tokens. Therefore, we introduce the `Token` trait.
This trait itself does not require implementation of any methods, but it refers
to types that implement the required `Clone` and `Display` methods:
```rust
trait Token: Clone + Display {}
```

The terminals of the binary tree will now consist of tokens, any type that
implements the `Token` trait:
```rust
enum BinaryTree<T: Token> {
    Terminal(T),
    Nonterminal(Box<BinaryTree<T>>, Box<BinaryTree<T>>),
}
```
One way to interpret this is: the Rust compiler will generate, on the fly,
versions of the `BinaryTree` storing different types of terminals, as long as
those types implement the `Token` trait. (We say they "are `Token`.") It will
also generate versions of any methods on `BinaryTree` that depend on what is
stored.

The built-in `char` and `str` types already implement `Display` and `Clone`. We
still need to "mark" them as implementing `Token` with a single line each:

```rust
impl Token for char {}
impl Token for &str {}
```

`generate_stacks` was calling the `chars` method, but that method is only
suitable for character sequences. We replace its argument with any sequence that
implements an iterator over `Token` types. We generalize the argument of
`generate` similarly:
```rust
fn generate_stacks<T: Token>(input_sequence: impl Iterator<Item = T>)
-> Vec<Stack<T>> {
    input_sequence.fold(
        vec![Stack::default()],
        |stacks, input| {
            stacks.into_iter().fold(
                Vec::default(),
                shift_reduce_fn(input)
            )
        }
    )
}

fn generate<T: Token>(input_sequence: impl Iterator<Item = T>)
-> Vec<BinaryTree<T>> {
    tops(filter_stacks(generate_stacks(input_sequence)))
}
```
In `main`, we test this capability by passing sequences of characters as well as
words:
```rust
fn main() {
    let x = generate("abcde".chars());
    println!("{} trees", x.len());
    for t in x {
        println!("{}", t);
    }
    let word_sequence = vec!["the", "cat", "sat", "on", "the", "mat"];
    let x = generate(word_sequence.into_iter());
    println!("{} trees", x.len());
    for t in x {
        println!("{}", t);
    }
}
```

[This
version](https://github.com/mspandit/rust-binary-tree-generator/releases/tag/2026-04-11a)
successfully generates 42 trees for the sequence of words!
