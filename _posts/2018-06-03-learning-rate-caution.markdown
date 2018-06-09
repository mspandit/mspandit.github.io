---
layout: post
title: "Learning Rate Caution"
summary: "Your choice of learning rate affects the success of gradient descent."
date:   2018-06-03 07:46:00
---

When you program a computer to use [gradient
descent](/2018/06/03/gradient-descent), you must choose a learning rate. If the
learning rate is too small, then many iterations might be required before model
converges. If it is too large, then the model may never converge. To illustrate
this, we use gradient descent to find the minimum of a very simple function,
$$f(x) = x^2$$.

The blue line is the graph of the function. According to [step
1.](/2018/06/03/gradient-descent#step1), we start by guessing that the minimum
is at $$x = 8$$. We calculate the gradient $$\frac{\partial f(x)}{\partial x} =
2x$$ and then adjust our guess by the product of the gradient and the learning
rate. We repeat adjustments until the gradient becomes very close to zero.

During the repeated adjustments, different values of $$x$$ are generated. The black line shows the value of the function for these values.

Move the slider to adjust the learning rate and see how long the model takes to
converge---if it converges at all.

<table class="table">
  <tr>
    <td colspan="3" style="text-align: center;">
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
        <input type="range" min="1" max="110" value="1" class="slider" id="learning-rate">
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
    var path = [];
    while (Math.abs(adjustment) > 0.00001 && iterCount < 20000) {
      iterCount += 1;
      currentLoss = loss(x);
      var converged = currentLoss < 11.0;
      path.push(scaleX(x) + "," + scaleY(currentLoss));
      adjustment = learningRate * d_loss_d_x(x);
      x -= adjustment;
    }
    return { points: path, count: iterCount, converged: converged };
  }
  
  function updatePath(learningRate) {
    $('#learning-rate-output').attr("value", learningRate);
    path = generatePath(learningRate);
    if (!path.converged) {
      $('#path').attr("points", path.points.slice(0, 20).join(" "));
      $('#iterations').html("No convergence after 20,000 iterations.")
    } else {
      $('#path').attr("points", path.points.join(" "));
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