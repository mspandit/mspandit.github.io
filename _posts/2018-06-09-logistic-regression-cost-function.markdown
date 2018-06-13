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
output $$ y^{(i)} = 0 $$ and the right addend becomes zero when $$ y^{(i)} = 1 $$.

$$ J(\theta_0, \theta_1) = -\frac{1}{m}\bigg[\sum_{i=1}^{m}{y^{(i)}ln(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}}) + (1 - y^{(i)})ln(1 - \frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}})}\bigg] $$

$$ \frac{\partial J(\theta_0, \theta_1)}{\partial \theta_0} =  \sum_{i=1}^m{(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}} - y^{(i)})}$$


$$ \frac{\partial J(\theta_0, \theta_1)}{\partial \theta_1} =  \sum_{i=1}^m{(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}} - y^{(i)})x^{(i)}}$$


# Summary

Click the arrows to see different ways of expressing the same thing:
<table class="table">
  <tr>
    <td style="width: 10%; text-align: center;">
      <a class="btn btn-default" id="left"><i class="fa fa-angle-left"></i></a>
    </td>
    <td style="width: 80%; text-align: center;">
      <div class="frame" id="frame-0" style="display: none;">the curve that "best classifies" the training examples</div>
      <div class="frame" id="frame-1" style="display: none;">the curve that "best fits" training examples that are in a class or not</div>
      <div class="frame" id="frame-2" style="display: none;">the sigmoid curve that "best fits" training examples whose \(y^{(i)}\) values are 1 or 0</div>
      <div class="frame" id="frame-3" style="display: none;">the parameters \( \theta_0 \) and \( \theta_1 \) that minimize the distances from the examples to  $$y = \frac{1}{1 + e^{\theta_0 + \theta_1x}}$$</div>
      <div class="frame" id="frame-4" style="display: none;">the parameters \( \theta_0 \) and \( \theta_1 \) that minimize the <em>vertical distances</em> from the examples to  $$y = \frac{1}{1 + e^{\theta_0 + \theta_1x}}$$</div>
      <div class="frame" id="frame-5" style="display: none;">the parameters \( \theta_0 \) and \( \theta_1 \) that minimize  $$| y^{(i)} - \frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}} |$$ for examples \((x^{(1)}, y^{(1)}), (x^{(2)}, y^{(2)}), ..., (x^{(m)}, y^{(m)})\)</div>
      <div class="frame" id="frame-6" style="display: none;">the parameters \( \theta_0 \) and \( \theta_1 \) that minimize  $$ \frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}}$$ when \(y^{(i)} = 0 \) and minimize $$ 1 - \frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}} $$ when \(y^{(i)} = 0 \) for examples \((x^{(1)}, y^{(1)}), (x^{(2)}, y^{(2)}), ..., (x^{(m)}, y^{(m)})\) </div>
      <div class="frame" id="frame-7" style="display: none;">the parameters \( \theta_0 \) and \( \theta_1 \) that minimize  $$ -ln(1 - \frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}})$$ when \(y^{(i)} = 0 \) and minimize $$ -ln(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}}) $$ when \(y^{(i)} = 0 \) for examples \((x^{(1)}, y^{(1)}), (x^{(2)}, y^{(2)}), ..., (x^{(m)}, y^{(m)})\) </div>
      <div class="frame" id="frame-8" style="display: none;">the parameters \( \theta_0 \) and \( \theta_1 \) that minimize  $$ -(1 - y^{(i)})ln(1 - \frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}}) -y^{(i)}ln(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}}) $$ for examples \((x^{(1)}, y^{(1)}), (x^{(2)}, y^{(2)}), ..., (x^{(m)}, y^{(m)})\) </div>
      <div class="frame" id="frame-9" style="display: none;">the parameters \( \theta_0 \) and \( \theta_1 \) that minimize  $$ \sum_{i=1}^{m}-(1 - y^{(i)})ln(1 - \frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}}) -y^{(i)}ln(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}}) $$</div>
      <div class="frame" id="frame-10" style="display: none;"> \( \theta_0 \) and \( \theta_1 \) that minimize  $$J(\theta_0, \theta_1) =  -\frac{1}{m}\bigg[\sum_{i=1}^{m}y^{(i)}ln(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}}) + (1 - y^{(i)})ln(1 - \frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}})\bigg]$$</div>    
      <div class="frame" id="frame-11" style="display: none;"> \( \theta_0 \) and \( \theta_1 \) such that  $$\frac{\partial}{\partial \theta_0}  \Bigg[-\frac{1}{m}\bigg[\sum_{i=1}^{m}y^{(i)}ln(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}}) + (1 - y^{(i)})ln(1 - \frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}})\bigg]\Bigg] = 0$$ and $$\frac{\partial}{\partial \theta_1} \Bigg[-\frac{1}{m}\bigg[\sum_{i=1}^{m}y^{(i)}ln(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}}) + (1 - y^{(i)})ln(1 - \frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}})\bigg]\Bigg] = 0$$</div>
      <div class="frame" id="frame-12" style="display: none;"> \( \theta_0 \) and \( \theta_1 \) such that $$ \sum_{i=1}^m(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}} - y^{(i)}) = 0 $$ and $$ \sum_{i=1}^m(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}} - y^{(i)})x^{(i)} = 0 $$</div>
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
