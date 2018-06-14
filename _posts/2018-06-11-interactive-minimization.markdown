---
layout: post
title: "Interactive Minimization of the Logistic Regression Cost Function"
summary: "Adjust \\(\\theta_0\\) and \\(\\theta_1\\) to minimize the cost function."
date:   2018-06-11 17:26:00
---


The table below shows 10 examples. The chart
shows these examples and the curve $$ y = \frac{1}{1 + e^{\theta_0 + \theta_1x}} $$. Move the sliders to minimize the value of the cost function
$$J(\theta_0, \theta_1)$$.

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
              <input type="range" min="1" max="100" value="55" class="slider" id="theta0">
            </div>
          </td>
        </tr>
        <tr>
          <td style="text-align: right; height: 30px;">\(\theta_1 = \)&nbsp;</td>
          <td id='theta1-out'></td>
          <td colspan="6" style="">
            <div class="slidecontainer">
              <input type="range" min="1" max="100" value="40" class="slider" id="theta1">
            </div>
          </td>
        </tr>
        <tr>
          <td style="text-align: right; height: 30px;">\(J(\theta_0, \theta_1) = \)&nbsp;</td>
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
  ];
  var scaleX = d3.scaleLinear().domain([5, 40]).range([30, 440]);
  var scaleY = d3.scaleLinear().domain([-0.1, 1.1]).range([430, 30]);
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
    .attr("cy", function (d) { return scaleY(d.y); }).attr("r", 2);
    theta = [
      parseFloat($("#theta0").attr("value")) - 50,
      (parseFloat($("#theta1").attr("value")) - 50.0) / 50.0
    ] 
    
    function logistic(theta, x) {
      return 1.0 / (1 + Math.E ** (theta[0] + theta[1] * x))
    }
  
    function cost(theta) {
      sum = 0.0;
      $.map(trainingExamples, function (ex) {
        sum += ex.y * Math.log(logistic(theta, ex.x)) + (1 - ex.y) * Math.log(1 - logistic(theta, ex.x));
      });
      return -sum / trainingExamples.length;
    }
    
    function generatePath(theta) {
      path = "";
      for (x = 5; x < 40; x += 0.1) {
        y = logistic(theta, x)
        path += scaleX(x) + "," + scaleY(y) + " ";
      }
      return path;
    }

    function updatePath(theta) {
      $('#theta0-out').html(theta[0]);
      $('#theta1-out').html(theta[1]);
      $('#j-out').html((cost(theta) + "").slice(0, 7));
      $('#path').attr("points", generatePath(theta));
    }
  
    updatePath(theta)
    
    document.getElementById("theta0").oninput = function () {
      theta[0] = parseFloat(this.value) - 50;
      updatePath(theta);
    }
    document.getElementById("theta1").oninput = function () {
      theta[1] = (parseFloat(this.value) - 50.0) / 50.0;
      updatePath(theta);
    }
  
</script>