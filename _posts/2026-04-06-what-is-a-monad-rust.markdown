---
layout: post
title: "What is a Monad (in Rust)?"
summary: "Transcription of the video <em>What is a Monad? - Computerphile</em> but modified for Rust"
date:   2026-04-06 12:40:00 -0700
---

Below is my modified transcription of the video [What is a Monad? -
Computerphile](https://www.youtube.com/watch?v=t1e8gqXLbsU) in which a
presentation by [Dr. Graham Hutton](https://people.cs.nott.ac.uk/pszgmh/) is
filmed and edited by Sean Riley. In my revision, I demonstrate a monad in Rust
rather than Haskell.

The concept of monads was invented in mathematics in the 1960s, and then it
was rediscovered in computer science in the 1990s. It gives you a new way of
thinking about programming with effects. This may be one of the most important
new ideas in programming languages in the last 25 years. So that's what we're
going to be looking at today&mdash;programming with monads.

We're going to come at this using an example of writing a function that
evaluates simple expressions. And I'm going to use Rust for this, but we're
going to use it in a very simple way, and I'm going to explain everything as
we're going along.

We're going to start by defining a simple datatype for the kind of expressions
that we're going to be evaluating. So, we'll use the `enum` keyword in Rust,
which introduces a new data type, and then we're going to define a new data type
for expressions. There's two things that an expression can be. It can either be
an integer value, so we'll write that down&mdash;we have `Val` of an `i64`. Or,
it can be the division of two sub-expressions. So we've got two variants here in
our data type&mdash;we've got `Val`, which builds expressions from integers, and
we've got `Div`, which builds expressions from two sub-expressions.

```rust
enum Expr {
    Val(i64),
    Div(Expr, Expr)
}
```

However, the Rust compiler does not like this:

```
error[E0072]: recursive type `Expr` has infinite size
 --> src/lib.rs:1:1
  |
1 | enum Expr {
  | ^^^^^^^^^
2 |     Val(i64),
3 |     Div(Expr, Expr)
  |         ---- recursive without indirection
  |
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
3 |     Div(Box<Expr>, Expr)
  |         ++++    +
```

In order to allocate a new value of an `Expr` type on the stack, Rust needs to
know its size at compilation time. This is not possible if it is defined
recursively. The compiler is suggesting that sub-expressions live on the heap where they will be allocated at run-time. We specify this by putting them inside `Box` pointers:

```rust
enum Expr {
    Val(i64),
    Div(Box<Expr>, Box<Expr>)
}
```

To reiterate what what's actually going on here, we're declaring a new data type
called `Expr`, and it's got two new variants&mdash;one called `Val`, which takes
an integer parameter, and one called `Div`, which takes two sub-expressions as
parameters. Expressions are built up from integer values using a simple division
operator. Many of you may not be familiar of this kind of syntax, so let's have
a couple of examples of values of this data type, so that we make sure
everyone's on the same page.

I'm going to draw a little table. On the left-hand side, I'm going to have what
we would normally write down in mathematics. And then on the right-hand side,
we'll think how would you translate this into a value in this Rust data type?

Let's have three simple examples here&mdash;we'll have one, and we'll have six
divided by two, and let's do one more example, we'll have six divided by three
divided by one.

| Mathematics&nbsp; | &nbsp;Rust |
| ----------- | ---- |
| 1 |  |
| 6 &divide; 2 | |
| 6 &divide; (3 &divide; 1)  |  |

These simple expressions are built up from integers using a division operator.
But, we're writing Rust programs today, so let's think how do these things
actually get represented as values of our expression data type? The first
one is very simple&mdash;if we want to represent the value one, we just need to use
the `Val` tag, so write `Val` of one.

| Mathematics&nbsp; | &nbsp;Rust |
| ----------- | ---- |
| 1 | `Expr::Val(1)` |
| 6 &divide; 2 | |
| 6 &divide; (3 &divide; 1)  |  |

If we want to have an expression like six
divided by two, well it's a division, so we have a `Div` at the top level, and
then we have two values&mdash;we have `Val` six, and `Val` two.

| Mathematics&nbsp; | &nbsp;Rust |
| ----------- | ---- |
| 1 | `Expr::Val(1)` |
| 6 &divide; 2 | `Expr::Div(Box::new((Expr::Val(6), Expr::Val(2))))` |
| 6 &divide; (3 &divide; 1)  |  |

The last one will need two divisions, three `Val` constructors, and then a bunch
of brackets.

| Mathematics&nbsp; | &nbsp;Rust |
| ----------- | ---- |
| 1 | `Expr::Val(1)` |
| 6 &divide; 2 | `Expr::Div(Box::new((Expr::Val(6), Expr::Val(2))))` |
| 6 &divide; (3 &divide; 1)  | `Expr::Div(Box::new(Expr::Val(6)), Box::new(Expr::Div(Box::new(Expr::Val(3)), Box::new(Expr::Val(1)))))` |

Indeed, the following test passes:
```rust
    #[test]
    fn test_expr_type() {
        let one = Expr::Val(1);
        let six_div_two = Expr::Div(Box::new(Expr::Val(6)), Box::new(Expr::Val(2)));
        let six_div_three_div_one = Expr::Div(
            Box::new(Expr::Val(6)),
            Box::new(Expr::Div(
                Box::new(Expr::Val(3)),
                Box::new(Expr::Val(1)),
            ))
        );
    }
```

We've got simple expressions built up from integers using division. Let's write
a function to evaluate these expressions.

We're going to write an function that takes an expression as input, and what
it's going to give back is the integer value of that expression. And there's
going to be two cases here, because we have two kinds of expressions. We have a
case for values, and we need to figure out what to do with that, which we'll do
in a moment. And then we have a case for division, and we need to think what to
do with that. (Note that, in Rust, we _borrow_ the expression rather than taking
ownership of it in this function, because we are treating it as "read-only.")

```rust
fn evaluate(x: & Expr) -> i64 {
    match x {
        Expr::Val(_) => todo!(),
        Expr::Div(expr, expr1) => todo!(),
    }
}
```

So, we've got the skeleton here of a function, and then we just need to fill in
the details. So, how do you evaluate an integer value? Well, that's very simple,
you just give back the number&mdash;so if I had `Val` of one, it's value is just
one. And then how do I evaluate a division? Well, these two expressions here,
`expr1` and `expr2`, these could be as complicated as you wish. So, we need to
evaluate these recursively. So what we would do, is evaluate the first one,
`expr1`, and that will give us an integer. And then we'll evaluate the second
one, `expr2`, and that will give us another integer. And then, all we need to do
is divide one by the other.

```rust
fn evaluate(x: & Expr) -> i64 {
    match x {
        Expr::Val(number) => *number,
        Expr::Div(expr1, expr2) => evaluate(expr1) / evaluate(expr2),
    }
}
```

This simple function evaluates expressions built up from integers using division
&mdash; we just have a simple recursive function, two cases, and everything
looks fine.

But there's a problem with this function, and the problem is that it may crash -
because if you divide a number by zero, then that's undefined, so this function
will just crash.

```rust
    #[test]
    fn demo_crash() {
        let _result = evaluate(
            Expr::Div(
                Box::new(Expr::Val(1)),
                Box::new(Expr::Val(0))
            )
        );
    }
```
```
running 1 test

thread 'tests::demo_crash' (2035286) panicked at src/lib.rs:9:36:
attempt to divide by zero
```

We don't want our programs to crash, so what do we do to fix this problem?

First of all, we're going to define a safe version of the division operator,
which doesn't crash anymore. That's basically the root of the problem
here&mdash;division by zero gives an undefined result, and the function is going
to crash. So, let's define a safe version of the division operator. We're going
to define a function called `safediv`, and it's going to take a couple of
integers, and it's going to give back an `Option` of an integer. `Option` is one
way that we deal with things that can possibly fail in Rust. The function
signature here is not `i64` and `i64` returning `i64`, it's `i64` and `i64`
returning `Option<i64>`, because division may fail. And we'll see how this
`Option` type works in a moment.

So, how do we actually define `safediv`? We take two integers, `n` and `m`,
and then what we'll do is check&mdash;is the second of these zero? Because that's
the case when things would go wrong. So, if `m` happened to be zero, then we
will give back the result `None`. `None` is one of the
variants of the `Option` type. If `m` is not zero, what we're going to do
is give back the result of dividing. `Some` is another variant of
the `Option` type&mdash;`Option` only has two variants, `None`, which
represents things that have gone wrong, or in our case division by zero, and
`Some`, which represent things that have gone fine. In this case, we actually
just get back the result of dividing one number by the other.
```rust
fn safediv(n: i64, m: i64) -> Option<i64> {
    if 0 == m {
        None
    } else {
        Some(n / m)
    }
}
```
We now have a safe version of the division operator, which is
explicitly checking for the case when the function would have crashed. So this
doesn't crash anymore, it returns one of two values&mdash;either `None` if things
go wrong, or `Some` of the division if things have gone fine.

```rust
    #[test]
    fn demo_safediv() {
        assert!(safediv(6, 0).is_none());
        match safediv(6, 3) {
            Some(result) => assert_eq!(2, result),
            None => assert!(false),
        }
    }
```
With this safe division operator, we can rewrite our little `evaluate` function
to make sure that it doesn't crash.

Our new evaluator is going to have a slightly different type than before. The
original function just took an expression as input, and then it gave back an
integer. But that could crash. The new evaluator takes an expression as input as
before, but now it gives you an optional integer, because it could fail, it
could have division by zero.

We'll do the two cases again. In the base case, we can't just return `number` this time,
because we've got to return a `Option` value. And there's only two things we
could return, either `None` or `Some`, and in this case the right thing to do
is to return `Some` of `number`, because if you evaluate a value then that's always going
to succeed, so we use a success tag, which is `Some`, and then we have the
integer value sitting in here.

```rust
        Expr::Val(number) => Some(*number),
```

If we have a division, we need to do a bit more work, because when we evaluate
`expr1` that may fail, when we evaluate `expr2` that may fail, and then when we
do the division that may fail. So, we're going to need to do a little bit of
checking and management of failure.

So, what we're going to do, is when we evaluate a division, first of all, we'll
do a case analysis on the result of evaluating `expr1`. And that could be one of
two things&mdash;it could either be `None`, in which case we're going to do
something, or we could get `Some` number, in which case we're going to do
something. So, there's two cases to consider&mdash;when we evaluate the first
parameter `expr1`, either it succeeds or it fails. So in the failure case, if we
get back `None`, the only sensible thing to do is just to say, well if
evaluation of `expr1` fails, the evaluation of the whole division fails. So
we'll just return `None` as well. In the `Some` case, then we need to evaluate
the second parameter `expr2`. So, what we're going to do is do another case
analysis, we'll do a match evaluate of `expr2`, and then again there's two
possible outcomes which we could have here&mdash;either we could have `None`,
which means it failed, or we could have `Some` of `m`, some other number, in
which case we've succeeded. Then again, we need to think what do we do in each
of these two cases. So, in the first case, if the evaluation of `expr2` fails,
the only sensible thing to do is say, well, we fail as well. In the second case,
we've now got to successfully evaluated expressions&mdash;`expr1` has given the
result `n`, `expr2` has given the result `m`, and now we can do the safe
division. So, in this case we just do `safediv`.

```rust
fn evaluate(x: Expr) -> Option<i64> {
    match x {
        Expr::Val(number) => Some(number),
        Expr::Div(expr1, expr2) => {
            match evaluate(*expr1) {
                None => None,
                Some(n) => match evaluate(*expr2) {
                    None => None,
                    Some(m) => safediv(n, m)
                },
            }
        },
    }
}
```

Now we have a working evaluator. We started off with a two-line program, which
kind of did the essence of evaluation, but it didn't check for things going
wrong&mdash;it didn't check for a division by zero. Now we've fixed the problem
completely, we have a program which works, this program will never crash, it
will always give a well-defined result, either `None` or `Some`, but there's a
bit of a problem with this program, in that it's a bit too long. It's a bit too
verbose, there's quite a lot of noise in here, I can hardly see what's going on
anymore, because it's all of this management of failure.

How can we make this function better? And how can we make it more like the
original function, that didn't work, but still maintain the fact that this
actually does the right thing? And the idea here, is we're going to observe a
common pattern.

When you look at this function, you can see quite clearly we're doing the same
thing twice&mdash;we're doing two matches. What we're doing, is doing a match on the
result of evaluating `expr1`, and if it's `None` we give back `None`, and if
it's `Some`, we do something with the result. And then we do exactly the same
thing with the result of evaluating `expr2`. If that gives `None` we give back
`None`, and if it's a `Some`, we do something with it. So, a very common idea in
computing is when you see the same things multiple times, you abstract them out,
and have them as a definition. And that's what we're going to do here.

Let's draw a little picture first, to capture the pattern which we've seen
twice. We're doing a match on
something, so let me just draw it as an ellipsis&mdash;we don't know what's in there,

```rust
match ... {
    None => None
    Some(x) => ...(x)
}
```
And, there's two cases&mdash;if it's `None`, we give back `None`, and if we get
`Some` of some value `x`, then we're going to process it in some way, we're
going to apply some other function to `x`. So, this is the pattern which we've
seen twice. In the first case, we had eval of `expr1` sitting here, and in the
second case, we had eval of `expr2` sitting here, but this is the same pattern that
we see two times in the new evaluator which we've just written.

We can abstract this out as a definition. We're going to give names to these
ellipses. The first ellipsis is an `Option` value&mdash;it's going to be either
`None` or a `Some`, so we'll call it `m`. And this second ellipsis is going to
be a function, it's going process the result in the case we're successful, so
we'll call this `f`. So, we can turn this picture here into a definition now,
and then we can use it to make our program simpler.

```rust
fn and_then(m: Option<i64>, f: impl Fn(i64) -> Option<i64>)
-> Option<i64> {
    match m {
        None => None,
        Some(x) => f(x),
    }
}
```

This function looks at what the `Option` value is&mdash;if it's `None`, we'll
give back `None`, and if it's `Some` of `x`, we'll apply the function to it.
We've just captured the pattern, which we've seen twice, by a definition now.
So, we have some `Option` value, and then, or in sequence with, some function `f`,
and all we're going to do is look at what the value of the `Option` is&mdash;if
it's failed, we'll fail, if it succeeds, we pass the result to the function `f`.
It's just the idea of abstracting out a common pattern as a definition. So, now
we can use this definition to make our program simpler.

Let's rewrite our evaluator once again. The type will remain the same&mdash;it
takes in an expression as input, and it's going to give back an `Option` value,
as before. But the definition is going to be a bit simpler this time. If we
evaluate a value, we're going to do something. If we evaluate a division, we're
going to do something.

```rust
fn evaluate(x: Expr) -> Option<i64> {
    match x {
        Expr::Val(number) => todo!(),
        Expr::Div(expr1, expr2) => todo!(),
    }
}
```

In the base case, we will return `Some` of `number`. In the division case, we're
going to evaluate `expr1` first, and then if that's successful, using our little
`and_then` function, we're going to feed the result into a lambda expression.
That lambda expression is going to take the result, `n`, that comes from
evaluating `expr1`, and then it's going to evaluate `expr2`. If that's
successful, we're going to feed that result, `m`, into a lambda expression. So,
if these two things are both successful, we'll have two values, `n` and `m`, and
then all we do is call `safediv` with them, then close the brackets.

```rust
fn evaluate(x: & Expr) -> Option<i64> {
    match x {
        Expr::Val(number) => Some(*number),
        Expr::Div(expr1, expr2) => and_then(
            evaluate(expr1),
            |n| and_then(
                evaluate(expr2),
                |m| safediv(n, m)
            )
        )
    }
}
```

This function is equivalent to the version that had all the nested `match`es.
But, that's all been abstracted away now&mdash;it's all been kind of abstracted into
`and_then`, and `safediv`.

This is a nicer program now, but still I'm not entirely happy with this. There's
still some complexity in there&mdash;we're still using the funny lambda
notation, we're still using `and_then`. Maybe I can make it even simpler?
Fortunately, Rust provides an `and_then` function _as a method on the `Option`
enum._ Let's write this function using that method, and then we'll come back to
what this has all got to do with monads. This will be our final program. We take
an expression as input, and it's going to return an `Option` of an integer. The
base case will not change, so we'll get `Some` of `number`. But the recursive
case is going to become a bit simpler, because we use the `and_then` method.
```rust
fn evaluate(x: & Expr) -> Option<i64> {
    match x {
        Expr::Val(number) => Some(*number),
        Expr::Div(expr1, expr2) => evaluate(expr1)
            .and_then(|n| evaluate(expr2)
                .and_then(|m| safediv(n, m))
            )
    }
}
```
If I evaluate a division, I'm going to take the result `n`, from the result of
evaluating `expr1`, if it's successful. Then, we'll take the result `m`, from
the result of evaluating `expr2`, if that's successful. And then, we will call
`safediv`. And this is our final program, and I'm much happier with this one. I
mean, it looks kind of similar to the original program, a similar level of
complexity, but all the failure management is now handled for us automatically.
The failure is happening behind the scenes behind the `and_then` method, and
with `safediv`, but we don't need to see that when we're reading this program.
This is a much nicer program than the last one, because we've kind of abstracted
away from a lot of the detail.

So, you can look at a program like this, and I've hardly mentioned the word
monads in the last ten minutes, you can say what's this actually got to do with
monads? Well, what we've actually done, is we've rediscovered what's known as
the `Option` monad. The `Option` monad is three things&mdash;it's the `Option` type, or
really the `Option` type constructor, because it takes a parameter. So you can
have an `Option` of an integer, or option of a Boolean, or option of whatever you
like. And then it's two functions&mdash;it's the function called `Some`, and it's
the `and_then` method which we introduced. And we can think about what are the
types of these things? `Some` takes a thing of any old
type, `T`&mdash;could be an integer, could be a Boolean, could be whatever you like.
And it converts it into a `Option` value. So, in our case, this just took an
integer like five, and we return `Option` of five.

And what it gives you, is a bridge between the pure world of values here, and
the impure world of things that could go wrong&mdash;so it's a bridge from pure to
impure, if you like. And what `and_then` does, is it gives you a way of
sequencing things&mdash;so you give it something which can fail, an `Option<T>`, and
then you give it a function that tells you what to do with that `T`, if you
succeed&mdash;so a `T` to `Option<U>`. And then, finally, what you're going to get
back is a `Option<U>`. Okay, and this is all that a monad is essentially&mdash;a
monad is some kind of type constructor, like `Option`, or `List`, or something
else, as there's many other examples, together with two functions that have
these types here. So, what we've essentially done is rediscovered what's called
the `Option` monad.

We seem to have gone through quite a lot of steps, to write in the end quite a
simple program. What was the actual point here? So there's four points which I
would like to emphasize here.

So, the first point, is that the same idea we've seen works for other effects as
well&mdash;it's not specific to `Option`, which captures failure. The same idea can
be used with other kinds of effects like input/output, like mutable state, like
reading from environments, like writing to log files, non-determinism. All sorts
of other things which you think of as being effects in programming languages fit
exactly the same pattern. So, monads kind of give you a uniform framework for
thinking about programming with effects.

Another important point is that it supports separation of pure code from
effects. Pure functions just take inputs, and produce outputs, they don't have
any kind of side effects at all. But you need to have side effects to write real
programs. So, what monads give you is a way of doing impure things, like proper
side effects, like input/output, separately from pure functions like division.

Another important point here, is that the use of the effects is explicit in the
types. When I wrote the evaluator which didn't fail, it took an expression as
input, and it delivered an `Option` of an integer. So, the `Option` in the type
is telling me that this program may fail. So, this is the idea of being explicit
about what kind of effects, or side effects, that your programs can have in the
types. And this is a very, very powerful idea.

And the last thing is, it's a little bit strange, but it's particularly
interesting, it's the idea of writing functions that work for any effect&mdash;we
might call this kind of effect polymorphism. So, a simple example of this would
be maybe you have a sequence of things, which can have some effects, and you
want to run them all one after the other. You could write a generic function, in
a language like Haskell which supports monads, which would take a sequence of
effects of any kind, any monadic type, and it would run them for you. So this is
a very, very powerful idea, and languages like Haskell have libraries of kind of
generic effect functions, which are very useful. So, that's basically all I want
to say.

Just going back to the start, I think the idea of programming with monads is one
of the most important developments in programming languages in the last 25
years&mdash;I find this particularly fascinating. We've only really touched on
the surface here, and if you want to know a little bit more, I can do a bit of a
plug&mdash;I have a new book which came out fairly recently, [Programming in
Haskell](https://www.amazon.com/Programming-Haskell-Graham-Hutton/dp/1316626229/ref=sr_1_1),
and this has got a chapter specifically about this, which goes into much more
detail. I've only really touched on the surface, there's lots of things I didn't
say, which maybe you need to know to write real programs using this stuff. So,
you could have a look in the book to find out more about that.
