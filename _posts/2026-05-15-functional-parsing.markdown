---
layout: post
title: "Even More Functional Context Free Grammar Parsing"
summary: "Functional representation of grammar rules"
date:   2026-05-14 09:27:00 -0700
---

In the [last](/2026/04/14/cfg-parsing.html)
[couple](/2026/05/01/functional-parsing.html) of posts, we have represented the
grammar as `HashMap`s for "unigrams" and "digrams."

This is a representation of a grammar in [Chomsky normal
form](https://en.wikipedia.org/wiki/Context-free_grammar#Normal_forms).

A context free grammar consists of nonterminal symbols (of which one is a
_start),_ terminal symbols, and production rules. Each rule has a nonterminal
symbol on the left-hand side and a sequence of symbols on the right-hand side.

From a functional programming perspective, a symbol corresponds to a type, and a
rule corresponds to a constructor for that type. A constructor takes one or more
arguments. Unary rules naturally correspond to constructors with a single
argument. Binary rules correspond to constructors with two arguments. The fact
that any CFG can be represented in Chomsky normal form is related to the fact
that a function with numerous arguments can be
[curried](https://en.wikipedia.org/wiki/Currying) into a sequence of functions,
each taking a single argument.

| CFG | Functional Programming |
| --- | ---------------------- |
| {Start, Terminal, Nonterminal} Symbol | Type |
| Production Rule | Constructor returning a type, given arguments of specified types |
| Unary Rule | Constructor returning a type given a single matching argument |
| Binary Rule | Constructor returning a type given two matching arguments |
| Conversion to Chomsky Normal Form | Currying of constructors with multiple arguments|


Therefore, we can represent a unary rule as a function that accepts a terminal
type `T` and returns a nonterminal type `N`&mdash;assuming it "matches." We can
represent a binary rule as a function that accepts two nonterminal types `N`
and, assuming they "match," returns a nonterminal type `N`:

```rust
type Unary<T, N> = dyn Fn(& T) -> Option<N>;
type Binary<N> = dyn Fn(& N, & N) -> Option<N>;
```

A grammar (in Chomsky normal form) is a set of unary and binary rules:

```rust
pub struct Grammar<T, N> {
    unary: Vec<Rc<Unary<T, N>>>,
    binary: Vec<Rc<Binary<N>>>,
}
```

We can now consider the grammar itself as a function. When applied to an input
(terminal) type, it returns a set of nonterminal types corresponding to its
unary rules. When applied to two nonterminal types, it returns a set of
nonterminal types corresponding to its binary rules.

```rust
    // Apply unary rules to a terminal, returning any number of
    // nonterminals
    pub fn apply_unary(&self, token: & T) -> Vec<N> {
        self.unary.iter()
        .flat_map(|rule| rule(token))
        .collect()
    }

    // Apply binary rules to a pair of nonterminals, returning any number of
    // nonterminals
    pub fn apply_binary(self: & Self, left: & N, right: & N) -> Vec<N> {
        self.binary.iter()
        .flat_map(|rule| rule(left, right))
        .collect()
    }
```

# Partial Grammars

A _partial_ grammar can compose a grammar.

```rust
pub struct PartialGrammar<T, N>(pub Grammar<T, N>);
```

Its `apply_unary` function will simply delegate to the grammar's function.

```rust
    pub fn apply_unary(&self, token: & T) -> Vec<N> {
        self.0.apply_unary(token)
    }
```

However, its `apply_binary` function will be very different. First, it will take a
_set_ of nonterminals. For each, it will return a partial function corresponding
to a binary rule applied to the nonterminal. The partial will be ready to accept a second nonterminal and then use the binary rule to return a nonterminal.

```rust
pub type Partial<N> = dyn Fn(& N) -> Vec<N>;
```

```rust
    pub fn apply_binary(self: & Self, symbols: & Vec<N>)
    -> Vec<Rc<Partial<N>>> {
        symbols.iter()
        .map(|left| {
            let left = left.clone();
            let grammar = self.0.clone();
            Rc::new(
                move |right: &N| grammar.apply_binary(&left, right)
            ) as Rc<Partial<N>>
        })
        .collect()
    }
```

# Symbols

A _symbol_ composes
* a nonterminal (in which case it is _complete)_ or
* a partial function (in which case it is _incomplete)_

```rust
pub enum Symbol<N> {
    Complete(N),
    Incomplete(Rc<Partial<N>>),
}
```

# Contexts

A context is a stack of symbols:

```rust
pub struct Context<N>(pub Option<Rc<dyn Fn() -> (Symbol<N>, Self)>>)
```

A context is applicable to a symbol to produce a set of contexts.

There are six combinations of the stack, its top, the symbol, and the result of the application:

| Stack/Top | Symbol | Result |
| --------- | ------- | ------ |
| Empty     | Complete | Context with symbol on top |
| Empty     | Incomplete | Context with symbol on top |
| Complete  | Complete | No contexts |
| Complete  | Incomplete | No contexts |
| Incomplete | Incomplete | Context with symbol pushed on top |
| Incomplete | Complete | In this case, call the partial function on the symbol to get a set of new symbols. 1. Recursively apply the rest of the stack to each new symbol and collect the resulting contexts. 2. For the partial function returned by the grammar for each new symbol, recursively apply the rest of the stack and collect the resulting contexts |


```rust
pub fn apply<T>(
    self: & Self,
    symbol: Symbol<N>,
    grammar: & PartialGrammar<T, N>
)
-> Vec<Self>
where T: Clone + 'static {
    match self.0 {
        None =>
            // Context with symbol on top
            vec![self.clone().push(symbol)],
        Some(ref f) => {
            let (top, rest) = f();
            match (top, symbol.clone()) {
                (Symbol::Complete(_), _) => vec![], // No contexts
                (Symbol::Incomplete(_), Symbol::Incomplete(_)) =>
                    vec![self.clone().push(symbol)], // Context w/symbol on top
                (Symbol::Incomplete(p), Symbol::Complete(s)) => {
                    let new_ss = p(& s);
                    let contextual_results: Vec<Self> = new_ss.iter()
                    .flat_map(|symbol|
                        // Recurse on rest of context with new symbols
                        rest.clone().apply(
                            Symbol::Complete(symbol.clone()),
                            grammar
                        )
                    ).collect();
                    let recursive_results: Vec<Self> = grammar
                    .apply_binary(& new_ss)
                    .into_iter()
                    .flat_map(|partial|
                        // Recurse on partials started by the new symbols
                        rest.clone().apply(Symbol::Incomplete(partial), grammar)
                    ).collect();
                    [contextual_results, recursive_results].concat()
                },
            }
        }
    }
}
```

The shift/reduce function on a context applies the unary rules of a grammar to
an input token. The grammar is applied to these results to acquire partial
functions. The context is then applied to the complete and incomplete symbols.

```rust
    pub fn shift_reduce<T>(self: Self, token: & T, g: & PartialGrammar<T, N>)
    -> Vec<Self>
    where T: Clone + Debug + 'static {
        let unary_symbols = g.apply_unary(token);
        let binary_symbols: Vec<Symbol<N>> = g
        .apply_binary(& unary_symbols)
        .into_iter().map(Symbol::Incomplete)
        .collect();
        let unary_symbols: Vec<Symbol<N>>= unary_symbols.clone()
        .into_iter().map(Symbol::Complete)
        .collect();
        let retval = [unary_symbols, binary_symbols].concat()
        .into_iter().flat_map(|symbol| self.apply(symbol, g))
        .collect();
        retval
    }
```

# Parse State

A _parse state_ composes contexts and a partial grammar:

```rust
```

# Example Grammars

The "binary tree" can very simply be represented as a string:

```rust
pub struct BinaryString(String);
```

A single unary rule converts any character to a string. A single binary rule
puts two strings inside parentheses:

```rust
pub fn binary_string() -> Grammar<char, BinaryString> {
    let unary = vec![
        Rc::new(|token: & char|
            Some(BinaryString(format!("{}", token)))
        ) as Rc<Unary<char, BinaryString>>
    ];
    let binary = vec![
        Rc::new(|left: & BinaryString, right: & BinaryString|
            Some(BinaryString(format!("({:?} {:?})", left, right)))
        ) as Rc<Binary<BinaryString>>
    ];
    Grammar::new(unary, binary)
}
```

The sentence grammar can also be represented using a single unary rule and a
single binary rule, but these rules return different variants for the
intermediate structures:

```rust
pub enum Sentence {
    Det(String),
    N(String),
    P(String),
    V(String),
    NP(String),
    PP(String),
    VP(String),
    S(String),
}

pub fn sentence() -> Grammar<String, Sentence> {
    let unary = vec![
        Rc::new(|token: & String|
            match token.as_str() {
                "the" => Some(Sentence::Det("the".to_string())),
                "cat" | "mat" => Some(Sentence::N(format!("{}", token))),
                "sat" => Some(Sentence::V(format!("{}", token))),
                "on" => Some(Sentence::P(format!("{}", token))),
                _ => None
            }
        ) as Rc<Unary<String, Sentence>>
    ];
    let binary = vec![
        Rc::new(|left: & Sentence, right: & Sentence| match (left, right) {
            (Sentence::Det(_), Sentence::N(_)) => Some(
                Sentence::NP(format!("({:?} {:?})", left, right))
            ),
            (Sentence::V(_), Sentence::NP(_)) => Some(
                Sentence::VP(format!("({:?} {:?})", left, right))
            ),
            (Sentence::V(_), Sentence::PP(_)) => Some(
                Sentence::VP(format!("({:?} {:?})", left, right.clone()))
            ),
            (Sentence::P(_), Sentence::NP(_)) => Some(
                Sentence::PP(format!("({:?} {:?})", left, right.clone()))
            ),
            (Sentence::NP(_), Sentence::VP(_)) => Some(
                Sentence::S(format!("({:?} {:?})", left, right.clone()))
            ),
            _ => None
        }) as Rc<Binary<Sentence>>
     ];
    Grammar::new(unary, binary)
}
```

The expression grammar can also be represented using a single unary rule and a single binary rule, returning different variants for the intermediate structures:

```rust
pub enum Expression {
    UnOp(String),
    E(String),
    BinOp(String),
    EBO(String),
}

pub fn expression() -> Grammar<char, Expression> {
    let unary = vec![
        Rc::new(|token: & char| match token {
            '1' | '2' | '3' | '4' => Some(Expression::E(format!("{}", token))),
            '-' => Some(Expression::UnOp("-".to_string())),
            '+' => Some(Expression::BinOp("+".to_string())),
            '*' => Some(Expression::BinOp("*".to_string())),
            _ => None // No terminal rules
        }) as Rc<Unary<char, Expression>>
    ];
    let binary = vec![
        Rc::new(|left: & Expression, right: & Expression| match (left, right) {
            (Expression::UnOp(_), Expression::E(_)) => Some(Expression::E(format!("({:?} {:?})", left, right))),
            (Expression::E(_), Expression::BinOp(_)) => Some(Expression::EBO(format!("({:?} {:?})", left, right))),
            (Expression::EBO(_), Expression::E(_)) => Some(Expression::E(format!("({:?} {:?})", left, right))),
            _ => None
        }) as Rc<Binary<Expression>>
     ];
    Grammar::new(unary, binary)
}
```

We now have a way of _deserializing_ any data structure, even a recursive one,
from a sequence of characters, strings (or for that matter, any other data
type).

1. Collect various constructors of the desired data structure. Each will take
   one or more arguments of different types. Each of these _intermediate types_
   may have its own constructors.
2. Introduce new constructors and types so that all constructors take one or two
   arguments (conversion to Chomsky normal form)
3. Include the desired data structure in an `enum` with variants for each
   intermediate type.
