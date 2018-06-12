---
layout: post
title: "A Better Cost Function for Logistic Regression"
summary: "A cost function for logistic regression that works with gradient descent."
date:   2018-06-09 08:56:00
---

We [can't use](/2018/06/08/cost-function-visualization) the same cost function
for [logistic regression](/2018/06/07/almost-entirely-nonlinear-regression) as
for [linear regression](/2018/06/01/linear-regression). To find a better cost
function, we'll exploit the fact that the model output approaches 0 or 1 and
the outputs in the training set are always either 0 (indicating the input is
not in the class) or 1 (indicating the input is in the class). We want a cost
function with the following properties:

1. If the model output is near the training output, the cost should near 0.

2. If the model output is near 1 when the training output is 0, the cost should be very large.

3. If the model output is near 0 when the training output is 1, the cost should be equally large.

The following cost function has all three of these properties. It looks quite
long, but you can see that the left addend becomes zero when the training
output is zero and the right addend becomes zero when the training output is 1.

$$ J(\theta_0, \theta_1) = -\frac{1}{m}\bigg[\sum_{i=1}^{m}{y^{(i)}ln(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}}) + (1 - y^{(i)})ln(1 - \frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}})}\bigg] $$

$$ \frac{\partial J(\theta_0, \theta_1)}{\partial \theta_0} =  \sum_{i=1}^m{(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}} - y^{(i)})}$$


$$ \frac{\partial J(\theta_0, \theta_1)}{\partial \theta_1} =  \sum_{i=1}^m{(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}} - y^{(i)})x^{(i)}}$$