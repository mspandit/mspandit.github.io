---
layout: post
title: "Context Free Grammar Parsing"
summary: "From binary tree generation to parsing of context free grammars."
date:   2026-04-14 14:14:00 -0700
---


The binary tree generator operates similarly to [a shift-reduce
parser](/2026/04/11/binary-tree-parse-derivation.html), but right now, there is
no grammar to use in parsing!

Starting with a `GeneratorState` consisting of an empty stack, the code performs
shift and reduce steps for every input token. The result is all possible binary
trees over&mdash;all possible decompositions of&mdash;the input sequence.

A context-free grammar consists of [productions, or
rules](https://en.wikipedia.org/wiki/Production_(computer_science)). The
left-hand side (LHS) of each production is a _nonterminal_ symbol. For a grammar
in Chomsky Normal Form, the right-hand side (RHS) is a pair of _terminal or
nonterminal_ symbols. (Terminal symbols are simply those that never occur on the
LHS of a production.)

In a shift-reduce parser, those rules control whether the shift and reduce steps
happen.

To parse using a CFG, I'll modify the code to "check with" a grammar before
shifting or reducing. If the input token corresponds to a terminal
grammar symbol, it can be pushed on to the stack. If the two items on the top
of the stack correspond to symbols on the RHS of a production, then the
nonterminal on the LHS of the production can be pushed on to the stack.

## Binary Tree Modifications

The first modification will be to store labels (grammar symbols) in our
`BinaryTree`:
```rust
pub enum BinaryTree<T: Token> {
    Terminal { label: String, token: T },
    Nonterminal {
        label: String,
        left: Box<BinaryTree<T>>,
        right: Box<BinaryTree<T>>
    },
}
```

Next, we'll add a `label` method on `BinaryTree` to retrieve the label:
```rust
    pub fn label(&self) -> String {
        match self {
            BinaryTree::Terminal { label, .. } => label.clone(),
            BinaryTree::Nonterminal { label, .. } => label.clone(),
        }
    }
```

## Grammar Representation

The grammar will store rules mapping tokens to terminal symbols as "unigrams,"
and rules mapping pairs of symbols to nonterminal symbols as "digrams."

Note that in a grammar, tokens can correspond to _multiple_ terminal symbols,
and pairs of symbols can correspond to multiple nonterminal symbols. These
represent "alternative interpretations" of the input sequence. Therefore, the
mapping is to `Vec<String>` not `String`.
```rust
pub struct Grammar<T: Token> {
    unigrams: HashMap<T, Vec<String>>, // token -> terminal label
    // (left_label, right_label) -> nonterminal label
    digrams: HashMap<(String, String), Vec<String>>,
}
```

I've added a couple of elementary grammars to demonstrate the parser. One is a
simplified version of an expression grammar from Unit 1 of Bill MacCartney's
[SippyCup project](https://github.com/wcmac/sippycup). (This project has been a
source of great inspiration for me!) This grammar parses expressions consisting
of the characters 1, 2, 3, 4, -, +, and *. It allows - to be used as a unary
operator for negation, or a binary operator for subtraction:

```rust
    pub fn expression() -> Self {
        let mut unigrams = HashMap::default();
        unigrams.insert('1', vec!["E".to_string()]);
        unigrams.insert('2', vec!["E".to_string()]);
        unigrams.insert('3', vec!["E".to_string()]);
        unigrams.insert('4', vec!["E".to_string()]);
        unigrams.insert('-', vec![
            "UnOp".to_string(),
            "BinOp".to_string()
        ]);
        unigrams.insert('+', vec!["BinOp".to_string()]);
        unigrams.insert('*', vec!["BinOp".to_string()]);
        let mut digrams = HashMap::default();
        digrams.insert(("UnOp".to_string(), "E".to_string()), vec![
            "E".to_string()
        ]);
        digrams.insert(("E".to_string(), "BinOp".to_string()), vec![
            "EBO".to_string()
        ]);
        digrams.insert(("EBO".to_string(), "E".to_string()), vec![
            "E".to_string()
        ]);
        Self { unigrams, digrams }
    }
```

The other is an elementary natural language grammar:

```rust
    pub fn sentence() -> Self {
        let mut unigrams = HashMap::default();
        unigrams.insert("the", vec!["Det".to_string()]);
        unigrams.insert("cat", vec!["N".to_string()]);
        unigrams.insert("sat", vec!["V".to_string()]);
        unigrams.insert("on", vec!["P".to_string()]);
        unigrams.insert("mat", vec!["N".to_string()]);
        let mut digrams = HashMap::default();
        digrams.insert(("Det".to_string(), "N".to_string()), vec![
            "NP".to_string()
        ]);
        digrams.insert(("V".to_string(), "NP".to_string()), vec![
            "VP".to_string()
        ]);
        digrams.insert(("P".to_string(), "NP".to_string()), vec![
            "PP".to_string()
        ]);
        digrams.insert(("V".to_string(), "PP".to_string()), vec![
            "VP".to_string()
        ]);
        digrams.insert(("NP".to_string(), "VP".to_string()), vec![
            "S".to_string()
        ]);
        Self { unigrams, digrams }
    }
```

## Processing Modifications

The modified `process_fn` will check with the grammar using `lookup_terminals`
before putting an input token on the stack. It will then create copies of the
stack for every terminal symbol the token corresponds to.
```rust
fn process_fn<T: Token>(token: T, grammar: &Grammar<T>)
-> impl Fn(Vec<Stack<T>>, Stack<T>) -> Vec<Stack<T>> {
    move |new_stacks, current_stack| {
        grammar.lookup_terminals(& token).map_or(
            new_stacks.clone(),
            |t_labels| t_labels.iter().fold(
                new_stacks,
                |mut new_stacks, terminal_label| {
                    new_stacks.append(&mut current_stack.clone()
                        .shift_reduce(
                            BinaryTree::Terminal {
                                label: terminal_label.clone(),
                                token: token.clone()
                            },
                            grammar
                        )
                    );
                    new_stacks
                }
            )
        )
    }
}
```
The modified `shift_reduce` function will check with the grammar using
`lookup_nonterminals` before reducing new terminal and the tree on the top of
the stack. It will then create copies of the stack for every nonterminal symbol
the pair corresponds to:
```rust
    pub fn shift_reduce(
        mut self: Self,
        tree: BinaryTree<T>,
        grammar: & Grammar<T>
    ) -> Vec<Self> {
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
                let new_stacks = vec![self.clone()];

                match grammar.lookup_nonterminals(
                    &(popped_tree.label(), tree.label())
                ) {
                    None => new_stacks,
                    Some(new_nonterminal_labels) => {
                        new_nonterminal_labels.iter().fold(
                            new_stacks,
                            |mut new_stacks, new_nonterminal_label| {
                                let new_nonterminal = BinaryTree::Nonterminal {
                                    label: new_nonterminal_label.clone(),
                                    left: Box::new(popped_tree.clone()),
                                    right: Box::new(tree.clone()),
                                };
                                new_stacks.append(&mut r.clone()
                                    .shift_reduce(new_nonterminal, grammar)
                                );
                                new_stacks
                            }
                        )
                    }
                }
            }
        }
    }
```

## Tokenizeable

I want to clean up the code by introducing a new trait, `Tokenizeable`:
```rust
trait Tokenizeable<T: Token> {
    fn tokenize(self) -> impl Iterator<Item = T>;
}
```
The implementation of this trait for `str` will call the `chars` method, and the
implementation for `Vec<& str>` will call `into_iter`:
```rust
impl Tokenizeable<char> for &str {
    fn tokenize(self) -> impl Iterator<Item = char> {
        self.chars()
    }
}

impl<'a> Tokenizeable<&'a str> for Vec<&'a str> {
    fn tokenize(self) -> impl Iterator<Item = &'a str> {
        self.into_iter()
    }
}
```

Now `generate` can operate on any sequence that can iterate over tokens:
```rust
fn generate<T: Token>(
    input_sequence: impl Tokenizeable<T>,
    grammar: &Grammar<T>
) -> Vec<BinaryTree<T>> {
    generate_stacks(input_sequence.tokenize(), grammar)
        .filter_stacks()
        .tops()
}
```
Calling it becomes more straightforward, too:
```rust
fn main() {
    let x = generate("-1+2*4", &Grammar::expression());
    println!("{} trees", x.len());
    for t in x {
        println!("{}", t);
    }
    let word_sequence = vec!["the", "cat", "sat", "on", "the", "mat"];
    let x = generate(word_sequence, &Grammar::sentence());
    println!("{} trees", x.len());
    for t in x {
        println!("{}", t);
    }
}
```
[This
version](https://github.com/mspandit/rust-binary-tree-generator/tree/2026-04-14)
of the code generates five trees for the expression example. This is to be
expected, because the grammar is ambiguous and allows various orders of
operation for the different operators.

The sentence grammar is deterministic, so the code generates a single tree for
the example.