---
layout: post
title: "Exploding and Vanishing Gradients"
summary: ""
date:   2022-12-24 07:45:00 -0700
---

In a very deep neural network, including in an unrolled recurrent neural
network, backpropagated gradients are either amplified or attenuated as their
calculation moves from the output to the input.

Assume input $$x$$, a neural network with $$L$$ layers, weights $$W_i$$ at
layer $$i$$ and the identity activation function (!) at every layer. Then the
output

$$ y = W_L W_{L-1} W_{L-2} ... W_3 W_2 W_1 x $$

If the magnitude of the weight matrix $$||W_i|| > 1.0$$, then the gradients of
the cost with respect to the parameters are too big. After adjusting the
weights on the basis of the cost gradients (during backpropagation) the cost
will tend to oscillate around its minimum value.

If the magnitude of the weight matrix $$||W_i|| < 1.0$$, then the gradients of
the cost with respect to the parameters are too small. The weights will not
change much at all on the basis of the cost gradients (during backpropagation)
and optimization will cease.

