---
layout: post
title: "Overfitting and Regularization"
summary: "Regularization reduces the complexity of the model to help it generalize."
date:   2018-06-23 08:10:00
---

We introduced [polynomial
regression](/2018/06/06/even-less-linear-regression#polynomial-regression) as a
way of finding a curve that best fits the training examples. We combined it
with logistic regression, in the [Python](/2018/06/14/logistic-regression-python) and [Julia](/2018/06/22/logistic-regression-julia) programs, to create a curved
boundary between examples in the class and those outside the class.

# Detecting Overfitting

In practice, we are given a data set and asked to find a model that fits it. We
_detect_ overfitting by separating a [testing
set](/2018/06/06/even-less-linear-regression#testing-set) of data apart from
the training set. During gradient descent, only the training set is used in the
cost function. After the $$\theta_i$$ have been found that minimize the cost on
the training set, we check that model's cost on the testing set. If the testing
set cost is significantly higher than the training set cost, then we know
overfitting has occurred.

# Avoiding Overfitting

One way to _avoid_ overfitting is to create a preference for simpler models,
and one way to simplify a model is to eliminate the contribution of certain
features. However, we may not know in advance which features are unimportant.
Furthermore, it may be that their contribution should be diminished, but not
eliminated. Therefore, instead of taking values out of the feature vector
entirely, we try reducing $$\theta_i$$. We "penalize" models having large
$$\theta_i$$ values by adding a term to the logistic regression [cost function](/2018/06/09/logistic-regression-cost-function):

$$ J(\theta_0, \theta_1) = -\frac{1}{m}\bigg[\sum_{i=1}^{m}{y^{(i)}ln(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}}) + (1 - y^{(i)})ln(1 - \frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}})}\bigg] + \lambda\theta_1^2$$

or the linear regression [cost function](/2018/06/01/linear-regression):

$$ \frac{1}{2}\sum_{i=1}^m{(\theta_0 + \theta_1x^{(i)}- y^{(i)})^2} + \lambda\theta_1^2$$

In the general case, where $$\theta_i$$ are are polynomial coefficients, we say
that the resulting $$\vec{\theta}$$ is made **sparse** because it contains more
values that are zero (or close to zero), thereby eliminating (or diminishing)
the contribution of a feature to a model. $$\lambda$$ is a parameter that
influences how simple the resulting model should become.
