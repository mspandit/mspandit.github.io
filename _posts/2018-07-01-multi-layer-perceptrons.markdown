---
layout: post
title: "Multi-Layer Perceptrons"
summary: "Multi-layer perceptrons approach the multivariate logistic regression
problem by learning the appropriate features at the same time as their
coefficients."
date:   2018-07-01 08:55:00
---

In the [previous](/2018/06/29/simple-computer-vision-python)
[posts](/2018/07/01/simple-computer-vision-julia), we used a simple linear
logistic model to perform a computer vision task with 91% accuracy or better.
It was _linear_ because it used the raw inputs, not their products or powers.
It was _logistic,_ because it composed a linear model with the [logistic
function](/2018/06/07/almost-entirely-nonlinear-regression) to classify the
input vector. 

One way to improve the accuracy of the program is to assume a more complex
model, for example a [polynomial](/2018/06/06/even-less-linear-regression)
logistic model. However, in complex problems like computer vision or speech
recognition, there may be hundreds or even millions of input variables. (For
example, smartphone cameras routinely capture 2.8 million pixels, each of which
is a combination of red, green, and blue values.) For such problems, generating
a complete polynomial feature vector (including all possible products of input
variables and their powers) is intractable. And this is before even starting to
calculate coefficients $$\vec{\theta}$$ for each input and feature.

**Multi-layer perceptrons** approach the multivariate logistic regression
problem by _learning the appropriate features at the same time as their
coefficients $$\vec{\theta}$$._ By "appropriate features" we mean functions of
the raw inputs---whether their powers, their products, or for that matter,
anything else.

The logistic regression model function used a vector $$\vec{\theta}$$ which
contained the coefficients of the input variables. We can illustrate it as
follows:

<img src="https://docs.google.com/drawings/d/e/2PACX-1vRAIYaNVeUlLxQGnQBjES2GiQZzdb_EOuaXBvb_HBdpVK2-IVGLzMlkUeeFQ25z26vrv7fx3i16jnpG/pub?w=318&amp;h=456">

Here is how the multilayer perceptron works: the raw input is "classified" by
numerous logistic regression models. Each determines whether the input exhibits
a particular feature or not. (Because we expect the input to exhibit multiple
features, we use the logistic function, not softmax, for each model.) The parameters of each model determine which feature that model detects.

Those features are then classified by a multiclass logistic regression model.
This model determines which distinct class the combination of features is in.
(Because we expect the input to be in a single class, we use the softmax
function for this classifier. This gives us a probability distribution across
classes.) This is illustrated as follows:

<img src="https://docs.google.com/drawings/d/e/2PACX-1vSOpMlgbcxengmHbgpbimSn_u3hb_prXJ40chZAT6X0m_z3qwOqBtXEnHdVofft4cdkYPDB8KBHD993/pub?w=525&amp;h=565">

Note that the multilayer perceptron is composed of logistic and multiclass
logistic models. Therefore _the cost function remains differentiable by all
parameters._ This allows us to use gradient descent to find the parameters that
minimize it.
