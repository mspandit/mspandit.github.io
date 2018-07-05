---
layout: post
title: "Simple Computer Vision in Julia"
summary: "A Julia program that uses stochastic mini-batch gradient descent to classify 28-pixel square images from the MNIST dataset."
date:   2018-07-01 08:44:00
---

The [MNIST dataset <span class="fa
fa-external-link-alt"></span>](https://en.wikipedia.org/wiki/MNIST_database) is
a large set of 28-pixel square grayscale images of handwritten digits. The task
of assigning each image to one of ten classes (digits zero through nine) can be
considered a simple computer vision task. It has been used historically to
evaluate machine learning algorithms. The Julia program below uses stochastic
mini-batch gradient descent to fit a logistic linear model to the training set
of 55,000 images. It then evaluates the model on a test set of 10,000 images
and prints the accuracy of the classification. It runs in a few minutes.

Remember to run `Pkg.add("TensorFlow")` before running it.

The program includes functions from
[https://github.com/malmaud/TensorFlow.jl](https://github.com/malmaud/TensorFlow
.jl) to download and decompress the dataset from an internet source.

{% highlight julia %}
include(Pkg.dir("TensorFlow", "examples", "mnist_loader.jl"))
{% endhighlight %}

The model has $$28 \times 28 = 784$$ input values and 10 output values:

{% highlight julia %}
exampleInput = TensorFlow.placeholder(Float64, shape=[nothing, 784])
exampleOutput = TensorFlow.placeholder(Float64, shape=[nothing, 10])
{% endhighlight %}

The dataset is provided to us as input vectors without $$x_0 = 1$$
[elements](/2018/06/04/not-completely-linear-regression) for $$\theta_0$$.
Therefore, we separate the $$\vec{\theta_0}$$ from the remaining
$$\vec{\theta}$$:

{% highlight julia %}
thetas = TensorFlow.Variable(TensorFlow.ones((784, 10)))
theta0 = TensorFlow.Variable(TensorFlow.ones((1, 10)))
{% endhighlight %}

The model function is slightly different from the logistic function used
previously. `softmax()` divides the logistic result for each class by the sum of
the results over all classes, producing a [probability
distribution](/2018/06/12/multiclass-logistic-regression#probability-distribution) across the possible outputs. The modified cost function reflects this
variation.

{% highlight julia %}
modelOutput = TensorFlow.nn.softmax(
  TensorFlow.matmul(exampleInput, thetas) + theta0
)
cost = TensorFlow.reduce_mean(
  -TensorFlow.reduce_sum(
    TensorFlow.multiply(exampleOutput, TensorFlow.log(modelOutput)), 
    axis=2
  )
)
{% endhighlight %}

In [SGD](/2018/06/28/stochastic-gradient-descent), the overall cost can be
expected to fluctuate from iteration to iteration. The size of the gradients
will fluctuate also. Therefore, we don't bother printing the starting cost of
the model, and we iterate a fixed number of times rather than continuing until
the gradients get close to zero:

{% highlight julia %}
for i = 1:16000
  run(sess, [updateThetas, updateTheta0], getFeeds())
  if (0 == i % 100) print(".") end
end
{% endhighlight %}

Finally, we extend the graph to measure the accuracy of the model. This is done
by comparing the `arg_max()` of the model output---returning the digit with the
highest probability---with the `arg_max()` of the example output vector---the
digit corresponding to the position with a 1. `equal()` will return True if the
two are equal. `cast()` will convert True values to 1.0 and False values to 0.0.

{% highlight julia %}
accuracy = TensorFlow.reduce_mean(
  TensorFlow.cast(
    TensorFlow.equal(TensorFlow.arg_max(modelOutput, 2), TensorFlow.arg_max(exampleOutput, 2)),
    TensorFlow.Float32
  )
)
{% endhighlight %}

The program below should run in a few minutes and produce a model able to
correctly classify over 91% of the test images. This is not a bad result, but
next, we'll look at more complex models that do even better.

<script src="https://gist.github.com/mspandit/474ff83beb59724e35ff19bf915db823.js"></script>