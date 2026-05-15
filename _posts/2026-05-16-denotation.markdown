---
layout: post
title: "Denotation"
summary: "Generating Denotation from a Functional CFG"
date:   2026-05-15 07:05:00 -0700
---

In the last post, we represented a context-free grammar and its production rules
as functions. Specifically, rules correspond to constructors, and a grammar is a
set of constructors for a desired type (the start symbol) from values of some
input type (terminal symbols). The grammar included constructors for convenient
intermediate types.

One of the example grammars was a constructor for strings structured as
expressions. For the character sequence `-1+2*4` it produced five trees:

| Output | Interpretation |
| ------ | -------------- |
| `(((((- 1) +) 2) *) 4)` | $$ (-1 + 2) \times 4 $$ |
| `(((- 1) +) ((2 *) 4))` | $$ -1 + (2 \times 4) $$ |
| `(((- ((1 +) 2)) *) 4)` | $$ -(1 + 2) \times 4 $$ |
| `(- ((((1 +) 2) *) 4))` | $$ -((1 + 2) \times 4) $$ |
| `(- ((1 +) ((2 *) 4)))` | $$ -(1 + (2 \times 4)) $$ |

The current grammar does not assume any order of operations. Therefore, all of
these interpretations are valid.

The strings expose alternative (binary) decompositions of the input sequence.

We can modify the grammar so that it actually calculates the value of the
expression while it is parsed from the character sequence.

We start by representing the value of an `E` type as a 32-bit integer.

The value of `UnOp` and `BinOp` types will simply be the characters they were
constructed from.

There's not much we can do with an `EBO` type except represent it as a tuple
with the integer from the `E` type and the character from the `BinOp` type.

```rust
pub enum Expression {
    E(i32),
    UnOp(char),
    BinOp(char),
    EBO(i32, char),
}
```

We then modify the rules. They now perform conversions (`to_digit`) and
calculations (negation, addition, multiplication) when constructing `E` types,
but compose symbols and tokens when constructing other types:

```rust
pub fn expression() -> Grammar<char, Expression> {
    let unary = vec![
        Rc::new(|token: & char| match token {
            '1' | '2' | '3' | '4' => Some(Expression::E(
                token.to_digit(10).unwrap() as i32
            )),
            '-' => Some(Expression::UnOp('-')),
            '+' => Some(Expression::BinOp('+')),
            '*' => Some(Expression::BinOp('*')),
            _ => None // No terminal rules
        }) as Rc<Unary<char, Expression>>
    ];
    let binary = vec![
        Rc::new(|left: & Expression, right: & Expression| match (left, right) {
            (Expression::UnOp(_), Expression::E(right)) => Some(
                Expression::E(-right)
            ),
            (Expression::E(n), Expression::BinOp(c)) => Some(
                Expression::EBO(*n, *c)
            ),
            (Expression::EBO(left, op), Expression::E(right)) => Some(
                Expression::E(match op {
                    '+' => left + right,
                    '*' => left * right,
                    _ => unreachable!()
                })
            ),
            _ => None
        }) as Rc<Binary<Expression>>
     ];
    Grammar::new(unary, binary)
}
```


| Old Output | Interpretation | New Output |
| ---------- | -------------- | ---------- |
| `(((((- 1) +) 2) *) 4)` | $$ (-1 + 2) \times 4 $$ | 4 |
| `(((- 1) +) ((2 *) 4))` | $$ -1 + (2 \times 4) $$ | 7 &dagger; |
| `(((- ((1 +) 2)) *) 4)` | $$ -(1 + 2) \times 4 $$ | -12 |
| `(- ((((1 +) 2) *) 4))` | $$ -((1 + 2) \times 4) $$ | -12 |
| `(- ((1 +) ((2 *) 4)))` | $$ -(1 + (2 \times 4)) $$ | -9 |

A key question is: **How should the grammar be modified to respect order of
operations?** We want it to generate a single, correct output, the one marked by
&dagger;.

Our current solution generates a _set_ of start symbol values. An alternative is
to assign a _probability distribution_ over start symbol values, with the
highest likelihood assigned to the correct value. This is the solution Bill
MacCartney's [SippyCup project](https://github.com/wcmac/sippycup) implements,
by generating parses and then assigning weighted "features" to them. Additional
details are presented in [_Learning Executable Semantic Parsers for Natural
Language Understanding_](https://dl.acm.org/doi/pdf/10.1145/2866568) by Percy
Liang.

Although this approach is valid, a couple of things about it always bothered me:
* The grammar "wastes time" generating incorrect candidate parses that are later
  scored by the model. Why can't the model be "merged" with the grammar so that
  it directly produces scored results?
* The example grammar above is sufficiently ambiguous that it produce the
  desired result among other candidates to be scored, but what if it didn't? No
  amount of feature weight adjustment would generate the desired result.
* The features must be defined manually, even though the _weights_ of those
  features can be computed automatically using examples. Why can't a neural
  network approach be taken where useful features are learned from examples?

To address the first point, we need a grammar whose function is
parameterized&mdash;whose rules are parameterized. To address the second point,
depending on the parameters, the grammar must generate all possible
decompositions, no decompositions, and _every possibility in between._ To
address the third point, if these parameters can be modified using stochastic
gradient descent, then a neural network approach will work, and no manual
feature engineering will be required.