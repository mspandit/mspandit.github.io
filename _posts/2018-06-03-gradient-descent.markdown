---
layout: post
title: "Gradient Descent"
summary: "A standard, iterative method for minimizing the cost function."
date:   2018-06-03 07:43:00
---

For [simple linear regression](/2018/06/01/linear-regression), it is possible
to minimize the [cost function](/2018/06/01/linear-regression#cost-function) by
setting its partial derivative equations to zero and then solving for the
variables $$\theta_0$$ and $$\theta_1$$.

In modern machine learning, the computer learns vastly more complex, non-linear
models. (You'll encounter them later.) These models sometimes describe the
relationships between _millions_ of inputs and _thousands_ of outputs. To learn
such models, we can still define a cost function and find its partial
derivative equations. However, setting them to zero and solving for the
variables may be impossible or excessively time-consuming.

The alternative method to minimize the cost function is **gradient descent**.

1. <span id='step1'>We start with some (possibly random) values for the variables.</span>

2. We calculate the _partial derivatives_ of the cost function using those values.
These values are called **gradients** because each is the rate of change (slope
of the tangent) of the cost function based on the change in one variable.

1. We adjust each variable value by an amount _directly proportional to its
corresponding gradient._ (Of course, if the gradient is zero, then the variable
is already "doing its part" to minimize the cost function, and we need not
change its value.) The [constant of
proportionality <i class="fa fa-external-link-alt"></i>](https://en.wikipedia.org/wiki/Proportionality_(mathematics))
is called the **learning rate**.

1. We repeat steps 2. and 3. until _all_ the gradients are zero (or very close
to it). When this happens, we loosely say that "the model has converged." This
really means we have arrived at a set of values that minimize the cost function
for the training set.

If you tried to minimize the linear regression cost function
[interactively](/2018/06/01/interactive-minimization),
you already have a good sense for gradient descent. You may have moved the
sliders rapidly until the line came close to the data set. During this time,
the cost function decreased rapidly. Then, could make fine adjustments,
paying close attention to the value of $$J(\theta_1, \theta_2)$$.
