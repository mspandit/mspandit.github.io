---
layout: post
title: "Scikit-learn for Logistic Regression"
summary: "Scikit-learn is a popular open-source library with a fast, efficient implementation of logistic regression."
date:   2018-06-23 18:00:00
---

It is instructive to study implementations of simple logistic regression using
gradient descent, but the open source community has produced fast, efficient
implementations with flexible options for regularization.
[Scikit-learn](http://scikit-learn.org/stable/index.html) is one of these.

The programs below vividly illustrate that the use of easily-available
libraries can dramatically speed the execution of machine learning, and
dramatically reduce the number of lines of code you have to write and maintain.

# Logistic Regression with Scikit-learn in Python

Use `pip install scikit-learn` before running the Python program below:

<script src="https://gist.github.com/mspandit/c52300c62046890577baf71bce71a6f3.js"></script>

The above program should run in _less than a second_ and then print out
$$\theta$$ values. For each of the classes, try entering its $$\theta$$ values
[here](/2018/06/14/logistic-regression-python#entry-table). When you've entered all the values, you will see what the model function
for that class looks like.

# Logistic Regression with Scikit-learn in Julia

Use `Pkg.add('ScikitLearn')` before running the Julia program below:

<script src="https://gist.github.com/mspandit/68b97321644d17e9bed3704bbf50dc52.js"></script>


The above program should run in a few seconds and then print out
$$\theta$$ values. For each of the classes, try entering its $$\theta$$ values
[here](/2018/06/22/logistic-regression-julia#entry-table). When you've entered all the values, you will see what the model function
for that class looks like.
