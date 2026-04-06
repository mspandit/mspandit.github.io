---
layout: post
title: "What is a Monad (in Rust)?"
summary: ""
date:   2026-04-06 12:40:00 -0700
---

Below is a transcription of the video [What is a Monad? -
Computerphile](https://www.youtube.com/watch?v=t1e8gqXLbsU) in which a
presentation by [Dr. Graham Hutton](https://people.cs.nott.ac.uk/pszgmh/) is
filmed and edited by Sean Riley. In the revision of this post, I will modify it
to demonstrate a monad in Rust rather than Haskell.

So, monads are a concept that was invented in mathematics in the 1960s, and
then it was rediscovered in computer science in the 1990s. And what it gives
you, is a new way of thinking about programming with effects. And for me, this
is one of the most important new ideas in programming languages in the last 25
years. So that's what we're going to be looking at today - programming with monads.

We're going to come at this using a simple example, and the example that
we're going to look at is the idea of writing a function that evaluates simple
expressions. And I'm going to use Haskell for this, but it doesn't matter if you don't
know anything about Haskell, because we're going to use it in a very simple
way, and I'm going to explain everything as we're going along.

So, what we're going to start with, is by defining a simple datatype for the
kind of expressions that we're going to be evaluating. So, we'll use the `data`
keyword in Haskell, which introduces a new data type, and then we're going to
define a new data type for expressions. And then there's two things that an
expression can be. It can either be an integer value, so we'll write that down -
we have `Val` of an `Int`. Or, it can be the division of two sub-expressions. So
we've got two constructors here in our data type - we've got `Val`, which builds
expressions from integers, and we've got `Div`, which builds expressions from two
sub-expressions.

So, just to reiterate what what's actually going on here, we're declaring a new
data type called `Expr`, and it's got two new constructors - one called `Val`, which
takes an integer parameter, and one called Div, which takes two sub-expressions
as parameters as well. So basically what we're working with is expressions that
are built up from integer values using a simple division operator. So, many of
you may not be familiar of this kind of syntax, so let's have a couple of
examples of values of this data type, so that we make sure everyone's on the
same page.

So, what I'm going to do here, is draw a little table. So, on one side, on the
left-hand side, I'm going to have what we would normally write down in
mathematics. And then on the right-hand side, we'll think how would you
translate this into a value in this Haskell data type?

So, let's have three simple examples here - we'll have one, and we'll have six
divided by two, and let's do one more example, we'll have six divided by three
divided by one.

So, these simple expressions built up from integers using a division operator.
But, we're writing Haskell programs today, so let's think how do these things
actually get represented as values of our expression data type? So, the first
one is very simple - if we want to represent the value one, we just need to use
the `Val` tag, so write `Val` of one. If we want to have an expression like six
divided by two, well it's a division, so we have a `Div` at the top level, and
then we have two values - we have `Val` six, and `Val` two. And actually, I'll
leave the last one is a little exercise for you here, so you can try this one
for yourself - how do you represent this as a value in Haskell? Well, you're
gonna need two divisions, you're going to need three `Val` constructors, and
then a bunch of brackets.

So, this is the basic idea - we've got simple expressions built up from integers
using division, and we want to think about how do we write a program to evaluate
these expressions? Let's write a program to do that.

So, we're going to write an evaluator, and it's going to be a program, or a
function in this case, that takes an expression as input, and what it's going to
give back is the integer value of that expression. And there's going to be two
cases here, because we have two kinds of expressions. We have a case for values,
and we need to figure out what to do with that, which we'll do in a moment. And
then we have a case for division, and we need to think what to do with that.

So, we've got the skeleton here of a program, and then we just need to fill in
the details. So, how do you evaluate an integer value? Well, that's very simple,
you just give back the number - so if I had `Val` of one, it's value is just
one. And then how do I evaluate a division? Well, these two expressions here,
`x` and `y`, these could be as complicated as you wish. So, we need to evaluate
these recursively. So what we would do, is evaluate the first one, `x`, and that
will give us an integer. And then we'll evaluate the second one, `y`, and that
will give us another integer. And then, all we need to do is divide one by the
other.

So, this is a nice simple program that evaluates these kind of expressions
built up from integers using division - we just have a simple recursive program, two
cases, and everything looks fine.

But there's a problem with this program, and the problem is that it may crash -
because if you divide a number by zero, then that's undefined, so this program
will just crash. So, in particular, if the value of the expression `y` here was
zero, then this division operator would crash, and you get some kind of runtime
error. So we don't want our programs to crash, so we think, what do we do to fix
this problem?

First of all, what we're going to do is we're going to define a safe version of
the division operator, which doesn't crash anymore. Because that's basically the
root of the problem here - division by zero gives an undefined result, and the
program is going to crash. So, let's define a safe version of the division
operator. We're going to define a function called `safediv`, and it's going to
take a couple of integers, and it's going to give back `Maybe` an integer. And
`Maybe` is the way that we deal with things that can possibly fail in Haskell.
So, the type here is not `Int` to `Int` to `Int`, it's `Int` to `Int` to `Maybe
Int`, because division may fail. And we'll see how this `Maybe` type works in a
moment.

So, how do we actually define `safediv`? We take two integers, `n` and `m`,
and then what we'll do is check - is the second of these zero? Because that's
the case when things would go wrong. So, if `m` happened to be zero, then we
will give back the result `Nothing`. Okay, so `Nothing` is one of the
constructors in the `Maybe` type. If `m` is not zero, what we're going to do
is `Just` give back the result of dividing. So, `Just` is another constructor in
the `Maybe` type - `Maybe` only has two constructors, `Nothing`, which
represents things that have gone wrong, or in our case division by zero, and
`Just`, which represent things that have gone fine. In this case, we actually
just get back the result of dividing one number by the other.

So, what we have here now is a safe version of the division operator, which is
explicitly checking for the case when the program would have crashed. So this
doesn't crash anymore, it returns one of two values - either `Nothing` if things
go wrong, or `Just` of the division if things have gone fine. So, what we can do
then, with this safe division operator, is rewrite our little evaluator program
to make sure that it doesn't crash.

So, our new evaluator is going to have a slightly different type than before. So
before, the original program just took an expression as input, and then it gave
back an integer. But that program could crash. The new evaluator takes an
expression as input as before, but now it `Maybe` gives you an integer, because
it could fail, it could have division by zero. So, how do we rewrite this
evaluator?

So, we'll do the two cases again - write down the skeleton, and then we'll fill
in the details. So, in the base case, we can't just return `n` this time,
because we've got to return a `Maybe` value. And there's only two things we
could return, either `Nothing` or `Just`, and in this case the right thing to do
is to return `Just` of `n`, because if you evaluate a value that's always going
to succeed, so we use a success tag, which is `Just`, and then we have the
integer value sitting in here. If we have a division, now we need to do a bit
more work, because when we evaluate `x` that may fail, when we evaluate `y` that
may fail, and then when we do the division that may fail. So, we're going to
need to do a little bit of checking and management of failure.

So, what we're going to do, is when we evaluate a division, first of all, we'll
do a case analysis on the result of evaluating `x`. And that could be one of two
things - it could either be `Nothing`, in which case we're going to do
something, or we could get `Just` of some number, in which case we're going to
do something. So, there's two cases to consider - when we evaluate the first
parameter `x`, either it succeeds or it fails. So in the failure case, if we get
back `Nothing`, the only sensible thing to do is just to say, well if evaluation
of `x` fails, the evaluation of the whole division fails. So we'll just return
`Nothing` as well. In the `Just` case, then we need to evaluate the second
parameter `y`. So, what we're going to do is do another case analysis, we'll do
a case eval of `y`, and then again there's two possible outcomes which we could
have here - either we could have `Nothing`, which means it failed, or we could
have `Just` of `m`, some other number, in which case we've succeeded. Then
again, we need to think what do we do in each of these two cases. So, in the
first case, if the evaluation of `y` fails, the only sensible thing to do is
say, well, we fail as well. In the second case, we've now got to successfully
evaluated expressions - `x` has given the result `n`, `y` has given the result
`m`, and now we can do the safe division. So, in this case we just do `safediv`.

Now we have a working evaluator. We started off with a two-line program, which
kind of did the essence of evaluation, but it didn't check for things going
wrong - it didn't check for a division by zero. Now we've fixed the problem
completely, we have a program which works, this program will never crash, it
will always give a well-defined result, either Nothing or Just, but there's a
bit of a problem with this program, in that it's a bit too long. It's a bit too
verbose, there's quite a lot of noise in here, I can hardly see what's going on
anymore, because it's all of this management of failure.

So, we can look at this program, and think - how can we make this program
better? And how can we make it more like the original program, that didn't work,
but still maintain the fact that this actually does the right thing? And the
idea here, is we're going to observe a common pattern.

So, when you look at this program, you can see quite clearly we're
doing the same thing twice - we're doing two case analyses. What we're doing, is
doing a case analysis on the result of evaluating `x`, and if it's `Nothing` we give
back `Nothing`, and if it's `Just`, we do something with the result. And then we do
exactly the same thing with eval of `y` - we're doing a case analysis on the
result of evaluating `y`, if that gives `Nothing` we give back `Nothing`, and if it's
a `Just`, we do something with it. So, a very common idea in computing is
when you see the same things multiple times, you abstract them out, and have
them as a definition. And that's what we're going to do here.

So, let's draw a little picture first, to capture the pattern which we've seen
twice. So, the pattern we have here, is we're doing a case analysis on
something, so let me just draw as a little box - we don't know what's in there,
we're doing a case analysis on something. And, there's two cases - if it's
`Nothing`, we give back `Nothing`, and if we get `Just` of some value `x`, then
what we're going to do is we're going to process it in some way, we're going to
apply some other function to `x`. So, this is the pattern which we've seen
twice. In the first case, we had eval of `x` sitting here, and in the second
case, we had eval of `y` sitting here, but this is the same pattern that we see
two times in the new evaluator which we've just written.

So, what we can do now, is abstract this out as a definition. And the idea here,
is that we're going to give names to these boxes. So, this box is a `Maybe`
value - it's going to be either `Nothing` or a `Just`, so we'll call it `m`. And
this box is going to be a function, it's going process the result in the case
we're successful, so we'll call this `f`. So, we can turn this picture here into
a definition now, and then we can use it to make our program simpler. So, the
definition we're going to have is, if we have some `Maybe` value, feeding into,
or in sequence with, some function `f`. So, the operator we're defining here is
this funny sequencing symbol, and we'll back to that in a second. What we're
going to do, is a case analysis - we're going to look at what the `Maybe` value
is - if it's `Nothing`, we'll give back `Nothing`, and if it's `Just` of `x`,
we'll apply the function to it. Okay, so we'll just captured the pattern, which
we've seen twice, by a definition now. So, we have some `Maybe` value, then, or in
sequence with, some function `f`, and all we're going to do is look at what the
value of the `Maybe` is - if it's failed, we'll fail, if it succeeds, we pass the
result to the function `f`. It's just the idea of abstracting out a common pattern
as a definition. So, now we can use this definition to make our program simpler.

So, let's rewrite our evaluator once again. The type will remain the same - it
takes in an expression as input, and it's going to give back a `Maybe` value, as
before. But the definition is going to be a bit simpler this time. So, let's
write down the skeleton. So, if we evaluate a value, we're going to do
something. If we evaluate a division, we're going to do something. So, what do
we write in the base case? Well, I could write `Just` of `n` here, but actually
I'm going to abstract that as well - rather than writing `Just` of `n`, I'm
going to write `return` of `n`, so really what I'm making is a little kind of
side definition, that says `return` of `x` is the same as `Just` of `x`. And
then, what are we doing in the division case? Well, we're going to do an
evaluation first - we're going to evaluate `x`, and then if that's successful,
using our little sequencing operator, we're going to feed the result into a
function. So that function is going to take the result, `n`, that comes from
evaluating that, and then it's going to evaluate `y`. So, if we do eval of `y`,
if that's successful, we're going to feed that result into a function. And here
again, I'm using the lambda notation, which we did a video about previously, you
can have a look back at that. So, if these two things are both successful, we'll
have two values, `n` and `m`, and then all we do is call `safediv` with them,
then close the brackets. So, this program here is equivalent to the program
which we wrote, which had all the nested case analyses. But, that's all been
abstracted away now - it's all been kind of abstracted into `return`, and the
sequencing, and `safediv`.

So, this is a nicer program now, but still I'm not entirely happy with this.
There's still some complexity in there - we're still using the funny lambda
notation, we're still using this funny symbol, which we've introduced. Maybe I
can make it even simpler? So, what a language like Haskell gives you, is a
special notation for writing programs which have this kind of form. And this is
called the `do` notation.

So let me write this in `do` notation, and then we'll come back to what this has
all got to do with monads. So, let's write this program in an even more simple
form, and this will be our final program. We take an expression as input, and
it's going to `Maybe` deliver us an integer. And the base case will not change, so
we'll get return of `n`. But the recursive case is going to become a bit simpler,
because we use the `do` notation as a shorthand for using the sequencing operator
which we've introduced. So, I can say, if I evaluate a division, what I'm going
to do, and this is the keyword, which just gives you a shorthand for exactly
what we've just written, it's not anything special, it's just shorthand, just
syntactic sugar. What we're going to do, is take the result `n`, from the result
of evaluating `x`, if it's successful. Then, we'll take the result `m`, from the
result of evaluating `y`, if that's successful. And then, we will call
`safediv`. And this is our final program, and I'm much happier with this one. I
mean, it looks kind of similar to the original program, a similar level of
complexity, but all the failure management is now handled for us automatically.
The failure is happening behind the scenes with the `do` notation, and with
`safediv`, but we don't need to see that when we're reading this program. This
is a much nicer program than the last one, because we've kind of abstracted away
from a lot of the detail.

So, you can look
at a program like this, and I've hardly mentioned the word monads in the last
ten minutes, you can say what's this actually got to do with monads? Well, what
we've actually done, is we've rediscovered what's
known as the `Maybe` monad. The `Maybe` monad is three things -
it's the `Maybe` type, or really the `Maybe` type constructor, because it takes a
parameter. So you can have `Maybe` of an integer, or maybe of a Boolean, or maybe of
whatever you like. And then it's two functions - it's the function called
`return`, and it's the sequencing operator which we introduced. And we can think
about what are the types of these things? So what `return` does, is it takes a thing
of any old type, `a` - could be an integer, could be a Boolean, could be whatever you
like. And it converts it into a `Maybe` value. So, in our case, this just took an
integer like five, and we return `Just` of five. Okay, so that's all the `return` was
doing, it's basically just applying `Just`.

And what it gives you, is a bridge between the pure world of values here, and
the impure world of things that could go wrong - so it's a bridge from pure to
impure, if you like. And what sequencing does, is it gives you a way of
sequencing things - so you give it something which can fail, a `Maybe<a>`, and
then you give it a function that tells you what to do with that `a`, if you
succeed - so an `a` to `Maybe<b>`. And then, finally, what you're going to get
back is a `Maybe<b>`. Okay, and this is all that a monad is essentially - a
monad is some kind of type constructor, like `Maybe`, or `List`, or something
else, as there's many other examples, together with two functions that have
these types here. So, what we've essentially done is rediscovered what's called
the `Maybe` monad.

What's the point of all of this? I mean, what's the point? We seem to have gone
through quite a lot of steps, to write in the end quite a simple program. What
was the actual point here? So there's four points which I would like to
emphasize here.

So, the first point, is that the same idea we've seen works for other effects as
well - it's not specific to `Maybe`, which captures failure. The same idea
captures other kinds, or you can use with, other kinds of effects like
input/output, like mutable state, like reading from environments, like writing
to log files, non-determinism. All sorts of other things which you think of as
being effects in programming languages fit exactly the same pattern. So, monads
kind of give you a uniform framework for thinking about programming with
effects.

Another important point is that it supports
pure programming with effects. I mean, Haskell is a pure
language - functions just take inputs, and produce outputs, they don't have any kind
of side effects at all. But you need to have side effects to write real
programs. So, what monads give you is a way of doing impure things, like proper
side effects, like input/output, in a pure programming language like Haskell.

Another important point here, is that the use of the effects is explicit in the
types. When I wrote the evaluator which didn't fail, it took an expression as
input, and it delivered `Maybe` of an integer. So, the `Maybe` in the type is
telling me that this program may fail. So, this is the idea of being explicit
about what kind of effects, or side effects, that your programs can have in the
types. And this is a very, very powerful idea.

And the last thing is, it's a little bit strange, but it's particularly
interesting, it's the idea of writing functions that work for any effect - we
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
plug - I have a new book which came out fairly recently, Programming in Haskell,
and this has got a chapter specifically about this, which goes into much more
detail. I've only really touched on the surface, there's lots of things I didn't
say, which maybe you need to know to write real programs using this stuff. So,
you could have a look in the book to find out more about that.

This is an interesting point, it causes quite quite some problems for people
learning languages like Haskell, because Haskell people tend to use the proper
mathematical terms for things, and those terms are often quite foreign to
programmers. And it does cause quite a lot of difficulty - so there's some
people have the view that we shouldn't actually have used the term monad, maybe
we should have called them effects, or something like that. So, just use the
more kind of human, or a familiar term. But it is an issue.

But I'm actually of the point of view that, if we know the proper term for
something, we should call it that something, and the people who are using it
should just learn that term. I mean, it's what it is, it's a monad, and we
should kind of pay homage to the mathematicians for discovering this idea first,
and not kind of reappropriate it as if it was discovered independently - the
mathematicians discovered this, they should get credit for that, and so I'm
quite happy with the word monad. But, it does cause some problems when people
are learning programming languages, because it does sound a bit scary, and
there's lots more scary terms like this in programming as well. This is all
built into languages like Haskell.

So, there's lots of libraries for programming with monadic things - you don't
need to define a lot of the infrastructure, like `Maybe`, and `return`, and the
sequencing, for yourself - this is kind of built in as libraries. You can define
your own ones if you want to, but there's maybe kind of fifteen or twenty monads
which are just lying around waiting for people to use. And if you want to use
multiple different monads in your programs, maybe you need two different kinds
of effects, maybe you need things that can fail, and you need some state,
there's ways of coping with that kind of stuff as well. So, you don't need to do
all yourself, it's mostly built in for you.

