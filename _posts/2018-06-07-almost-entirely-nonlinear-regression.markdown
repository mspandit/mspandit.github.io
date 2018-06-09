---
layout: post
title: "Almost Entirely Nonlinear Regression"
summary: "Logistic regression can be used for <em>classification</em> because it learns a nonlinear relationship between input and output."
date:   2018-06-07 21:46:00
---

Many useful problems involve determining whether an input is the member of a
class or not, for example,

* Given an e-mail, is it spam or not spam?

* Given a credit card transaction, is it fraudulent or legitimate?

* Given medical test results, are they positive or negative for a disease?

For most such problems, neither a [linear](/2018/06/01/linear-regression) nor a
[polynomial](/2018/06/06/even-less-linear-regression) model fits the data very
well. One reason is that these models can produce large, continuous-valued,
positive or negative outputs. The desire is for a _binary_ output (0 for
not-in-class or 1 for in-class).

One recourse is to take the output of a linear or polynomial model $$ y =
\vec{\theta} \times \vec{x} $$ and use it as the input to _another_ model with
output ranging between 0 and 1. The [logistic function <i class="fa
fa-external-link-alt"></i>](https://en.wikipedia.org/wiki/Logistic_function)
has this property: no matter how large or small its input is, the output
remains between 0 and 1.

$$ y = \frac{1}{1 + e^{\vec{\theta}\times\vec{x}}} $$

Mathematically speaking, this [composes <i class="fa
fa-external-link-alt"></i>](https://en.wikipedia.org/wiki/Function_composition)
a logistic function with a linear or polynomial function. Data scientists
sometimes say the linear/polynomial model's output is "put through a sigmoid,"
or "squashed." The output of such a model is not strictly binary, but because
it is between 0 and 1, we can usefully interpret it as the _predicted
probability that the input is in a particular class._

The [linear regression](/2018/06/01/linear-regression) model assumed that there
was a line such that the examples were on the line or near it. [Polynomial
regression](/2018/06/06/even-less-linear-regression) assumed that there was a
curve such that the examples were on the curve or near it. Logistic regression
assumes that there is a line or curve such that _examples on one side of the
line or curve are in the class, and examples on the other side are outside the
class._
