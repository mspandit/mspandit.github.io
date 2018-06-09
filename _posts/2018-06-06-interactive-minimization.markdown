---
layout: post
title: "Interactive Minimization of the Cost Function"
summary: "Adjust \\(\\theta_0\\), \\(\\theta_1\\) and \\(\\theta_2\\) to minimize the cost function."
date:   2018-06-06 14:11:00
---


The table below shows 25 examples drawn from [this
site <i class='fa fa-external-link-alt'></i>](https://newonlinecourses.science.psu.edu/stat501/node/324/). The chart
shows these examples and the curve $$y = \theta_0 + \theta_1x + \theta_2x^2$$. Move the sliders to minimize the value of the cost function
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
              <input type="range" min="1" max="100" value="52" class="slider" id="theta2">
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