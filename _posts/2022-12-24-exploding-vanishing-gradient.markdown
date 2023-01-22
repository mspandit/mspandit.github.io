---
layout: post
title: "Exploding and Vanishing Gradients"
summary: ""
date:   2022-12-24 07:45:00 -0700
---

We train neural networks by gradually adjusting a large number (hundreds of
billions in the latest large language models) of weights $$W_i$$. In a
backpropagation pass, the loss is calculated, and the weights are adjusted,
starting at the output layer and proceeding to the input layer. For each
weight, we calculate a partial derivative or _gradient._ Roughly, the gradient
value tells us how rapidly the loss grows (or shrinks) based on an incremental
change to the weight---assuming all other weights are held to their current
value. The magnitude of the gradient reflects how "sensitive" the loss is to an
incremental change in the weight.

If a gradient happens to become extremely small or zero, then the loss is
insensitive to incremental changes in the weight. _There is no point in
continuing to make incremental changes to this weight._ In addition, logically,
the loss will be insensitive to incremental changes to some weights in earlier
layers, because those layers feed their outputs to this one. Those weights will
also change slowly or stop changing entirely. This is the _vanishing gradient
problem._ The network stops training without minimizing the loss.

If a gradient happens to become extremely large, then the loss is overly
sensitive to incremental changes in the weight. Incremental changes in the
weight will cause a large fluctuation in the loss value, but fail to achieve
the desired reduction in the magnitude of the loss. In addition, logically, the
loss will be overly sensitive to incremental changes to some weights in earlier
layers, because those layers feed their outputs to this one. Changes to those
weights will also fail to minimize the loss. This is the _exploding gradient
problem._ During training, the network loss tends to oscillate around its
minimum value.

In a very deep neural network, if the magnitude of the weight matrix $$||W_i|| > 1.0$$,
then the gradients of the loss with respect to the weights will be
likely to explode. If the magnitude of the weight matrix $$||W_i| < 1.0$$, then
the gradients of the cost with respect to the weights will be likely to vanish.

An unrolled recurrent neural network is like a deep network that uses the same
set of weights in every "layer." Consequently, the ability to train the network
is highly sensitive to the magnitude of the weights.

