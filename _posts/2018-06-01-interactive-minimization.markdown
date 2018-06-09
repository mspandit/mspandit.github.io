---
layout: post
title: "Interactive Minimization of Cost Function"
summary: "Adjust \\(\\theta_0\\) and \\(\\theta_1\\) to minimize the cost function."
date:   2018-06-01 18:03:00
---

The table below show ten examples. The chart shows these examples and a line
defined by $$\theta_0$$ and $$\theta_1$$. Move the sliders to adjust the values
of $$\theta_0$$ and $$\theta_1$$. Try to minimize the value of the cost
function $$J(\theta_0, \theta_1)$$.

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
              <line x1="0" x2="100" y1="0" y2="100" stroke="black" stroke-width="4" id="line"></line>
            </svg>
          </td>
        </tr>
        <tr>
          <td style="text-align: right; height: 30px">\(\theta_0 = \)&nbsp;</td>
          <td id='theta2-out'></td>
          <td colspan="6">
            <div class="slidecontainer">
              <input type="range" min="1" max="100" value="50" class="slider" id="theta2">
            </div>
          </td>
        </tr>
        <tr>
          <td style="text-align: right; height: 30px;">\(\theta_1 = \)&nbsp;</td>
          <td id='theta1-out'></td>
          <td colspan="6" style="">
            <div class="slidecontainer">
              <input type="range" min="1" max="100" value="50" class="slider" id="theta1">
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
    $('#theta1-out').html(slope);
    $('#theta2-out').html(yIntercept);
    $('#j-out').html((loss(slope, yIntercept) + "").slice(0, 7));
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