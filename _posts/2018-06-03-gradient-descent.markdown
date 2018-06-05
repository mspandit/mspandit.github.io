---
layout: post
title: "Gradient Descent"
excerpt: "A standard, iterative method for minimizing the cost function."
date:   2018-06-03 07:43:00
---
<style type="text/css" media="screen">
  .slider {
      -webkit-appearance: none;
      width: 100%;
      height: 15px;
      border-radius: 5px;   
      background: #d3d3d3;
      outline: none;
      opacity: 0.7;
      -webkit-transition: .2s;
      transition: opacity .2s;
  }

  .slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 25px;
      height: 25px;
      border-radius: 50%; 
      background: #4CAF50;
      cursor: pointer;
  }

  .slider::-moz-range-thumb {
      width: 25px;
      height: 25px;
      border-radius: 50%;
      background: #4CAF50;
      cursor: pointer;
  }
</style>

For [simple linear regression](/2018/06/01/linear-regression), it is possible
to minimize the [cost function](/2018/06/01/linear-regression#cost-function) by
setting its partial derivative equations to zero and then solving for the
variables $$\theta_1$$ and $$\theta_2$$.

In modern machine learning, the computer learns vastly more complex, non-linear
models. (You'll encounter them later.) These models typically describe the
relationships between _millions_ of inputs and _thousands_ of outputs. To learn
such models, we can still define a cost function and find its partial
derivative equations. Setting them to zero and solving for the variables may be
impossible or excessively time-consuming.

The alternative method to minimize the cost function is **gradient descent:** 

1. We start with some (possibly random) values for the variables.

2. We calculate the _partial derivatives_ of the cost function at that point.
These values are called **gradients** because each is the rate of change (slope
of the tangent) of the cost function based on the change in one variable.

3. We adjust each variable value by an amount _directly proportional to its
corresponding gradient._ (Of course, if the gradient is zero, then the variable
is already "doing its part" to minimize the cost function, and we need not
change its value.) The [constant of
proportionality](https://en.wikipedia.org/wiki/Proportionality_(mathematics))
is called the **learning rate**.

4. We repeat steps 2. and 3. until _all_ the gradients are zero (or very close
to it). When this happens, we loosely say that "the model has converged." This
really means we have arrived at a set of values that minimize the cost function
for the training set.

If you tried to minimize the linear regression cost function
[interactively](/2018/06/01/linear-regression#interactive-minimization-of-cost-function), 
you already have a good sense for gradient descent. You may have moved the
sliders rapidly until the line came close to the data set. During this time,
the cost function decreased rapidly. Then, you could make fine adjustments,
paying close attention to the value of $$J(\theta_1, \theta_2)$$.
  
# Gradient Descent in Python

Below is a Python program that calculates $$\theta_1$$ and $$\theta_2$$ from
the data set used in the interactive linear regression:

<script src="https://gist.github.com/mspandit/7296e379cbea13e02bc4e710a3e2a3f6.js"></script>

# Gradient Descent in Julia

Below is the same program written in the [Julia](http://julialang.org) language:

<script src="https://gist.github.com/mspandit/00a989341da3f09e4688e2b967306930.js"></script>

# Learning Rate Caution

If the learning rate is too small, then too many iterations will be required
before model converges. If it is too large, then the model may never converge.
To illustrate this, we use gradient descent to find the minimum of the simple
function $$f(x) = x^2$$.

The blue line is the graph of the function. According to step 1. above, we
start by guessing that the minimum is at $$x = 8$$. We calculate the gradient
$$\frac{\partial f(x)}{\partial x} = 2x$$ and then adjust our guess by the
product of the gradient and the learning rate. We repeat adjustments until the
gradient becomes very close to zero. 

The black line shows the value of the function for different values of $$x$$
that are generated during gradient descent.

Move the slider to adjust the learning rate and see how long the model takes to
converge---if it converges at all.

<table class="table">
  <tr>
    <td colspan="3">
      <svg width="450" height="450">
        <polyline fill="none" stroke="blue" stroke-width="1" id="curve" />
        <polyline fill="none" stroke="black" stroke-width="4" id="path" />
      </svg>
    </td>
  </tr>
  <tr>
    <td colspan="3" id="iterations"></td>
  </tr>
  <tr>
    <td>learning rate:</td>
    <td><input type="text" disabled="true" id="learning-rate-output" style="width: 100px;"/></td>
    <td>
      <div class="slidecontainer" style="width: 300px;">
        <input type="range" min="1" max="100" value="1" class="slider" id="learning-rate">
      </div>
    </td>
  </tr>
</table>

<script src="https://d3js.org/d3.v5.min.js"></script>
<script type="text/javascript">
  function loss(x) {
    return x ** 2;
  }
  
  function d_loss_d_x(x) {
    return 2 * x;
  }
  
  function generatePath(learningRate) {
    var x = 8;
    var adjustment = 10;
    var iterCount = 0;
    var path = "";
    while (Math.abs(adjustment) > 0.00001 && iterCount < 20000) {
      iterCount += 1;
      currentLoss = loss(x);
      var converged = currentLoss < 11.0;
      path += scaleX(x) + "," + scaleY(currentLoss) + " "
      adjustment = learningRate * d_loss_d_x(x);
      x -= adjustment;
    }
    return { points: path, count: iterCount, converged: converged };
  }
  
  function updatePath(learningRate) {
    $('#learning-rate-output').attr("value", learningRate);
    path = generatePath(learningRate);
    $('#path').attr("points", path.points);
    if (!path.converged) {
      $('#iterations').html("No convergence after 20,000 iterations.")
    } else {
      $('#iterations').html("Converged after " + path.count + " iterations.");
    }
  }

  var scaleX = d3.scaleLinear().domain([-10, 10]).range([0, 450]);
  var scaleY = d3.scaleLinear().domain([0, 100]).range([430, 0]);
  d3.select('svg')
    .append('g')
    .attr("transform", "translate(0, 430)").call(d3.axisBottom(scaleX));
  d3.select('svg')
    .append('g')
    .attr("transform", "translate(225, 0)").call(d3.axisLeft(scaleY));
    
  points = ""
  for (x = -10; x <= 10; x += 0.1) {
    y = loss(x);
    points += scaleX(x) + "," + scaleY(y) + " "
  }
  $('#curve').attr("points", points);
  
  updatePath((parseFloat($('#learning-rate').attr('value')) / 100));
  
  document.getElementById("learning-rate").oninput = function () {
    learningRate = (parseFloat(this.value) / 100);
    updatePath(learningRate)
  }
  
</script>