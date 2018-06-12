---
layout: post
title: "Visualization of Improved Cost Function for Logistic Regression"
summary: "The new cost function has a convex shape suitable for gradient descent."
date:   2018-06-10 08:43:00
---

You [saw](/2018/06/08/cost-function-visualization) that the cost function for
linear regression generates a surface with large flat regions when it is
applied to logistic regression. Such a cost function is not suitable for
gradient descent.

The [improved](/2018/06/09/logistic-regression-cost-function.html) cost function is:

$$ J(\theta_0, \theta_1) = -\frac{1}{m}\bigg[\sum_{i=1}^{m}{y^{(i)}ln(\frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}}) + (1 - y^{(i)})ln(1 - \frac{1}{1 + e^{\theta_0 + \theta_1x^{(i)}}})}\bigg] $$

The three-dimensional graph below shows the values of the improved cost function for
the same dataset and values of $$\theta_0$$ and $$\theta_1$$.

You can click and drag to rotate the graph, scroll to zoom in and out, and
hover over the data points in the graph to see each value of $$\theta_0$$,
$$\theta_1$$, and $$J$$.

As you can see, for a logistic model, the improved cost function generates a
surface with single "fold." The process of [gradient
descent](/2018/06/03/gradient-descent) can quickly and easily find the values
of $$\theta_1$$ and $$\theta_2$$ that minimize this function.

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
  
  function hypothesis(slope, yIntercept, ex) {
    return 1.0 / (1 + Math.E ** (yIntercept + slope * ex.x));
  }
  
  function cost(slope, yIntercept) {
    sum = 0.0;
    $.map(trainingExamples, function (ex) {
      if (1 == ex.y) {
        sum += Math.log(hypothesis(slope, yIntercept, ex))
      } else {
        sum += Math.log(1 - hypothesis(slope, yIntercept, ex))
      }
    });
    return -sum / trainingExamples.length;
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
            var value = cost(x, y);
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
    console.log(data);
    var graph3d = new vis.Graph3d(container, data, options);
</script>