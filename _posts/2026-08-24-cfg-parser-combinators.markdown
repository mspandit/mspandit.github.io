---
layout: post
title: "Combinators for Functional CFG Definition"
summary: ""
date:   2026-08-24 16:05:00 -0700
---

In the last three posts ([1](/2026/04/14/cfg-parsing.html),
[2](/2026/05/01/functional-parsing.html),
[3](/2026/05/14/functional-parsing.html)) we have defined each grammar as a
`HashMap` of unary and binary functions.

# Keep it Simple

A more functional way of defining a grammar---of arbitrary complexity---is by
_composing_ it from simpler grammars.

The simplest grammar is a unary rule, a function that may or may not map a
terminal input to a nonterminal output:

```rust
type Unary<T, N> = fn(& T) -> Option<N>;
```

A simple but _nondeterministic_ rule may or may not map a terminal input to
_multiple_ nonterminal outputs. We represent the output as a `Vec<N>`. An empty
vector substitutes for `None` to indicate there is no mapping.

```rust
type Nondeterministic<T, N> = fn(& T) -> Vec<N>;
```

Professor [Graham Hutton](https://people.cs.nott.ac.uk/pszgmh/) of the
University of Nottingham pioneered work on functional programming, grammars, and
parsers. As he writes in _Programming in Haskell,_ 2nd Ed. p. 161,

> The key is to view the type [`Vec<N>`] as a generalisation of [`Option<N>`]
> that permits multiple results in the case of success. More precisely, we can
> think of the empty list as representing failure, and a nonempty list as
> representing all the possible ways in which a result may succeed.

To convert one to the other, we need a function that accepts a `Unary` and
returns a `Nondeterministic`. The returned function must call the `Unary` and if
return the result in a vector, or an empty vector if the result is `None`:

```rust
// DOESN'T COMPILE
impl<T, N> Nondeterministic<T, N> {
    fn from(u: Unary<T, N>) -> Self {
        move |t: & T| {
            match u(t) { // call the unary function
                None => vec![],
                Some(n) => vec![n],
            }
        }
    }
}
```

# Rust Friction

Unfortunately, there are two problems with the above
1. It attempts to provide an implementation for a primitive type, namely `type
   Nondeterministic<T, N> = fn(& T) -> Vec<N>;` This is not allowed in Rust.
2. A Rust closure has a unique type of its own and can only be coerced to the
   `Nondeterministic<T, N>` type if it captures none of its environment. `u` is
   defined outside the above closure, and `from` attempts to return a closure
   that captures it.

We get around the first problem by redefining `Nondeterministic` as `struct`
instead of a `type`.

We get arond the second problem by storing, inside the struct, a pointer to a
closure. The closure with its unique type is moved to the heap, but it becomes a
_trait object,_ an object that implements a specified trait.

```rust
struct Nondeterministic<T, N>(Box<dyn Fn(& T) -> Vec<N>>);
```

Implementing the conversion as the `From` trait gives us one small convenience:
We can now call the `into` method on a `Unary<T, N>` to convert it in an
idiomatic way.

```rust
impl<T, N> From<Unary<T, N>> for Nondeterministic<T, N>
where T: 'static, N: 'static {
    fn from(u: Unary<T, N>) -> Self {
        Nondeterministic(Box::new(move |t: & T| {
            match u(t) {
                None => vec![],
                Some(n) => vec![n],
            }
        }))
    }
}
```

When `Nondeterministic` was just a synonym for a function type, we could call it
directly. Now that it is a struct, we need to implement a `call` method:

```rust
impl<T, N> Nondeterministic<T, N> {
    pub fn call(self: & Self, t: & T) -> Vec<N> {
        (self.0)(t)
    }
}
```

# A Wealth of Choices

This is sufficient only in the case that a “grammar” consists of a single unary
rule. We need a way to combine `Nondeterministic`s to create new ones.

The _choice_ combinator allows a rule to combine two rules as alternatives. It
is implemented as the `or` method that accepts another `Nondeterministic`. The
resulting `Nondeterministic` combines the results of `Self` with the results of
the other:
```rust
fn or(self: Self, other: Self) -> Self
where T: 'static, N: 'static {
    Nondeterministic(Box::new(move |t: & T| {
        let mut v = self.call(t);
        v.extend(other.call(t));
        v
    }))
}
```

# One Thing at a Time

Unary rules are insufficient even if we can define alternatives between them. We
need a way to define binary---indeed $$n$$-ary---rules.

We’d like to represent an $$n$$-ary rule as an [applicative
functor](https://en.wikipedia.org/wiki/Applicative_functor). This will allow us
to define and represent rules of any length---no need for conversion to Chomsky
Normal Form.

Under the applicative pattern, the result of a _deterministic_ $$n$$-ary rule
would be one of the following:

* `None` if the function consumed a token but failed
* a nonterminal result if the final RHS token was consumed successfully
* a function---another deterministic $$n$$-ary rule---if additional tokens must
  be consumed before success/failure can be determined

The latter variant I call a
[`Continuation`](https://en.wikipedia.org/wiki/Continuation-passing_style)
because it reflects what is to be done upon completion of the function.

```rust
type Nary<T, N> = fn(& T) -> Option<Grammar<T, N>>
enum Grammar<T, N> {
    Nonterminal(N),
    Continuation(Nary<T, N>),
}
```

This is similar to currying, in which a function taking $$n$$ arguments is
represented as $$n$$ functions, each taking a single argument, of which $$n − 1$$
return another function.

As Hutton writes in _Programming in Haskell,_ 2nd Ed., p. 158,

> In particular, we don’t require special versions of application for functions
> with different numbers of arguments, instead relying on currying in
> definitions…

Following the same logic as we did for unary rules, the result of a
_nondeterministic_ $$n$$-ary rule is a _vector_ where each element is either a
nonterminal or another nondeterministic $$n$$-ary rule.

Thus far, we could get away with using Rust’s simplest pointer type, `Box`. But
later, we will want to clone this pointer to allow multiple references to the
same function. Therefore, we will use the reference counting `Rc` pointer
instead.

```rust
#[derive(Clone)]
pub struct NDNary<T, N>(
    pub Rc<dyn Fn(& T) -> Vec<Grammar<T, N>>>
)
where N: Clone, T: Clone;

#[derive(Clone)]
pub enum Grammar<T, N>
where N: Clone, T: Clone {
    Nonterminal(N),
    Continuation(NDNary<T, N>),
}
```

Next, we’d like to be able to construct an $$n$$-ary rule from two others. To do
this, we’ll write a combinator called `then`. Your first thought might be that
`then` should simply take two `NDNary`s, the way `or` did.

However, there are crucial differences between the function returned by the `or`
(choice) combinator or and the one returned by the `then` (sequence) combinator.

| Choice Combinator `or` | Sequence Combinator `then` |
| ---------------------- | -------------------------- |
| Preserves (and returns) the results of applying both rules. | Returns only the results of applying the second rule. |
| Imposes no preconditions on applying either rule. | Imposes the result(s) of first rule as a precondition on applying the second rule. |

Because of these differences, instead of providing two `NDNary`s to `then`,
we'll provide an `NDNary` and _a callback function that returns a second
`NDNary`._ This is the [_monadic
bind_](https://en.wikipedia.org/wiki/Monad_(functional_programming)#Overview)
operation, and it gives critical flexibility to the construction of complex
grammars.

| Choice Combinator | Sequence Combinator | Monadic Bind |
| ----------------- | ------------------- | ------------ |
| Preserves (and returns) the results of applying both functions. | Returns only the results of applying the second function. | Receives the results of the first function (as an argument to the callback function) even though it returns the results of the second function |
| Imposes no preconditions on applying either function. | Imposes the first function as a precondition on applying the second function. | Using the callback, can define the second function on the fly or otherwise condition it on the results of the first |

Of course, if this flexibility is not needed, the callback function can discard
any results from the first function and return a fixed function for combination.

The combination calls the first function (`self`) on a token, generating a
vector of nonterminals or continuations. For each result in the vector,
* If it is a nonterminal `n`, then it is passed to the callback. The resulting
  `NDNary` is returned as a continuation.
* If it is a continuation, then it means the current rule must consume
  additional tokens before generating a nonterminal. We sequence the
  continuation with the result of the callback and return that as a
  continuation.

```rust
pub fn then<M, F>(self: Self, f: F) -> NDNary<T, M>
where
    M: Clone,
    F: Fn(& N)
-> NDNary<T, M> + Clone + 'static {
    use Grammar::*;
    NDNary(Rc::new(move |t| {
        self.call(t)
        .into_iter()
        .map(|x| match x {
            Nonterminal(n) => Continuation(f(&n)),
            Continuation(cont) => Continuation(
                cont.then(f.clone())
            ),
        })
        .collect()
    }))
}
```

We wrote `then` with the purpose of sequencing grammars, but it can also be used
to _convert_ or otherwise transform the results of grammars. If the callback
function returns a `Continuation` variant, an additional input token will be
consumed in sequence, but if the callback function returns a `Nonterminal`, then
the result(s) of the prior grammar will be converted without consuming an
additional input token.

Because the resulting grammar produces the results of the second grammar for
every result of the first grammar, it's appropriate to think of `then` as a
_multiplication_ operation on grammars.

# Keep it Kleene

In addition to choice and sequence combinators, [Kleene
star](https://en.wikipedia.org/wiki/Kleene_star) and
[plus](https://en.wikipedia.org/wiki/Kleene_star#Kleene_plus) operators add
convenience to the definition of grammars.

These are tricky due to three problems:
1. They are nondeterministic with respect to arity. Plus terminates after _one or
  more_ applications, while star terminates after _zero or more._
2. They convert a `NDNary<T, N>` into a `NDNary<T, Vec<N>>`
3. Hutton defines them, recursively, in terms of each other. In [this
  1998 paper](https://www.cs.tufts.edu/~nr/cs257/archive/graham-hutton/monadic-parsing-jfp.pdf)
  with Erik Meijer, they use `many` and `many1`, while in [his own
  1990 paper](https://people.cs.nott.ac.uk/pszgmh/combinators.pdf), he uses `many`
  and `some`

## How Long is a Piece of String?

Problem 1. can be avoided by assuming that the _caller_ of a `NDNary`
will handle the case of zero applications.

Under the applicative pattern, the result of a function might be another
function. We can implement two methods on `Grammar`:
* `shift` replaces `call`, consuming a token by calling the continuation (for
  which we use the `Shift` variant) to return a vector of nonterminals or
  continuations
* `reduce` returns a vector (for which we use the `Reduce` variant) of
  nonterminals or continuations without consuming any tokens

In either case, an empty vector is returned if the function fails.

```rust
#[derive(Clone)]
pub enum Grammar<T, N>
where
    N: Clone,
    T: Clone,
{
    Nonterminal(N),
    Reduce(Vec<Grammar<T, N>>),
    Shift(NDNary<T, N>),
}

impl<T, N> Grammar<T, N>
where
    N: Clone,
    T: Clone,
{
    // For Nonterminal, fail
    // For Reduce, return a Reduce of the reduction
    // For Shift, call the function
    pub fn shift(self: &Self, t: &T) -> Grammar<T, N>
    where
        N: 'static,
        T: 'static,
    {
        use Grammar::*;
        match self {
            Nonterminal(_) => Reduce(vec![]),
            Reduce(_) => Reduce
                self.reduce()
                .iter()
                .map(|g| g.shift(t))
                .collect()
            ),
            Shift(ndnary) => ndnary.call(t),
        }
    }

    // Flatten the grammar to contain only Nonterminal
    // or Shift variants
    pub fn reduce(self: &Self) -> Vec<Self> {
        use Grammar::*;
        match self {
            Reduce(rs) => rs.iter()
                .flat_map(Grammar::reduce)
                .collect(),
            Nonterminal(_) | Shift(_) => vec![self.clone()],
        }
    }
```
What this says is that if you have a `Grammar::Nonterminal` and you insist on
passing it a token, you will receive a failure result `Reduce(vec![])`.

If you have a `Reduce` and pass it a token, then it will be flattened (to
eliminate embedded `Reduce`s) and the token will be passed to each result. The
vector of those results will be returned in a `Reduce` variant.

`or` is simply a `Reduce` of the combined grammars:
```rust
pub fn or(self: Self, other: Self) -> Self {
    Grammar::Reduce(vec![self.clone(), other.clone()])
}
```

Because the resulting grammar sums the results of two grammars, it's appropriate
to think of `or` as an _addition_ operation on grammars, with the failure
grammar `Reduce(vec![])` constituting the "zero" of the sum.

```rust
#[test]
fn test_or_identity() {
    use Grammar::*;
    let failure: Grammar<char, char> = Reduce(vec![]);
    let g = failure.or(& item());
    assert_eq!(
        format!("{:?}", g.shift(& 'a').reduce()),
        "[Nonterminal('a')]"
    );
}
```

One useful function to eliminate a lot of boilerplate is `item`:
```rust
// Eliminates the Grammar::Shift(Rc::new(...)) boilerplate
pub fn item<T, U>() -> Grammar<T, U>
where
    T: Clone,
    U: Clone + std::convert::From<T>,
{
    Grammar::Shift(Rc::new(|input: &T| Grammar::Nonterminal(
        input.clone().into()
    )))
}
```

## Conversion Therapy

Problem 2. is solved by the sequence operator `then` for `Grammar`. If
the callback returns a `Nonterminal` then it has converted the result(s) of the
first grammar.

| When the first grammar is a | `then` |
| --------------------------- | ------ |
| `Nonterminal` | uses the second grammar to return a converted result |
| `Reduce`  | returns a `Reduce` sequencing the second grammar over each element of the first grammar |
| `Shift` |  returns a `Shift` that sequences the second grammar with the first grammar |

```rust
pub fn then<M, F>(self: Self, f: F) -> Grammar<T, M>
where
    T: 'static,
    N: 'static,
    M: Clone,
    F: Fn(&N) -> Grammar<T, M> + Clone + 'static,
{
    use Grammar::*;
    match self {
        Nonterminal(n) => f(&n),
        Reduce(rs) => {
            let rs = rs.clone();
            Reduce(
                rs.into_iter()
                .map(|g| g.then(f.clone()))
                .collect()
            )
        }
        Shift(ndnary) => Shift(NDNary(Rc::new(move |t| ndnary
            .call(t)
            .then(f.clone())
        ))),
    }
}
```

## Two Birds with One Stone

The above modifications allow the definition of `plus` and `star` simply, in terms of each other:

```rust

pub fn star(self: Self) -> Grammar<T, Vec<N>>
where
    T: 'static,
    N: 'static,
{
    use Grammar::*;
    self.clone().plus().or(Nonterminal(vec![]))
}

pub fn plus(self: Self) -> Grammar<T, Vec<N>>
where
    T: 'static,
    N: 'static,
{
    use Grammar::*;
    self.clone().then(move |a| {
        let a = a.clone();
        self.clone().star().then(move |v_a| {
            let mut result = vec![a.clone()];
            result.extend(v_a.clone());
            Nonterminal(result)
        })
    })
}
```

# <a href="https://en.wikipedia.org/wiki/Ouroboros#Cybernetics">Ouroboros</a>

It's frequently convenient and expressive to define a recursive grammar, where
the RHS refers to the LHS terminal. Recursive grammars are tricky because they
can [lead to infinite
loops](https://github.com/glebec/left-recursion#the-problem), either when
grammars are defined using combinators or when they parse input tokens.

Recursion can be _indirect,_ where the RHS includes nonterminals that, in turn,
have RHSs that refer to the original LHS nonterminal. (There is a cycle in the
directed graph of LHS symbols pointing to their RHS symbols.)

The code above can handle indirect recursion, as evidenced by passing
tests on the `expr()` grammar:
```rust
fn factor() -> Grammar<char, i64> {
    character('(')
        .then(move |_| {
            expr().then(move |x| {
                let x = x.clone();
                character(')').then(
                    move |_| Grammar::Nonterminal(x.clone())
                )
            })
        })
        .or(integer())
}
fn term() -> Grammar<char, i64> {
    factor()
        .then(|x| {
            let x = x.clone();
            character('*')
            .then(move |_| term()
                .then(move |y| Grammar::Nonterminal(x * y))
            )
        })
        .or(factor())
}
fn expr() -> Grammar<char, i64> {
    term()
        .then(move |x| {
            let x = x.clone();
            character('+')
            .then(move |_| expr()
                .then(move |y| Grammar::Nonterminal(x + y))
            )
        })
        .or(term())
}
```

_Direct_ recursion means that, for a given rule, the RHS includes a reference to
the LHS nonterminal.

The code above can handle direct recursion as evidenced by passing the following test:
```rust
// This consumes a token before recursion, preventing stack
// overflow
pub fn last1() -> Grammar<char, String> {
    use Grammar::*;
    item()
    .then(|c|
        last1()
        .or(Nonterminal(format!("{c}")))
    )
}

#[test]
fn test_last1() {
    let g = last1();
    let x = g.shift(& 'a').reduce();
    assert_eq!(
        format!("{x:?}"),
        "[Shift, Nonterminal(\"a\")]"
    );
    let x = x[0].shift(& 'b').reduce();
    assert_eq!(
        format!("{x:?}"),
        "[Shift, Nonterminal(\"b\")]"
    );
    let x = g.parse(& vec!['a', 'b', 'c', '1', '?', '!']);
    assert_eq!(
        format!("{x:?}"),
        "[Shift, Nonterminal(\"!\")]"
    );
}
```

Direct _left_ recursion refers to the case where the recursive reference---the
LHS symbol---is the _first_ symbol on the RHS. The binary string grammar, `S <--
S S | c` is direct left-recursive.

One problem is how to _define_ a left-recursive grammar in the first place,
because it requires the nonterminal to be referenced _during_ its own definition.
The following correctly generates a warning that the function cannot return
without recursing. It overflows the stack during definition of the grammar:

```rust
pub fn binary_string() -> Grammar<char, String> {
    binary_string()
    .then(|left| binary_string()
        .then(|right| Grammar::Nonterminal(
            format!("({left} {right})")
        ))
    )
    .or(binary_string().then(|c| Grammar::Nonterminal(
        format!("{c}"))
    ))
}
```
(A direct left-recursive grammar _that never consumes tokens_ like `S <-- S`
will loop infinitely, but it should be possible to detect this case.)

Top-down parsers like Hutton's cannot handle direct left recursion, because they
"don't know" when to begin consuming tokens. On p. 16, [Hutton and
Meijer](https://people.cs.nott.ac.uk/pszgmh/monparsing.pdf) say of an expression
grammar that the "first thing it does is make a recursive call to itself...Thus
[it] never makes any progress and hence does not terminate."

> The biggest problem with this parser is that it is _left-recursive._ For many
> parser combinator libraries, This will cause infinite recursion at runtime
> since the recursion is unguarded by input consumption...Expressions with left
> recursion cannot be encoded by recursive descent parsers and will diverge.

--- _[Design Patterns for Parser Combinators (Functional
Pearl)](https://dl.acm.org/doi/epdf/10.1145/3471874.3472984),_ Jamie Willis,
Nicolas Wu, 2021

Willis and Wu write that [Hutton and
Meijer](https://people.cs.nott.ac.uk/pszgmh/monparsing.pdf) "discuss the classic
technique of replacing left recursion with iteration or recursion with an
accumulating parameter."

> An important restriction on most existing combinator parsers...is that they are
> unable to deal with left-recursion.

-- _[Parsec: Direct Style Monadic Parser Combinators For The Real
World](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/parsec-paper-letter.pdf),_
Daan
Leijen, Erik Meijer, October 4, 2001

We can at least hope that our use of continuations prevents infinite loops
during execution.

[Hutton and Meijer](https://people.cs.nott.ac.uk/pszgmh/monparsing.pdf) redefine
the expression grammar in a way that eliminates the left-recursion. Perhaps more
importantly, they define a new combinator `chainl1`. However, that combinator
appears to be specific to an expression grammar which is intended to be
deterministic. Furthermore, it seems to assume that expressions are separated by
operators. These assumptions make it difficult to adapt to the binary string
grammar which is intended to be ambiguous and where there is no separation
between the recursive RHS nonterminals.

The
[Y-combinator](https://en.wikipedia.org/wiki/Fixed-point_combinator#Y_combinator)
suggests using a _grammar generator._ The generator transforms a grammar (passed
in as a named argument) into a new one. Once the generator is defined, it can be
passed to itself (yes!) to generate a recursive grammar. This method allows a
recursive grammar successfully to be defined. However, when given a token, such
a grammar may still attempt immediately to make recursive calls, and possibly
overflow the stack.

The difficulty of the binary string grammar arises from this fact: Without
knowing in advance the number of tokens to be consumed, it is not possible to
know how many levels of recursive calls a continuation should make.

The binary string grammar is further complicated by the fact that it makes _two_
recursive calls: `S <-- S S | c`

I made numerous trials and errors over several weeks. (I have preserved several
additional tests from these trials.) Finally, I defined the binary string
grammar using combinators and the following generator:
```rust
// (Recursive) generator returns a binary string
// grammar that consumes $n$ tokens.
// S <- char
// S <- S S
fn binary_generator(n: usize) -> Grammar<char, String> {
    use Grammar::*;
    match n {
        0 => Reduce(vec![]),
        1 => item(),
        n => (1..n).fold(
            binary_generator(0),
            |g, i| g.or(& binary_generator(i)
                .then(move |left: & String| {
                    let left_clone = left.clone();
                    binary_generator(n - i).then(
                        move |right: & String| {
                            Nonterminal(
                                format!("({left_clone} {right})")
                            )
                        }
                    )
                })
            )
        ),
    }
}

pub fn binary_string() -> Grammar<char, String> {
    item().star() // Stack inputs
    .then(move |cs: & Vec<char>| {
        // Initialize with grammar of the necessary
        // depth, then apply it to history of inputs
        cs.iter().fold(
            binary_generator(cs.len()),
            |g, c| g.shift(c)
        )
    })
}
```

`binary_string` simply collects all of the inputs into a `Vec<char>` using
`item().star()`. Once the number of tokens is known, `binary_generator()`
generates a grammar that will consume the first one---and generate continuations
for the remainder. The `fold` call iteratively passes every token to this
grammar and its continuations.

`binary_generator` returns the failure case `Reduce(vec![])` if no tokens are to
be consumed, and `item()` if a single token is to be consumed.

If $$n > 1$$ tokens are to be consumed, it might be done via a recursive call in
either position. Therefore, we `fold` over the range `(1..n)` and let one
recursive call consume the earlier tokens and let the other recursive call
consume the later tokens. These grammars are combined by iteratively calling
`or` to allow all possible binary decompositions of the token sequence.

We can generalize a `left_recursive` function that will prove useful:
```rust
pub fn left_recursive<T, N>(
    generator: fn(usize) -> Grammar<T, N>
)
-> Grammar<T, N>
where
    T: Clone + 'static + Debug,
    N: Clone + 'static + Debug
{
    item().star() // Stack inputs
    .then(move |cs: & Vec<T>| {
        // Initialize with grammar of the necessary
        // depth, then apply it to history of inputs
        cs.iter().fold(
            generator(cs.len()),
            |g, c| g.shift(c)
        )
    })
}

pub fn binary_string() -> Grammar<char, String> {
    left_recursive(binary_generator)
}
```
# <a href="https://en.wikipedia.org/wiki/GNU#Name">GNU Stands for "GNU's Not Unix</a>"

Using combinators and the `left_recursive` function, we can define the
left-recursive version of the expression grammar:
```rust
// Number <- '1' | '2' | '3' | '4'
fn number() ->Grammar<char, Expression> {
    use Grammar::*;
    character('1')
    .or(& character('2'))
    .or(& character('3'))
    .or(& character('4'))
    .then(move |c| {
        Nonterminal(Expression::E(format!("{c}")))
    })
}

// UnOp <- '-' | '+'
fn un_op() -> Grammar<char, Expression> {
    use Grammar::*;
    character('-')
    .or(& character('+'))
    .then(move |c| {
        Nonterminal(Expression::UnOp(format!("{c}")))
    })
}

// BinOp <- '*' | '-' | '+'
fn bin_op() -> Grammar<char, Expression> {
    use Grammar::*;
    character('-')
    .or(& character('+'))
    .or(& character('*'))
    .then(move |c| {
        Nonterminal(Expression::BinOp(format!("{c}")))
    })
}

// (Recursive) generator returns an expression
// grammar that consumes $n$ tokens.
// E <- Number
// E <- UnOp E | E BinOp E
fn expr_gen(n: usize) -> Grammar<char, Expression> {
    use Grammar::*;
    match n {
        0 => Reduce(vec![]),
        1 => number(),
        n => (1..n).fold(
            expr_gen(0),
            |res, i| res.or(& expr_gen(i)
                .then(move |left_e| {
                    let le2 = left_e.clone();
                    bin_op().then(move |op| {
                        let op_clone = op.clone();
                        let le2 = le2.clone();
                        expr_gen(n - i).then(move |right_e| {
                            use Expression::*;
                            let re2 = right_e.clone();
                            let le2 = le2.clone();
                            Nonterminal(
                                E(format!("({le2:?} {op_clone:?} {re2:?})"))
                            )
                        })
                    })
                })
            )
        )
        .or(
            & un_op().then(move |op| {
                let op_clone = op.clone();
                expr_gen(n - 1).then(move |e | {
                    use Expression::*;
                    let e_clone = e.clone();
                    let op_clone = op_clone.clone();
                    match (op_clone, e_clone) {
                        (UnOp(op), E(e)) => Nonterminal(E(format!("{op}{e}"))),
                        _ => panic!("Unexpected pattern"),
                    }
                })
            })
        )
    }
}

pub fn expression() -> Grammar<char, Expression> {
    left_recursive(expr_gen)
}
```

# Conclusion

This implementation successfully enables the definition of even the
left-recursive binary string and expression grammars, with the convenience and
expressiveness of combinators. The `main` function demonstrates the use of these
functions on the binary string grammar, the sentence grammar, and the expression
grammar.

I am dissatisfied with the need to hand-write a complete generator function in
the case of left-recursive grammars. However, after defining and refactoring a
few left-recursive grammars with hand-written generator functions, I hope to
observe additional patterns that might be factored out as reusable functions.

Indeed, the handling of the base case and recursive case in separate arms of the
`match` might be one example.

There is another source of dissatisfaction: the left-recursive grammars not only
store their entire input history (in a `Vec<char>`) but they recursively
generate a fresh grammar on every input and pass it the entire history of
tokens.

Guido Van Rossum, the creator of Python,
[described](https://medium.com/@gvanrossum_83706/left-recursive-peg-grammars-65dab3c580e1)
how to reduce repetitive computation for recursive grammars using memoization.
Although I haven't implemented this yet, my use of pure functions (that always
return the same output for the same input) will facilitate memoization.

The full code is here.
