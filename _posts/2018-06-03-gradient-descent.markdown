---
layout: post
title: "Gradient Descent"
excerpt: ""
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
derivative equations, but setting them to zero and then solving for the
variables may not be possible.

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
you already have a good sense for gradient descent. You probably moved the
sliders rapidly until the line came close to the data set. During this time,
the cost function decreased rapidly. Then, you probably made fine adjustments,
paying close attention to the value of $$J(\theta_1, \theta_2)$$.
  
# Gradient Descent in Python

Below is a Python program that calculates $$\theta_1$$ and $$\theta_2$$ from
the data set used in the interactive linear regression:

```
import random

def loss(theta1, theta2, examples):
    """Cost or loss function"""
    return 0.5 * sum([(theta1 * ex["x"] + theta2 - ex["y"]) ** 2 for ex in examples])

def d_loss_d_theta1(theta1, theta2, examples):
    """Partial derivative function of loss w.r.t. theta1"""
    return sum([(theta1 * ex["x"] + theta2 - ex["y"]) * ex["x"] for ex in examples])

def d_loss_d_theta2(theta1, theta2, examples):
    """Partial derivative function of loss w.r.t. theta2."""
    return len(training_examples) * theta2 + theta1 * sum([ex["x"] for ex in examples]) - sum([ex["y"] for ex in examples])

if __name__ == "__main__":
    theta1 = random.random() * 100
    theta2 = random.random() * 100

    training_examples = [
        { "x": 6, "y": 47},
        { "x": 8, "y": 50},
        { "x": 15, "y": 66},
        { "x": 16, "y": 71},
        { "x": 22, "y": 84},
        { "x": 25, "y": 95},
        { "x": 30, "y": 105},
        { "x": 31, "y": 106},
        { "x": 32, "y": 110},
        { "x": 38, "y": 127}
    ]

    currentLoss = loss(theta1, theta2, training_examples)

    learning_rate = 0.0003

    adjustment1 = 10
    adjustment2 = 10
    iter_count = 0
    
    while adjustment1 > 1e-7 or adjustment2 > 1e-7:
        adjustment1 = learning_rate * d_loss_d_theta1(theta1, theta2, training_examples)
        adjustment2 = learning_rate * d_loss_d_theta2(theta1, theta2, training_examples)
        theta1 -= adjustment1
        theta2 -= adjustment2
        currentLoss = loss(theta1, theta2, training_examples)
        iter_count += 1

    print("theta1 = %0.2f, theta2 = %0.2f in %d iterations" % (theta1, theta2, iter_count))
```

# Gradient Descent in Julia

Below is the same program written in the [Julia](http://julialang.org) language:

```
function loss(theta1, theta2, examples)
    # Cost or loss function
    0.5 * sum([(theta1 * ex["x"] + theta2 - ex["y"]) ^ 2 for ex in examples])
end

function d_loss_d_theta1(theta1, theta2, examples)
    # Partial derivative function of loss w.r.t. theta1
    sum([(theta1 * ex["x"] + theta2 - ex["y"]) * ex["x"] for ex in examples])
end

function d_loss_d_theta2(theta1, theta2, examples)
    # Partial derivative function of loss w.r.t. theta2.
    length(training_examples) * theta2 + theta1 * sum([ex["x"] for ex in examples]) - sum([ex["y"] for ex in examples])
end

theta1 = rand(0:100)
theta2 = rand(0:100)

training_examples = [
    Dict("x" => 6,  "y" => 47),
    Dict("x" => 8,  "y" => 50),
    Dict("x" => 15, "y" => 66),
    Dict("x" => 16, "y" => 71),
    Dict("x" => 22, "y" => 84),
    Dict("x" => 25, "y" => 95),
    Dict("x" => 30, "y" => 105),
    Dict("x" => 31, "y" => 106),
    Dict("x" => 32, "y" => 110),
    Dict("x" => 38, "y" => 127)
]

currentLoss = loss(theta1, theta2, training_examples)

learning_rate = 0.0003

adjustment1 = 10
adjustment2 = 10
iterCount = 0

while abs(adjustment1) > 1e-7 || abs(adjustment2) > 1e-7
    adjustment1 = learning_rate * d_loss_d_theta1(theta1, theta2, training_examples)
    adjustment2 = learning_rate * d_loss_d_theta2(theta1, theta2, training_examples)
    theta1 -= adjustment1
    theta2 -= adjustment2
    iterCount += 1
end

println("theta1 = $(theta1), theta2 = $(theta2) in $(iterCount) iterations")
```

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