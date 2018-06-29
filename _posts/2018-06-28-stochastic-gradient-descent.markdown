---
layout: post
title: "Stochastic and Mini-Batch Gradient Descent"
summary: "The cost function for stochastic gradient descent (SGD) considers the cost of a <em>single</em> example, randomly-chosen. Mini-batch gradient descent considers a fraction of the examples."
date:   2018-06-28 15:06:00
---

The logistic regression [cost
function](/2018/06/09/logistic-regression-cost-function) we have been using
considers _all_ the examples in the training set. However, certain problems may
present you with a very large number of training examples, each of which may
be very large in size. In such cases, computer memory limitations may render
infeasible the calculation of this cost function.

An alternative is **stochastic gradient descent (SGD).** Here, the cost is
calculated on the basis of a _single_ example $$(x^{(1)}, y^{(1)})$$ chosen at
random from the training set:

$$ J(\theta_0, \theta_1) = -\bigg[y^{(1)}ln(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(1)}}}) + (1 - y^{(1)})ln(1 - \frac{1}{1 + e^{\theta_0 + \theta_1x^{(1)}}})\bigg] $$

$$ \frac{\partial J(\theta_0, \theta_1)}{\partial \theta_1} =  (\frac{1}{1 + e^{\theta_0 + \theta_1x^{(1)}}} - y^{(1)})x^{(1)}$$

Although SGD relieves the memory and computational demands of the cost
function, it essentially uses a slightly different cost function at every
iteration. Consequently, the cost of the model on the whole training set may
fluctuate during gradient descent, and more iterations will be required before
the best-fitting model is found.

Furthermore, modern computer processors have instructions and caches that allow
calculations on multiple examples at nearly the same speed as on a single
example.

A more general alternative is **mini-batch gradient descent.** Here, the cost
is calculated on the basis of $$b$$ examples $$(x^{(1)}, y^{(1)}), (x^{(2)},
y^{(2)}), \dots, (x^{(b)}, y^{(b)})$$ chosen at random from the training set:

$$ J(\theta_0, \theta_1) = -\frac{1}{b}\bigg[\sum_{i=1}^{b}{y^{(i)}ln(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}}) + (1 - y^{(i)})ln(1 - \frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}})}\bigg] $$

$$ \frac{\partial J(\theta_0, \theta_1)}{\partial \theta_1} =  \sum_{i=1}^b{(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}} - y^{(i)})x^{(i)}}$$

($$b < m$$, the total number of examples.) Mini-batch gradient descent allows
you to tune the batch size $$b$$ for optimal use of processor instructions and
caches, without being excessively demanding on memory.