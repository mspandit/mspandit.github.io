---
layout: post
title: "Simple Linear Regression"
summary: "Simple linear regression is one of the simplest forms of supervised machine learning."
date:   2018-06-01 18:02:00
---

<style type="text/css" media="print">
  
  @media print {
    a[href]:after {
      content: none;
    }
  }
  
</style>

In one of the simplest forms of
[supervised](/2018/05/31/introduction-machine-learning) machine learning, the
computer learns a linear relationship between a single input and its
corresponding continuous-valued output. The training data consists of $$m$$
input examples $${ x^{(1)}, x^{(2)}, ..., x^{(m)} }$$ and their corresponding output values,
$${ y^{(1)}, y^{(2)}, ..., y^{(m)} }$$. [**Simple linear
regression** <i class="fa fa-external-link-alt" aria-hidden="true"></i>](https://en.wikipedia.org/wiki/Simple_linear_regression) means
finding the line that "best fits" the training examples---such that the _sum of
the distances from each example to the line is minimized._ This line is a
**model** that can then be used to generate outputs for new inputs.

The [equation of any line <i class="fa fa-external-link-alt" aria-hidden="true"></i>](https://en.wikipedia.org/wiki/Linear_equation) can
be written as $$ y(x) = \theta_0 + \theta_1x $$ where $$\theta_1$$ is the slope
of the line and $$\theta_0$$ is its y-intercept. The actual distance from a
point $$(x^{(i)}, y^{(i)})$$ to a line is [fairly
complex <i class="fa fa-external-link-alt" aria-hidden="true"></i>](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_an_equation). 
Fortunately, we can minimize this distance by minimizing _half the square of
its vertical component_ $$\frac{1}{2}(y(x^{(i)}) - y^{(i)})^2$$. (You'll see why in a
moment.) For a line specified by $$\theta_0$$ and $$\theta_1$$, we want to
minimize:

$$ J(\theta_0, \theta_1) = \sum_{i=1}^m{\frac{1}{2}(y(x^{(i)}) - y^{(i)})^2} = \frac{1}{2}\sum_{i=1}^m{(\theta_0 + \theta_1x^{(i)}- y^{(i)})^2} $$

Such a function is called the <span id='cost-function'>**cost**</span> or
**loss** function. Its value is minimized for the best-fit model.
How do we find $$\theta_0$$ and $$\theta_1$$ that minimize this function? By [finding the zeroes of its partial
derivatives <i class="fa fa-external-link-alt" aria-hidden="true"></i>](https://en.wikipedia.org/wiki/Fermat%27s_theorem_(stationary_points)#Statement) 
with respect to those variables.

(We used half the square of the vertical distance precisely to simplify the
partial derivative equations. The term "partial derivative" may sound daunting,
but it just calculates how rapidly one variable makes the function change, when
the other variable is held constant. Near the point where both partial
derivatives are zero, neither variable is affecting the function's value. This
tells us the function is at its minimum.)

The partial derivative with respect to $$\theta_1$$ is simply

$$ \frac{\partial J(\theta_0, \theta_1)}{\partial \theta_1} = \sum_{i=1}^m({\theta_0  + \theta_1x^{(i)} - y^{(i)}})x^{(i)}$$

The partial derivative with respect to $$\theta_0$$ is simply

$$ \frac{\partial J(\theta_0, \theta_1)}{\partial \theta_0} = \sum_{i=1}^m{(\theta_0 + \theta_1x^{(i)} - y^{(i)})} $$

For simple linear regression, it is possible to set these equations to zero and
solve for $$\theta_0$$ and $$\theta_1$$. To learn more complex models, we must
take a different approach called [_gradient descent_](/2018/06/03/gradient-descent).

# Summary

Click the arrows to see different ways of expressing the same thing:
<table class="table">
  <tr>
    <td style="width: 10%; text-align: center;">
      <a class="btn btn-default" id="left"><i class="fa fa-angle-left"></i></a>
    </td>
    <td style="width: 80%; text-align: center;">
      <div class="frame" id="frame-0" style="display: none;">the line that “best fits” the training examples</div>
      <div class="frame" id="frame-1" style="display: none;">the line such that the sum of the distances from each example to the line is
      minimized</div>
      <div class="frame" id="frame-2" style="display: none;">the y-intercept \(\theta_0\) and slope \(\theta_1\) such that the sum of the
      distances from each example to \( y(x) = \theta_0 + \theta_1x \) is minimized</div>
      <div class="frame" id="frame-3" style="display: none;">the y-intercept \(\theta_0\) and slope \(\theta_1\) such that the sum of the
      distances from \((x^{(1)}, y^{(1)}), (x^{(2)}, y^{(2)}), \dots, (x^{(m)}, y^{(m)})\) to \( y(x) = \theta_0 + \theta_1x \) is minimized</div>
      <div class="frame" id="frame-4" style="display: none;">\( \theta_0 \) and \(\theta_1\) such that the sum of the <em>vertical</em> distances from
      \((x^{(1)}, y^{(1)}), (x^{(2)}, y^{(2)}), \dots, (x^{(m)}, y^{(m)})\) to \( y(x) = \theta_0 + \theta_1x \) is minimized</div>
      <div class="frame" id="frame-5" style="display: none;">\(\theta_0\) and \(\theta_1\) such that \(\sum_{i=1}^m{(y(x^{(i)}) - y^{(i)})}\) is minimized</div>
      <div class="frame" id="frame-6" style="display: none;">\(\theta_0\) and \(\theta_1\) such that \(\sum_{i=1}^m{\frac{1}{2}(y(x^{(i)}) - y^{(i)})^2}\) is minimized.</div>
      <div class="frame" id="frame-7" style="display: none;">\(\theta_0\) and \(\theta_1\) such that \(\frac{1}{2}\sum_{i=1}^m{(\theta_0 + \theta_1x^{(i)}- y^{(i)})^2} \) is minimized</div>
      <div class="frame" id="frame-8" style="display: none;">\(\theta_0\) and \(\theta_1\) such that \(\frac{\partial}{\partial \theta_0}\frac{1}{2}\sum_{i=1}^m{(\theta_0 + \theta_1x^{(i)}- y^{(i)})^2} = 0 \) and \(\frac{\partial}{\partial \theta_1}\frac{1}{2}\sum_{i=1}^m{(\theta_0 + \theta_1x^{(i)}- y^{(i)})^2} = 0\)</div>
      <div class="frame" id="frame-9" style="display: none;">\(\theta_0\) and \(\theta_1\) such that \(\sum_{i=1}^m{(\theta_0 + \theta_1x^{(i)} - y^{(i)})} = 0\) and \(\sum_{i=1}^m({\theta_0  + \theta_1x^{(i)} - y^{(i)}})x^{(i)} = 0 \)</div>
    </td>
    <td style="width: 10%; text-align: center;">
      <a class="btn btn-default" id="right"><i class="fa   fa-angle-right"></i></a>
    </td>
  </tr>
</table>
<script src="/js/mathpres.js"></script>
<script type="text/javascript">
  $(function () {
    mp = new mathPres();
  });
</script>


