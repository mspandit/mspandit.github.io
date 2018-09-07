---
layout: post
title: "Simple Computer Vision in Python"
summary: "A Python program that uses stochastic mini-batch gradient descent to classify 28-pixel square images from the MNIST dataset."
date:   2018-06-29 08:58:00
---

The [MNIST dataset <span class="fa
fa-external-link-alt"></span>](https://en.wikipedia.org/wiki/MNIST_database) is
a large set of 28-pixel square grayscale images of handwritten digits. The task
of assigning each image to one of ten classes (digits zero through nine) can be
considered a simple computer vision task. It has been used historically to
evaluate machine learning algorithms. The Python program below uses stochastic
mini-batch gradient descent to fit a logistic linear model to the training set
of 55,000 images. It then evaluates the model on a test set of 10,000 images
and prints the accuracy of the classification.

Remember to run `pip install tensorflow` or otherwise install TensorFlow.

TensorFlow includes a function to download and decompress the dataset from an
internet source. `one_hot=True` ensures that the output vector will have a 1 in
the position corresponding to the correct classification, and zeroes elsewhere:

<pre data-enlighter-language="python" data-enlighter-lineoffset="9">
mnist = input_data.read_data_sets("/tmp/mnist_data", one_hot=True)
</pre>

The model has $$28 \times 28 = 784$$ input values and 10 output values:

<pre data-enlighter-language="python" data-enlighter-lineoffset="12">
example_input = tf.placeholder(tf.float32, [None, 784])
example_output = tf.placeholder(tf.float32, [None, 10])
</pre>

The dataset is provided to us as input vectors without $$x_0 = 1$$ [elements](/2018/06/04/not-completely-linear-regression) for $$\theta_0$$. Therefore, we separate the $$\vec{\theta_0}$$ from the remaining $$\vec{\theta}$$:

<pre data-enlighter-language="python" data-enlighter-lineoffset="22">
thetas = tf.Variable(tf.zeros([784, 10]))
theta0 = tf.Variable(tf.zeros([10]))
</pre>

The model function is slightly different from the logistic function used
previously. `softmax()` divides the logistic result for each class by the sum of
the results over all classes, producing a [probability
distribution](/2018/06/12/multiclass-logistic-regression#probability-distribution) across the possible outputs. The modified cost function reflects this
variation.

<pre data-enlighter-language="python" data-enlighter-lineoffset="25">
model_output = tf.nn.softmax(tf.matmul(example_input, thetas) + theta0)
cost = tf.reduce_mean(
    -tf.reduce_sum(example_output * tf.log(model_output), reduction_indices=1))
</pre>

In [SGD](/2018/06/28/stochastic-gradient-descent), the overall cost can be
expected to fluctuate from iteration to iteration. The size of the gradients
will fluctuate also. Therefore, we don't bother printing the starting cost of
the model, and we iterate a fixed number of times rather than continuing until
the gradients get close to zero:

<pre data-enlighter-language="python" data-enlighter-lineoffset="35">
for _ in range(16000):
    sess.run([update_thetas, update_theta0], feed_dict=get_feeds())
</pre>

Finally, we extend the graph to measure the accuracy of the model. This is done
by comparing the `argmax()` of the model output---returning the digit with the
highest probability---with the `argmax()` of the example output vector---the
digit corresponding to the position with a 1. `equal()` will return True if the
two are equal. `cast()` will convert True values to 1.0 and False values to 0.0.

<pre data-enlighter-language="python" data-enlighter-lineoffset="38">
accuracy = tf.reduce_mean(
    tf.cast(
        tf.equal(tf.argmax(model_output, 1), tf.argmax(example_output, 1)),
        tf.float32))
</pre>

The program below should run in under a minute and produce a model able to
correctly classify over 91% of the test images. This is not a bad result, but
next, we'll look at more complex models that do even better.

<script src="https://gist.github.com/mspandit/4c1b234e9c03dcd2759ff57ddc5ea35b.js"></script>