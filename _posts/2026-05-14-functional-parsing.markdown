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
each taking a single argument&mdash;or at least a smaller number of arguments.

| CFG | Functional Programming |
| --- | ---------------------- |
| {Start, Terminal, Nonterminal} Symbol | Type |
| Production Rule | Constructor returning a type, given arguments of specified types |
| Unary Rule | Constructor returning a type given a single matching argument |
| Binary Rule | Constructor returning a type given two matching arguments |
| Conversion to Chomsky Normal Form | Currying of constructors with multiple arguments|


Therefore, we can represent a unary rule as a function that accepts a terminal
type `T` and, assuming it "matches," returns a nonterminal type `N`. We can
represent a binary rule as a function that accepts two nonterminal types `N`
and, assuming they "match," returns a nonterminal type `N`:

```rust
type Unary<T, N> = dyn Fn(& T) -> Option<N>;
type Binary<N> = dyn Fn(& N, & N) -> Option<N>;
```

A functional grammar (in Chomsky normal form) is a set of unary and binary
rules:

```rust
pub struct Grammar<T, N> {
    unary: Vec<Rc<Unary<T, N>>>,
    binary: Vec<Rc<Binary<N>>>,
}
```

We can now consider the _entire grammar_ as a function. When applied to an input
(terminal) type, it returns a set of nonterminal types, one for each of its
matching unary rules. When applied to two nonterminal types, it returns a set of
nonterminal types, one for each of its matching binary rules.

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

Although Chomsky normal form simplifies a grammar in certain ways, we can go
further by currying functions. A _partial_ grammar composes a grammar.

```rust
pub struct PartialGrammar<T, N>(pub Grammar<T, N>);
```

Its `apply_unary` method simply delegates to the grammar's function.

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

A _symbol_ unifies what is returned from the `apply_unary` and `apply_binary`
methods of a `PartialGrammar`. A symbol composes either
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

A context can be applied to a symbol to produce a set of contexts.

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

The shift/reduce function on a context (now called `apply_token`) first applies
the unary rules of a grammar to an input token to acquire a set of nonterminals.
The grammar is applied to these nonterminals to acquire partial functions. The
context is then applied to the complete and incomplete symbols.

```rust
    pub fn apply_token<T>(self: Self, token: & T, g: & PartialGrammar<T, N>)
    -> Vec<Self>
    where T: Clone + 'static {
        let unary_symbols = g.apply_unary(token);
        let binary_symbols: Vec<Symbol<N>> = g
        .apply_binary(& unary_symbols)
        .into_iter().map(Symbol::Incomplete)
        .collect();
        let unary_symbols: Vec<Symbol<N>>= unary_symbols.clone()
        .into_iter().map(Symbol::Complete)
        .collect();
        [unary_symbols, binary_symbols].concat()
        .into_iter().flat_map(|symbol| self.apply(symbol, g))
        .collect()
    }
```

# Parse State

A _parse state_ composes contexts and a partial grammar:

```rust
pub struct State<T, N>
where N: 'static {
    context: Vec<Context<N>>,
    grammar: PartialGrammar<T, N>,
}
```

A state can be applied to an input token to produce a new state. This is done
simply by applying each context in the old state to the token and collecting the
results.

```rust
    pub fn apply(self: Self, token: & T) -> Self {
        Self {
            context: self.context.into_iter().flat_map(|current_context|
                current_context.apply_token(token, &self.grammar)
            ).collect(),
            grammar: self.grammar,
        }
    }
```

The `filter_stacks` function has been renamed `single_contexts` but is otherwise
very similar. The `tops` function has been modified in an important way. Not
only does it check whether the context is non-empty, it checks whether the
symbol on top is a complete symbol and the start symbol.

```rust
    pub fn tops(self: Self) -> Vec<N> {
        self.context.into_iter().flat_map(|context| context.0.map_or(
            Vec::default(), // Empty context --> return empty vector
            // Non-empty context --> return vector with symbol
            |ref f| match f().0 {
                Symbol::Complete(s) if s.start(s.clone()) => vec![s],
                _ => Vec::default(),
            },
        ))
        .collect()
    }
```

To be able to check whether the complete symbol on top is the start symbol, we
require the nonterminal type to implement the `Start` trait:

```rust
pub trait Start<S> {
    fn start(&self, s: S) -> bool;
}
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
intermediate structures, `Det`, `N`, `P`, `V`, `NP`, `PP`, and `VP`:

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
            (Expression::UnOp(_), Expression::E(_)) => Some(
                Expression::E(format!("({:?} {:?})", left, right))
            ),
            (Expression::E(_), Expression::BinOp(_)) => Some(
                Expression::EBO(format!("({:?} {:?})", left, right))
            ),
            (Expression::EBO(_), Expression::E(_)) => Some(
                Expression::E(format!("({:?} {:?})", left, right))
            ),
            _ => None
        }) as Rc<Binary<Expression>>
     ];
    Grammar::new(unary, binary)
}
```

The `main` function demonstrates the nondeterminism of the binary tree grammar
by displaying 42 "trees" for the input sequence `abcdef`.

It demonstrates the determinism of the sentence grammar by displaying a single "tree" for the input sequence `the cat sat on the mat`.

It demonstrates the nondeterminism of the expression grammar by displaying 5 "trees" for the input sequence `-1+2*4`.

The full code is [here](https://github.com/mspandit/rust-binary-tree-generator/tree/2026-05-14).
