---
layout: post
title: "Even Less Linear Regression"
summary: "Learning a <em>polynomial</em> relationship between multiple inputs and an output."
date:   2018-06-06 14:10:00
---

In [simple linear regression](/2018/06/01/linear-regression) the computer
learns a linear relationship between a single input $$ x $$ and a single output
$$ y $$ by calculating two values $$\theta_0$$ and $$\theta_1$$. These values
define a _line_ that best fits the training examples.

<span id="polynomial-regression">**Polynomial regression**</span> finds a
_non-linear_ relationship between an input and the output. The model equation for polynomial regression contains terms that raise the
input value to various powers. For example:

$$ y(x) = \theta_0 + \theta_1x + \theta_2x^2 + \theta_3x^3 + \dots $$

The computer calculates values $$\theta_0, \theta_1, ...,$$. These coefficients
define a curve that best fits the training examples.

In the multiple-dimensional input case, the model equation looks the same.
However, $$ \vec{x} $$ includes inputs raised to various powers as well as
actual inputs.

$$ y(\vec{x}) = \vec{\theta}^T \times \vec{x} $$

In this case, we refer to $$ \vec{x} $$ as a **feature vector** because it
consists of actual inputs as well as "features" of the inputs.

You may be wondering: Which inputs are raised to which powers? This is a
matter of discretion and experimentation. If you know that the output depends
on an input raised to a power, you should use it. However, the more features
you include, the more iterations your model will require to converge.

The cost function and its partial derivatives are similar to those for
[multivariate linear regression](/2018/06/04/not-completely-linear-regression):

$$ J(\vec{\theta}) = \sum_{i=1}^m{\frac{1}{2}(\vec{\theta}^T \times \vec{x} - y^{(i)})^2} $$

$$ \frac{\partial J(\vec{\theta})}{\partial \theta_n} = \sum_{i=1}^m(\vec{\theta}^T \times \vec{x} - y^{(i)})x_n^{(i)}$$

Therefore, [gradient descent](/2018/06/03/gradient-descent) can be used to find
the best-fit surface.

# Overfitting

You can start with a linear model and gradually add features to $$ \vec{x} $$
and dimensions to $$ \vec{\theta} $$ until you get the desired fit.

If you include a large number of features, you are likely to encounter the
problem of **overfitting**. The model fits the training data well, but gives
poor or incorrect outputs when fed inputs outside the training data. For this
reason, when given a data set, it is best not to use the entire set for
training. Instead, reserve a portion of it (called the **test data**) for
testing the model after it has been trained. Later, we will look at a couple of
methods for preventing overfitting.
