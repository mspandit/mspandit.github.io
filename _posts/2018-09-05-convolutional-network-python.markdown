---
layout: post
title: "A Convolutional Neural Network in Python"
summary: "A combination of convolutional and pooling layers, with relu activation, gives us improved accuracy on the MNIST digit classification task."
date:   2018-09-05 09:16:00
---

The Python program below is based on an example from the [Tensorflow repository <i class="fa
fa-external-link-alt" title="(External link)"></i>](https://github.com/tensorflow/tensorflow). It uses a combination of
[convolutional](/2018/07/21/convolutional-layers) and
[pooling](/2018/09/04/pooling-layers) layers to classify images from the MNIST
dataset. The program should run for about half an hour and achieve an accuracy
of approximately 97% on the test set.

The model's graph is built up inside the `deepnn()` function, which uses a
variable `example_input`:

<pre data-enlighter-language="python" data-enlighter-linenumbers="false">
  example_input = tf.placeholder(tf.float32, [None, 784])
  model_output = deepnn(example_input)
</pre>

`deepnn()` first reshapes the input to suit a two-dimensional convolutional
layer. 

<pre data-enlighter-language="python" data-enlighter-linenumbers="false">
    example_image = tf.reshape(example_input, [-1, 28, 28, 1])
</pre>

The convolutional layer looks at 5&times;5 pixel regions and generates 32
feature maps. The feature maps are padded to ensure they are the same size as
the input. The values in these feature maps are passed through [rectified
linear units](/2018/09/04/another-activation-function).

<pre data-enlighter-language="python" data-enlighter-linenumbers="false">
  thetas_conv1 = weight_variable([5, 5, 1, 32])
  theta0_conv1 = bias_variable([32])
  activation_conv1 = tf.nn.relu(conv2d(example_image, thetas_conv1) + theta0_conv1)
</pre>

The output of this layer is passed to a max-pooling layer that looks at
2&times;2 pixel regions, downsampling the feature maps to a quarter of their size.

<pre data-enlighter-language="python" data-enlighter-linenumbers="false">
  activation_pool1 = max_pool_2x2(activation_conv1)
</pre>

Another convolutional layer looks at 5&times;5 pixel regions, this time generating 64 feature maps. The values in these feature maps are also passed
through relus.

<pre data-enlighter-language="python" data-enlighter-linenumbers="false">
  thetas_conv2 = weight_variable([5, 5, 32, 64])
  theta0_conv2 = bias_variable([64])
  activation_conv2 = tf.nn.relu(conv2d(activation_pool1, thetas_conv2) + theta0_conv2)
</pre>

These outputs are passed to another max-pooling layer.

<pre data-enlighter-language="python" data-enlighter-linenumbers="false">
  activation_pool2 = max_pool_2x2(activation_conv2)
</pre>
