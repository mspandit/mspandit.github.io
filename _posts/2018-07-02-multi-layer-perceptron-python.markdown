---
layout: post
title: "A Multilayer Perceptron in Python"
summary: "A Python program that uses a multi-layer perceptron to classify images from the MNIST dataset."
date:   2018-07-02 17:39:00
---

The Python program below uses a [multi-layer
perceptron](/2018/07/01/multi-layer-perceptrons) to classify images from the
MNIST dataset. The program should run in a few minutes and achieve an accuracy
of just under 97%. It has a few notable differences from the [previous
program](/2018/06/29/simple-computer-vision-python) that only used logistic
regression.

This program has parameters `feature_thetas` and `feature_theta0` for the
feature detection models as well as `output_thetas` and `output_theta0` for the
classification model.

Feature detection happens with logistic regression models operating on raw
inputs:

{% highlight python %}
features = 1.0 / (1.0 + tf.exp(tf.matmul(example_input, feature_thetas) + feature_theta0))
{% endhighlight %}

Classification happens with a softmax model operating on features:

{% highlight python %}
model_output = tf.nn.softmax(tf.matmul(features, output_thetas) + output_theta0)
{% endhighlight %}

# Number of Features

The model implemented by this program detects 500 features of the input. The
number 500 is called a **hyperparameter** of the model (in contrast to the
parameters $$\vec{\theta}$$). The choice of hyperparameter values is a matter
of experience and experimentation. Generally, if the number of features is
smaller than the number of inputs, then the features are a "compressed"
representation of the input.

# Initialization of $$\vec{\theta}$$

The previous program initialized `thetas` and `theta0` values to zero. For
multi-layer perceptrons, this is not a good idea. When their parameter values
are exactly the same, the feature detection models are all detecting the same
feature! Their gradients will be the same and they will be updated by the same
amounts, rendering them largely redundant. Researchers have searched for good
initial values of $$\vec{\theta}$$, and `VariableInitializerRandom` uses random
values in a range recommended by Yoshua Bengio and Xavier Glorot in their
AISTATS 2010 paper, [_Understanding the difficulty of training deep feedforward
neural networks._](http://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf) To
convince yourself of the value of careful initialization, replace the
instatiations of `VariableInitializerRandom` with `VariableInitializerZero`.
You will notice a decline in accuracy.


<script src="https://gist.github.com/mspandit/01eca4759bbe1c6b035b64e099f05293.js"></script>

