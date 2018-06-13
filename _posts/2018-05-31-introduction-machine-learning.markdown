---
layout: post
title: "Introduction to Machine Learning"
summary: "An introduction to a series of posts on machine learning."
date:   2018-05-31 20:14:00
---
<svg style="width: 555px; height: 150px; cursor: pointer;">
  <style>
    .label { font: 10px sans-serif; }
    .circle { fill: white; stroke: black; stroke-width: 1; opacity: 0.5;}
    .highlighted { fill: yellow; }
  </style>
  <ellipse cx="276.5" cy="75" rx="275" ry="73" class="circle" id="ai-circle"> </ellipse>
  <text x="260" y="15" class="label" id="ai-label"> Artificial Intelligence </text>
  
  <ellipse cx="276.5" cy="75" rx="260" ry="58" class="circle" id="ml-circle"> </ellipse>
  <text x="260" y="30" class="label" id="ml-label"> Machine Learning </text>
  
  <ellipse cx="276.5" cy="47" rx="110" ry="14" class="circle" id="s-circle"> </ellipse>
  <text x="260" y="45" class="label" id="ml-label"> Supervised  </text>
  
  <ellipse cx="276.5" cy="97" rx="110" ry="14" class="circle" id="u-circle"> </ellipse>
  <text x="260" y="95" class="label" id="ml-label"> Unsupervised  </text>
  
  <ellipse cx="143" cy="75" rx="95" ry="29" class="circle" id="r-circle"></ellipse>
  <text x="128" y="60" class="label" id="r-label">Regression</text>
  
  <ellipse cx="411" cy="75" rx="95" ry="29" class="circle" id="c-circle"></ellipse>
  <text x="406" y="60" class="label" id="c-label">Classification</text>
</svg>

The human mind is able to identify objects in our vision, recognize words spoken in our hearing, understand
multiple languages, and play games. <span id="ai-description">**Artificial intelligence** (“AI”) is the discovery and study of methods to
make computers mimic the functions of human minds.</span>

To make computers perform useful functions, programmers typically write and test many thousands of lines of
computer code, and frequently update that code over time. The code instructs a computer to accept inputs (like
gestures on a touch screen or video from a camera) and generate outputs (like files, graphics on a display, or
sounds from a speaker). <span id='ml-description'>**Machine learning** (ML) is the part of AI that makes computers learn new functions
without writing code for each one.</span>

<span id='r-description'>In **regression,** the computer learns to generate a _continuous-valued_ output from its
input.</span> For example, given inputs like the square footage of a home, the number of bedrooms, and its
geographic location, the computer might learn to output the price of the home.

<span id='c-description'>In **classification,** the computer learns to generate a _discrete-valued_ output from
its input.</span> For example, given an e-mail as input, the computer might learn to classify it as “junk” or
“not junk.”

<span id='s-description'>In **supervised learning,** the computer is given
**training examples,** each consisting of an input and the expected
output.</span> From these examples, the computer learns to generate the correct
output, even for inputs it has never been given before.

<span id='u-description'>In **unsupervised learning,** the computer is given
example inputs, but no outputs. The computer learns to _encode_ the
input---represent it in some useful way.</span> For example the output might be
a compressed representation from which the input can be recovered. It might
expose hidden similarities between inputs, allowing them to be **clustered**
near each other. The output can also be used for detection of **anomalies,**
hidden irregularities in inputs.

[<img src="/images/dt130202.gif" />](http://dilbert.com/strip/2013-02-02)

<script type="text/javascript">
  var states = {};
  function interact(circle, description) {
    states[circle] = 'normal';
    $(circle).on('click', function () {
      if (states[circle] == 'normal') {
        states[circle] = 'highlighted';
      } else {
        states[circle] = 'normal';
      }
    })
    $(circle).on('mouseover', function () {
      $(description).attr('style', 'background-color: yellow;');
      $(circle).attr('style', "fill:yellow;stroke:black;stroke-width:1");
    });
    $(circle).on('mouseleave', function () {
      if (states[circle] == 'normal') {
        $(description).attr('style', 'background-color: white;');
        $(circle).attr('style', "fill:white;stroke:black;stroke-width:1");
      }
    });
    $(description).on('mouseover', function () {
      if (states[circle] == 'normal') {
        $(description).attr('style', 'background-color: yellow;');
        $(circle).attr('style', "fill:yellow;stroke:black;stroke-width:1");
      }
    });
    $(description).on('mouseleave', function () {
      if (states[circle] == 'normal') {
        $(description).attr('style', 'background-color: white;');
        $(circle).attr('style', "fill:white;stroke:black;stroke-width:1");
      }
    });
  }
  interact("#ai-circle", "#ai-description");
  interact('#ml-circle', '#ml-description');
  interact('#r-circle', '#r-description');
  interact('#c-circle', '#c-description');
  interact('#s-circle', '#s-description');
  interact('#u-circle', '#u-description');
</script>
