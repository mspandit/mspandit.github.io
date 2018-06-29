---
layout: post
title: "Multiclass Logistic Regression in Python"
summary: "A Python program that finds polynomial logistic models for three classes. Interactive visualization of the results."
date:   2018-06-14 05:58:00
---

The chart below show 30 examples in three classes---red, green, and blue. Each
class has two inputs $$x_1$$ and $$x_2$$ that range between 0 and 100.

<table class="table">
  <tr>
    <td>
    </td>
    <td>
      <table>
        <tr>
          <td colspan="8">
            <svg width="450" height="450">
            </svg>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>

The Python program below finds polynomial logistic models for the
classes. It uses gradient descent to find coefficients $$\theta_0^{(i)}, \theta_1^{(i)}, ...
\theta_4^{(i)}$$ for $$x_1$$, $$x_2$$, $$x_1^2$$ and $$x_2^2$$ ($$i = {1, 2, 3}$$.)

Don't forget to use `pip install numpy` to install the `numpy` library before
running this.

<script src="https://gist.github.com/mspandit/b98e67057aed89e16ba6e472b28e73fc.js"></script>

<script src="https://d3js.org/d3.v5.min.js"></script>

<script type="text/javascript">
  var trainingExamples = [
    { x1: 6,  x2: 48, y: "red" },
    { x1: 8,  x2: 11, y: "red" },
    { x1: 15, x2:  1, y: "red" },
    { x1: 16, x2: 19, y: "red" },
    { x1: 22, x2: 40, y: "red" },
    { x1: 25, x2: 33, y: "red" },
    { x1: 30, x2: 49, y: "red" },
    { x1: 31, x2: 44, y: "red" },
    { x1: 32, x2: 29, y: "red" },
    { x1: 38, x2:  2, y: "red" },
  
    { x1: 53, x2: 63, y: "green" },
    { x1: 50, x2: 55, y: "green" },
    { x1: 90, x2: 70, y: "green" },
    { x1: 69, x2: 59, y: "green" },
    { x1: 76, x2: 28, y: "green" },
    { x1: 86, x2: 33, y: "green" },
    { x1: 51, x2: 55, y: "green" },
    { x1: 88, x2: 57, y: "green" },
    { x1: 85, x2: 54, y: "green" },
    { x1: 60, x2: 62, y: "green" },
    
    { x1: 14, x2: 66, y: "blue" },
    { x1: 13, x2: 76, y: "blue" },
    { x1: 40, x2: 82, y: "blue" },
    { x1: 10, x2: 98, y: "blue" },
    { x1:  6, x2: 51, y: "blue" },
    { x1: 47, x2: 62, y: "blue" },
    { x1: 40, x2: 85, y: "blue" },
    { x1: 11, x2: 59, y: "blue" },
    { x1: 26, x2: 95, y: "blue" },
    { x1: 20, x2: 88, y: "blue" }
  ];
  var scaleX = d3.scaleLinear().domain([0, 100]).range([30, 440]);
  var scaleY = d3.scaleLinear().domain([0, 100]).range([430, 30]);
  d3.select('svg')
    .append('g')
    .attr("transform", "translate(0, 430)").call(d3.axisBottom(scaleX));
  d3.select('svg')
    .append('g')
    .attr("transform", "translate(30, 0)").call(d3.axisLeft(scaleY));

  e = d3.select("svg").selectAll("circle").data(trainingExamples).enter();
  e.append("circle").attr("cx", function (d) { return scaleX(d.x1); })
    .attr("cy", function (d) { return scaleY(d.x2); }).attr("r", 3).attr("fill", function(d) { return d.y; })

</script>

The above program should run in a few minutes and then print out $$\theta$$
values. For each of the classes, try entering its $$\theta$$ values below.
When you've entered all the values, you will see what the model function for
that class looks like.

<table class="table" id="entry-table">
  <tr>
    <td>       $$\theta_0$$</td>
    <td><input class="theta" type="text"></td>
  </tr>
  <tr>
    <td>       $$\theta_1$$</td>
    <td><input class="theta" type="text"></td>
  </tr>
  <tr>
    <td>       $$\theta_2$$</td>
    <td><input class="theta" type="text"></td>
  </tr>
  <tr>
    <td>       $$\theta_3$$</td>
    <td><input class="theta" type="text"></td>
  </tr>
  <tr>
    <td>       $$\theta_4$$</td>
    <td><input class="theta" type="text"></td>
  </tr>
</table>

<div id="visualization"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
<script type="text/javascript"> 
  function hypothesis(x1, x2, theta) {
    x1 = (x1 - 50.0) / 50.0
    x2 = (x2 - 50.0) / 50.0
    return 1.0 / (1 + Math.E ** (theta[0] + theta[1] * x1 + theta[2] * x2 + theta[3] * x1 * x1 + theta[4] * x2 * x2));
  }

  function getData(theta) {
    // Create and populate a data table.
    var data = new vis.DataSet();
    var counter = 0;
    var steps = 50;  // number of datapoints will be steps*steps
    var axisMax = 314;
    var xMin = 0.0
    var xMax = 100.0
    var xStep = (xMax - xMin) / steps;
    var yMin = 0.0
    var yMax = 100.0
    var yStep = (yMax - yMin) / steps;
    for (var x = xMin; x < xMax; x += xStep) {
        for (var y = yMin; y < yMax; y += yStep) {
            var value = hypothesis(x, y, theta);
            if (!isNaN(value)) {
              data.add({
                id: counter++,
                x: x,
                y: y,
                z: value,
                style: ((x == 2.5 && y == 30) ? 0 : value)
              });
            }
        }
    }
    return data;
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
    yLabel: "theta0",
    zLabel: "model",
    tooltip: true,
    showLegend: false
  };

  // Instantiate our graph object.
  var container = document.getElementById('visualization');
  $(".theta").on("change", function () {
    theta = $.map($(".theta"), function (field) { 
      return parseFloat(field.value); 
    });
    console.log(theta);
    if (theta.every(function (value) { return !isNaN(value); })) {
      var graph3d = new vis.Graph3d(container, getData(theta), options);
    }
  });
</script>