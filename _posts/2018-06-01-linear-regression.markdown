---
layout: post
title: "Simple Linear Regression in One Page"
excerpt: "Simple linear regression is one of the simplest forms of supervised machine learnig."
date:   2018-06-01 18:02:00
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

In one of the simplest forms of
[supervised](/2018/05/31/introduction-machine-learning) machine learning, the
computer learns a linear relationship between a single input and its
corresponding continuous-valued output. The training examples consist of $$m$$
input values $${ x_1, x_2, ..., x_m }$$ and their corresponding output values,
$${ y_1, y_2, ..., y_m }$$. **Simple linear regression** means finding a line
such that the _sum of the distances from each value to the line_ is minimized.
This line is a **model** that can then be used to generate outputs for new
inputs.

The equation of any line can be written as $$ y(x) = \theta_1x + \theta_2 $$
where $$\theta_1$$ is the slope of the line and $$\theta_2$$ is its
y-intercept. The actual distance from a point $$(x_i, y_i)$$ to a line is
[fairly
complex](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defi
 ned_by_an_equation). However, we can get the same result by replacing the
actual distance with half the square of its vertical component
$$\frac{1}{2}(y(x_i) - y_i)^2$$. For a line
specified by $$\theta_1$$ and $$\theta_2$$, the function we want to minimize is

$$ J(\theta_1, \theta_2) = \sum_{i=1}^m{\frac{1}{2}(y(x_i) - y_i)^2} = \frac{1}{2}\sum_{i=1}^m{(\theta_1x_i + \theta_2 - y_i)^2} $$

This function is called the <span id='cost-function'>**cost**</span> or **loss** function. Its value is large
when the line is a poor fit for the training examples, and small when the line
is a good fit.

The values of $$\theta_1$$ and $$\theta_2$$ that minimize a function like the
one above can be determined by finding the zeroes of its partial derivatives
with respect to those variables. (We used half the square of the vertical
distance precisely to simplify the partial derivatives.) The partial derivative
with respect to $$\theta_1$$ is simply

$$ \frac{\partial J(\theta_1, \theta_2)}{\partial \theta_1} = \sum_{i=1}^m({\theta_1x_i + \theta_2 - y_i})x_i$$

The partial derivative with respect to $$\theta_2$$ is simply

$$ \frac{\partial J(\theta_1, \theta_2)}{\partial \theta_2} = \sum_{i=1}^m{(\theta_1x_i + \theta_2 - y_i)} = m\theta_2 + \theta_1\sum_{m=1}^i{x_i} - \sum_{m=1}^i{y_i}$$

For simple linear regression, it is possible to set these equations to zero and
solve for $$\theta_1$$ and $$\theta_2$$. 

To learn more complex models, we can find the partial derivatives of the cost
function, but it may not be possible to set them to zero and solve them
directly. We need to take a different approach called _gradient descent._

In the meantime, you can see what it feels like to minimize the cost function
by hand...

# Interactive Minimization of Cost Function

The table below show ten examples. The chart shows these examples and a line
defined by $$\theta_1$$ and $$\theta_2$$. Move the sliders to minimize the
value of the cost function $$J(\theta_1, \theta_2)$$.

<table class="table">
  <tr>
    <td>
      <table class="table">
        <thead>
          <tr>
            <th>$$i$$</th>
            <th>$$x_i$$</th>
            <th>$$y_i$$</th>
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
              <line x1="0" x2="100" y1="0" y2="100" stroke="black" id="line"></line>
            </svg>
          </td>
        </tr>
        <tr>
          <td>$$\theta_1$$</td>
          <td><input type="text" id="theta1-out" style="width: 50px;" disabled="true" /></td>
          <td colspan="6">
            <div class="slidecontainer">
              <input type="range" min="1" max="100" value="50" class="slider" id="theta1">
            </div>
          </td>
        </tr>
        <tr>
          <td>$$\theta_2$$</td>
          <td><input type="text" id="theta2-out" style="width: 50px;" disabled="true" /></td>
          <td colspan="6">
            <div class="slidecontainer">
              <input type="range" min="1" max="100" value="50" class="slider" id="theta2">
            </div>
          </td>
        </tr>
        <tr>
          <td>$$J(\theta_1, \theta_2)$$</td>
          <td><input type="text" id="j-out" style="width: 50px;" disabled="true"></td>
        </tr>
      </table>
    </td>
  </tr>
</table>
<script src="https://d3js.org/d3.v5.min.js"></script>
<script type="text/javascript">
  var trainingExamples = [
    { x: 6, y: 47},
    { x: 8, y: 50},
    { x: 15, y: 66},
    { x: 16, y: 71},
    { x: 22, y: 84},
    { x: 25, y: 95},
    { x: 30, y: 105},
    { x: 31, y: 106},
    { x: 32, y: 110},
    { x: 38, y: 127}
  ]
  var scaleX = d3.scaleLinear().domain([0, 50]).range([30, 440]);
  var scaleY = d3.scaleLinear().domain([0, 150]).range([430, 30]);
  d3.select("#training-examples").selectAll("tr").data(trainingExamples).enter()
    .append("tr").html(function (ex, i) { 
      return "<td>" + (i + 1) + "</td><td>" + ex.x + "</td><td>" + ex.y + "</td>"; 
    });
  d3.select("svg").selectAll("circle").data(trainingExamples).enter()
    .append("circle").attr("cx", function (d) { return scaleX(d.x); })
    .attr("cy", function (d) { return scaleY(d.y); }).attr("r", 2)
  d3.select('svg')
    .append('g')
    .attr("transform", "translate(0, 430)").call(d3.axisBottom(scaleX));
  d3.select('svg')
    .append('g')
    .attr("transform", "translate(30, 0)").call(d3.axisLeft(scaleY));
  $("#theta1").attr("value", 30);
  slope = 0.5
  $("#theta2").attr("value", 0);
  yIntercept = 0
  
  function loss(slope, yIntercept) {
    sum = 0.0;
    $.map(trainingExamples, function (ex) {
      sum += (slope * ex.x + yIntercept - ex.y) ** 2;
    });
    return 0.5 * sum;
  }

  function updateLine(slope, yIntercept) {
    $('#theta1-out').attr('value', slope);
    $('#theta2-out').attr('value', yIntercept);
    $('#j-out').attr('value', loss(slope, yIntercept));
    $('#line').attr("y1", scaleY(yIntercept));
    $('#line').attr("x1", 30);
    $('#line').attr("x2", 440);
    $('#line').attr('y2', scaleY(slope * 50 + yIntercept));
  }
  
  updateLine(slope, yIntercept)
  
  document.getElementById("theta1").oninput = function () {
    slope = (parseFloat(this.value) - 25) / 10.0;
    updateLine(slope, yIntercept);
  }
  document.getElementById("theta2").oninput = function () {
    yIntercept = 3 * parseFloat(this.value) / 2;
    updateLine(slope, yIntercept);
  }
</script>

# Visualization of the Cost Function

The three-dimensional graph below shows the values of the cost function
$$J(\theta_1, \theta_2)$$ for different values of $$\theta_1$$ and $$\theta_2$$.

You can click and drag to rotate the graph, scroll to zoom in and out, and
hover over the data points in the graph to see each value of $$\theta_1$$,
$$\theta_2$$, and $$J$$.

<div id="visualization"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
<script type="text/javascript">
    // Create and populate a data table.
    var data = new vis.DataSet();
    var counter = 0;
    var steps = 50;  // number of datapoints will be steps*steps
    var axisMax = 314;
    var xMin = -2.4
    var xMax = 7.5
    var xStep = (xMax - xMin) / steps;
    var yMin = 0
    var yMax = 150
    var yStep = (yMax - yMin) / steps;
    for (var x = xMin; x < xMax; x += xStep) {
        for (var y = yMin; y < yMax; y += yStep) {
            var value = loss(x, y);
            data.add({
              id: counter++,
              x: x,
              y: y,
              z: value,
              style: ((x == 2.5 && y == 30) ? 0 : value)
            });
        }
    }

    // specify options
    var options = {
      width:  '500px',
      height: '552px',
      style: 'dot-color',
      showPerspective: true,
      showGrid: true,
      showShadow: false,
      keepAspectRatio: false,
      verticalRatio: 0.5,
      xLabel: "theta1",
      yLabel: "theta2",
      zLabel: "J",
      tooltip: true,
      showLegend: false
    };

    // Instantiate our graph object.
    var container = document.getElementById('visualization');
    var graph3d = new vis.Graph3d(container, data, options);
</script>