---
layout: post
title: "Not Completely Linear Regression"
summary: "Learning a linear relationship from <em>multiple</em> inputs to one output."
date:   2018-06-04 20:57:00
---

In [simple linear regression](/2018/06/01/linear-regression) the computer
learns a linear relationship between a single input $$ x $$ and a single output
$$ y $$ by calculating two values $$\theta_0$$ and $$\theta_1$$. These values
define a line that best fits the training examples $$(x^{(1)}, y^{(1)}), (x^{(2)}, y^{(2)}), \dots, (x^{(m)}, y^{(m)}) $$.

<span id="multivariate-linear-regression">**Multivariate linear
regression**</span> is an extension that finds a relationship between
_multiple_ inputs $$ x_1, x_2, \dots, x_n $$ and an output. We say that the
input is "$$n$$ dimensional." The computer calculates $$n + 1$$ values
$$\theta_0, \theta_1, ..., \theta_n$$. These values define a plane (if $$ n = 2
$$) or _hyperplane_ (if $$ n > 2 $$) that best fits the training examples.

To handle the multiplicity of variables and values, it is convenient to use
matrices. 

Let \\( \vec{\theta} = \\) \`[[\theta_0], [\theta_1], [\vdots], [\theta_n]]\`.
Its transpose $$ \vec{\theta}^T = $$ \`[\theta_0, \theta_1, ..., \theta_n]\`

Let the inputs be represented as $$ \vec{x} = $$ \`[[x_0 = 1], [x_1], [\vdots], [x_n]]\`. (Below you'll see why we set $$ x_0 = 1$$.) 

Instead of $$ y(x) = \theta_0  + \theta_1x $$ as for simple linear
regression, we use the rules of [matrix
multiplication <i class="fa fa-external-link-alt"></i>](https://en.wikipedia.org/wiki/Matrix_multiplication#Definition) to get the model equation:

$$ y(\vec{x}) = \vec{\theta}^T \times \vec{x} = \theta_0 + \theta_1x_1 + \theta_2x_2 + \dots + \theta_nx_n $$

The cost function can also be expressed using matrix notation:

$$ J(\vec{\theta}) = \sum_{i=1}^m{\frac{1}{2}(\vec{\theta}^T \times \vec{x} - y^{(i)})^2} $$

The partial derivatives are as follows:

$$ \frac{\partial J(\vec{\theta})}{\partial \theta_0} = \sum_{i=1}^m(\vec{\theta}^T \times \vec{x} - y^{(i)})$$

$$ \frac{\partial J(\vec{\theta})}{\partial \theta_1} = \sum_{i=1}^m(\vec{\theta}^T \times \vec{x} - y^{(i)})x_1^{(i)}$$

$$ \frac{\partial J(\vec{\theta})}{\partial \theta_2} = \sum_{i=1}^m(\vec{\theta}^T \times \vec{x} - y^{(i)})x_2^{(i)}$$

$$ \vdots $$

$$ \frac{\partial J(\vec{\theta})}{\partial \theta_n} = \sum_{i=1}^m(\vec{\theta}^T \times \vec{x} - y^{(i)})x_n^{(i)}$$

The model equation, cost function, and its partial derivatives should look familiar. In the special case where $$n = 1$$ they are exactly the equations for simple linear regression.
