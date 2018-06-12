---
layout: post
title: "Visualization of Cost Function for Logistic Regression"
summary: "There is a problem with using gradient descent to minimize the cost function."
date:   2018-06-07 21:46:00
---
Suppose, as in [linear regression](/2018/06/01/linear-regression), we try to
minimize the sum of half the square of the vertical distance between each
example and the logistic curve:

$$J(\theta_0, \theta_1) = \sum_{i=1}^m{\frac{1}{2}(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}} - y^{(i)})^2} $$

The three-dimensional graph below shows the values of this cost function
 for a simple dataset and different values of
$$\theta_0$$ and $$\theta_1$$.

You can click and drag to rotate the graph, scroll to zoom in and out, and
hover over the data points in the graph to see each value of $$\theta_0$$,
$$\theta_1$$, and $$J$$.

As you can see, for a logistic model, this cost function generates a surface
with large flat regions. The process of [gradient
descent](/2018/06/03/gradient-descent) can easily get "stuck" in these regions.
If you try to minimize this cost function for a logistic model, you'll be lucky
if it converges at all, much less in a reasonable number of iterations.

<div id="visualization"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
<script type="text/javascript">
  var trainingExamples = [
    { x: 6, y: 0},
    { x: 8, y: 0},
    { x: 15, y: 0},
    { x: 16, y: 0},
    { x: 22, y: 0},
    { x: 25, y: 1},
    { x: 30, y: 1},
    { x: 31, y: 1},
    { x: 32, y: 1},
    { x: 38, y: 1}
  ]
  
  function loss(slope, yIntercept) {
    sum = 0.0;
    $.map(trainingExamples, function (ex) {
      sum += (1.0 / (1.0 + Math.E ** (slope * ex.x + yIntercept)) - ex.y) ** 2;
    });
    return 0.5 * sum;
  }

    // Create and populate a data table.
    var data = new vis.DataSet();
    var counter = 0;
    var steps = 50;  // number of datapoints will be steps*steps
    var axisMax = 314;
    var xMin = -0.5
    var xMax = 0.5
    var xStep = (xMax - xMin) / steps;
    var yMin = -25.0
    var yMax = 25.0
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
      yLabel: "theta0",
      zLabel: "J",
      tooltip: true,
      showLegend: false
    };

    // Instantiate our graph object.
    var container = document.getElementById('visualization');
    var graph3d = new vis.Graph3d(container, data, options);
</script>