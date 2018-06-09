---
layout: post
title: "Multivariate Gradient Descent in Python"
date:   2018-06-04 20:58:00
---

The program below learns a linear relationship between a three-dimensional
input and an output.

It downloads and operates on a dataset from Helmut Spaeth, _Mathematical Algorithms for Linear Regression,_ Academic Press, 1991, ISBN 0-12-656460-4.

The data concerns pasture rent structure and grass variety and includes 67
examples. The inputs are

* the rent per acre of arable land,
* the number of milk cows per square mile, and
* the difference between pasturage and arable land

The output is the rental price per acre for this variety of grass. The program
includes a `loss` function as well as a function that calculates the partial
derivative of the loss with respect to a specified element of $$\vec{\theta}$$.

Note:

* This program depends on the `numpy` library, which can generally be installed
  using the command `pip install numpy`.
  
* This program will generally take a few minutes to complete execution and output the best-fit $$\theta$$ vector.

<script src="https://gist.github.com/mspandit/be155af1cc475ef7ac026e663bcf4c93.js"></script>