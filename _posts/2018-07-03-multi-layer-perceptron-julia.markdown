---
layout: post
title: "A Multilayer Perceptron in Julia"
summary: "A Julia program that uses a multi-layer perceptron to classify images from the MNIST dataset."
date:   2018-07-03 07:54:00
---

The Julia program below uses a [multi-layer
perceptron](/2018/07/01/multi-layer-perceptrons) to classify images from the
MNIST dataset. The program should run in several minutes and achieve an
accuracy just under 97%. It has a few notable differences from the [previous
program](/2018/07/01/simple-computer-vision-julia) that only used logistic
regression.

This program uses the [FluxML library](https://fluxml.ai). Run
`Pkg.add("Flux")` before running it. The FluxML API is easier to use than
TensorFlow because it does not separate graph construction and execution.

This program has _tracked parameters_ `featureThetas` and `featureTheta0` for
the feature detection models as well as `outputThetas` and `outputTheta0` for
the classification model. 

{% highlight julia %}
featureThetas = param([scale(r, 784, 500) for r in rand((784, 500))]) # param(zeros((784, 500)))
featureTheta0 = param([scale(r, 1, 500) for r in rand((1, 500))]) # param(zeros((1, 500)))
{% endhighlight %}

{% highlight julia %}
outputThetas = param([scale(r, 500, 10) for r in rand((500, 10))]) # param(zeros((500, 10)))
outputTheta0 = param([scale(r, 1, 10) for r in rand((1, 10))]) # param(zeros((1, 10)))
{% endhighlight %}

In FluxML, tracked parameters are like any other numerical or array type, with
a notable exception: When you perform mathematical operations on a tracked
parameter, _it is able to record the gradients of the operations with respect
to itself._

Feature detection happens with logistic regression models operating on raw
inputs:

{% highlight julia %}
features(example) = 1.0 ./ (1.0 .+ exp.(example * featureThetas .+ featureTheta0))
{% endhighlight %}

Classification happens with a softmax model operating on features:

{% highlight julia %}
model(example) = NNlib.softmax(features(example) * outputThetas .+ outputTheta0)
{% endhighlight %}

During training, the `back!()` function calculates the cost with the side
effect of accumulating gradients. The gradients are retrieved with calls to
`grad()`.

{% highlight julia %}
  back!(cross_entropy)
  update!(featureThetas, -learningRate .* grad(featureThetas))
  update!(featureTheta0, -learningRate .* grad(featureTheta0))
  update!(outputThetas, -learningRate .* grad(outputThetas))
  update!(outputTheta0, -learningRate .* grad(outputTheta0))
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
initial values of $$\vec{\theta}$$, and this program uses random
values in a range recommended by Yoshua Bengio and Xavier Glorot in their
AISTATS 2010 paper, [_Understanding the difficulty of training deep feedforward
neural networks._](http://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf) To
convince yourself of the value of careful initialization, replace the
random initializations with the calls to `zeros` in the comments.
You will notice a decline in accuracy.

<script src="https://gist.github.com/mspandit/7b6a60bf7feb316b679c79e20aaf80bc.js"></script>