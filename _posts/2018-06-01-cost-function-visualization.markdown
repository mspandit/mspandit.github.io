---
layout: post
title: "Visualization of the Cost Function"
summary: "An interactive visualization of the cost function for linear regression."
date:   2018-06-01 18:04:00
---

The three-dimensional graph below shows the values of the cost function
$$J(\theta_0, \theta_1)$$ for different values of $$\theta_0$$ and $$\theta_1$$.

You can click and drag to rotate the graph, scroll to zoom in and out, and
hover over the data points in the graph to see each value of $$\theta_0$$,
$$\theta_1$$, and $$J$$.

<div id="visualization"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
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
  
  function loss(slope, yIntercept) {
    sum = 0.0;
    $.map(trainingExamples, function (ex) {
      sum += (slope * ex.x + yIntercept - ex.y) ** 2;
    });
    return 0.5 * sum;
  }

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
      yLabel: "theta0",
      zLabel: "J",
      tooltip: true,
      showLegend: false
    };

    // Instantiate our graph object.
    var container = document.getElementById('visualization');
    var graph3d = new vis.Graph3d(container, data, options);
</script>