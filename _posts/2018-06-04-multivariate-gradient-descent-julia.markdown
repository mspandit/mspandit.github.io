---
layout: post
title: "Multivariate Gradient Descent in Julia"
date:   2018-06-04 20:59:00
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

* This program dpends on the `HTTP` package, which can generally be installed
  using the command `Pkg.add("HTTP")`

* This program will generally take several seconds to complete execution and output the best-fit $$\theta$$ vector.

<script src="https://gist.github.com/mspandit/2511130379af6fbc885d04c71e8868b3.js"></script>
