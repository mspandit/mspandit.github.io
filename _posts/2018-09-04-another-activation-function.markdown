---
layout: post
title: "Another Activation Function"
summary: "The <em>rectified linear</em> function avoids two problems of the logistic/sigmoid activation function."
date:   2018-09-04 16:37:00
---

The [logistic or sigmoid
function](/2018/06/07/almost-entirely-nonlinear-regression) maps any input to a
value between 0 and 1. This property makes it a suitable [activation
function](/2018/07/04/neural-networks#activation-functions) for the output
layer of a deep neural network that is performing a classification task. Its
value can be interpreted as the probability of the input being in a class.

One problem with the logistic function is that _the slope of its tangent
approaches zero for large values, either positive or negative._ If, during
initialization or training, a neuron's parameters $$\vec{\theta}$$ happen to
generate large values as input to its logistic activation function, then the
partial derivatives of the composition function will be near zero. During
stochastic gradient descent, the changes to the parameters are directly
proportional to the partial derivatives. If the partial derivatives are near
zero, then the parameters will get "frozen" and the neuron will stop learning.
This is known as the **vanishing gradient** problem.

The [**rectified
linear** <i class="fa
fa-external-link-alt" title="(External link)"></i>](https://en.wikipedia.org/wiki/Rectifier_(neural_networks)) function
is an alternative activation function that is suitable for the hidden layers of
a deep neural network. Its equation is

$$f(x) = max(0, x)$$

It should be clear that the output of this function is exactly
* the same as its input when the input is greater than zero, and 
* 0 otherwise. 

The derivative of this function (the slope of its tangent) is exactly
* 1 when its input is greater than zero and 
* 0 otherwise. 

A hidden layer neuron having this activation function avoids the vanishing
gradient problem as long as its parameters generate positive values. As soon
as the parameters generate negative values, however, they stop changing, and
the neuron outputs 0, effectively ignoring its inputs. The neuron then
contributes to [sparseness](/2018/06/23/overfitting-regularization#sparse) of
the network. It simplifies the model by eliminating the contribution of certain
features, and thereby avoids the problem of overfitting.

A neuron having this activation function is commonly called a _rectified linear
unit_ or "relu."