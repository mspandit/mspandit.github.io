---
layout: post
title: "Even Less Linear Regression"
summary: "Learning a <em>polynomial</em> relationship from multiple inputs to an output."
date:   2018-06-06 14:10:00
---

In [simple linear regression](/2018/06/01/linear-regression) the computer
learns a linear relationship between a single input $$ x $$ and a single output
$$ y $$ by calculating two values $$\theta_0$$ and $$\theta_1$$. These values
define a line that best fits the training examples.

<span id="polynomial-regression">**Polynomial regression**</span> finds a
_non-linear_ relationship between the inputs $$ x_1, x_2, \dots, x_n $$ and the
output. The computer calculates $$n + 1$$ values $$\theta_0, \theta_1, ...,
\theta_n$$. These values define a curve (if $$ n = 1 $$), curved surface (if $$
n = 2 $$) or a curved _hypersurface_ (if $$ n > 2$$) that best fits the
training examples.

The model equation for polynomial regression contains terms that raise the
input value to various powers. For example:

$$ y(x) = \theta_0 + \theta_1x + \theta_2x^2 + \theta_3x^3 + \dots $$

In the multiple-dimensional input case, the model equation looks the same.
However, $$ \vec{x} $$ includes inputs raised to various powers as well as
actual inputs.

$$ y(\vec{x}) = \vec{\theta}^T \times \vec{x} $$

In this case, we refer to $$ \vec{x} $$ as a **feature vector** because it
consists of actual inputs as well as "features" of the inputs.

The cost function and its partial derivatives are similar to those for
[multivariate linear regression](/2018/06/04/not-completely-linear-regression):

$$ J(\vec{\theta}) = \sum_{i=1}^m{\frac{1}{2}(\vec{\theta}^T \times \vec{x} - y^{(i)})^2} $$

$$ \frac{\partial J(\vec{\theta})}{\partial \theta_n} = \sum_{i=1}^m(\vec{\theta}^T \times \vec{x} - y^{(i)})x_n^{(i)}$$

Therefore, [gradient descent](/2018/06/03/gradient-descent) can be used to find
the best-fit surface.

# Overfitting

You may be wondering: Which inputs should be raised to which powers? This is a
matter of discretion and experimentation. If you know that the output depends
on an input raised to a power, you should use it. However, the more features
you include, the more iterations your model will require to converge. You can
start with a linear model and gradually add features to $$ \vec{x} $$ and
dimensions to $$ \vec{\theta} $$ until you get the desired fit.

If you include a large number of features, you are likely to encounter the
problem of **overfitting**. The model fits the training data well, but gives
poor or incorrect outputs when fed inputs outside the training data. For this
reason, when given a data set, it is best not to use the entire set for
training. Instead, reserve a portion of it (called the **test data**) for
testing the model after it has been trained. Later, we will look at a couple of
methods for preventing overfitting.

# Interactive Minimization of Cost Function

The table below shows 25 examples drawn from [this
site <i class='fa fa-external-link-alt'></i>](https://newonlinecourses.science.psu.edu/stat501/node/324/). The chart
shows these examples and a curve defined by $$\theta_0, \theta_1$$ and
$$\theta_2$$. Move the sliders to minimize the value of the cost function
$$J(\vec{\theta})$$.

<table class="table">
  <tr>
    <td>
      <table class="table">
        <thead>
          <tr>
            <th>$$i$$</th>
            <th>$$x^{(i)}$$</th>
            <th>$$y^{(i)}$$</th>
          </tr>
        </thead>
        <tbody id='training-examples'>
        </tbody>
      </table>
    </td>
    <td>
      <table>
        <tr>
          <td colspan="8">
            <svg width="450" height="450">
              <polyline fill="none" stroke="black" stroke-width="4" id="path" />
            </svg>
          </td>
        </tr>
        <tr>
          <td style="text-align: right; height: 30px">\(\theta_0 = \)&nbsp;</td>
          <td id='theta0-out'></td>
          <td colspan="6">
            <div class="slidecontainer">
              <input type="range" min="1" max="100" value="30" class="slider" id="theta0">
            </div>
          </td>
        </tr>
        <tr>
          <td style="text-align: right; height: 30px;">\(\theta_1 = \)&nbsp;</td>
          <td id='theta1-out'></td>
          <td colspan="6" style="">
            <div class="slidecontainer">
              <input type="range" min="1" max="100" value="0" class="slider" id="theta1">
            </div>
          </td>
        </tr>
        <tr>
          <td style="text-align: right; height: 30px">\(\theta_2 = \)&nbsp;</td>
          <td id='theta2-out'></td>
          <td colspan="6">
            <div class="slidecontainer">
              <input type="range" min="1" max="100" value="50" class="slider" id="theta2">
            </div>
          </td>
        </tr>
        <tr>
          <td style="text-align: right; height: 30px;">\(J(\vec{\theta}) = \)&nbsp;</td>
          <td id='j-out' style="width: 100px;"></td>
          <td colspan="6"></td>
        </tr>
      </table>
    </td>
  </tr>
</table>

<script src="https://d3js.org/d3.v5.min.js"></script>

<script type="text/javascript">
  var trainingExamples = [
    { x: 6.6, y: -45.4 },
    { x: 10.1, y: -176.6 },
    { x: 8.9, y: -127.1 },
    { x: 6, y: -31.1 },
    { x: 13.3, y: -366.6 },
    { x: 6.9, y: -53.3 },
    { x: 9, y: -131.1 },
    { x: 12.6, y: -320.9 },
    { x: 10.6, y: -204.8 },
    { x: 10.3, y: -189.2 },
    { x: 14.1, y: -421.2 },
    { x: 8.6, y: -113.1 },
    { x: 14.9, y: -482.3 },
    { x: 6.5, y: -42.9 },
    { x: 9.3, y: -144.8 },
    { x: 5.2, y: -14.2 },
    { x: 10.7, y: -211.3 },
    { x: 7.5, y: -75.4 },
    { x: 14.9, y: -482.7 },
    { x: 12.2, y: -295.6 },
    { x: 8.4, y: -106.5 },
    { x: 7.2, y: -63 },
    { x: 13.2, y: -362.2 },
    { x: 7.1, y: -61 },
    { x: 10.4, y: -194 }
  ]
  var scaleX = d3.scaleLinear().domain([5, 15]).range([30, 440]);
  var scaleY = d3.scaleLinear().domain([-500, -20]).range([430, 30]);
  d3.select('svg')
    .append('g')
    .attr("transform", "translate(0, 430)").call(d3.axisBottom(scaleX));
  d3.select('svg')
    .append('g')
    .attr("transform", "translate(30, 0)").call(d3.axisLeft(scaleY));
  
  d3.select("#training-examples").selectAll("tr").data(trainingExamples).enter()
    .append("tr").html(function (ex, i) { 
      return "<td>" + (i + 1) + "</td><td>" + ex.x + "</td><td>" + ex.y + "</td>"; 
    });

  d3.select("svg").selectAll("circle").data(trainingExamples).enter()
    .append("circle").attr("cx", function (d) { return scaleX(d.x); })
    .attr("cy", function (d) { return scaleY(d.y); }).attr("r", 2)
    theta = [
      parseFloat($("#theta0").attr("value")) - 50,
      parseFloat($("#theta1").attr("value")) - 50,
      parseFloat($("#theta2").attr("value")) - 50      
    ] 
  
    function loss(theta) {
      sum = 0.0;
      $.map(trainingExamples, function (ex) {
        sum += (theta[0] + theta[1] * ex.x + theta[2] * (ex.x ** 2) - ex.y) ** 2;
      });
      return 0.5 * sum;
    }
    
    function generatePath(theta) {
      path = "";
      for (x = 5; x < 15; x += 0.1) {
        y = theta[0] + theta[1] * x + theta[2] * (x ** 2);
        path += scaleX(x) + "," + scaleY(y) + " ";
      }
      return path;
    }

    function updatePath(theta) {
      $('#theta0-out').html(theta[0]);
      $('#theta1-out').html(theta[1]);
      $('#theta2-out').html(theta[2]);
      $('#j-out').html((loss(theta) + "").slice(0, 7));
      $('#path').attr("points", generatePath(theta));
    }
  
    updatePath(theta)
    
    document.getElementById("theta0").oninput = function () {
      theta[0] = parseFloat(this.value) - 50;
      updatePath(theta);
    }
    document.getElementById("theta1").oninput = function () {
      theta[1] = parseFloat(this.value) - 50;
      updatePath(theta);
    }
    document.getElementById("theta2").oninput = function () {
      theta[2] = parseFloat(this.value) - 50;
      updatePath(theta);
    }
  
</script>