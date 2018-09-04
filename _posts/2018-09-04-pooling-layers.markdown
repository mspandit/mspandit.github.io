---
layout: post
title: "Pooling Layers"
summary: "Pooling layers \"downsample\" their inputs to highlight or summarize the features in a region."
date:   2018-09-04 16:22:00
---

After an image is processed by a [convolutional
layer](/2018/07/21/convolutional-layers), we are left with a group of feature
maps, each of which indicates the presence of a single feature at various
locations.

Each feature map is smaller than its input. How much smaller depends on the
size of the square processed by each neuron, and the amount of overlap between
one neuron's input and the next. However, there are frequently tens or hundreds
of feature maps in a group, so the output of the group can be many times larger
than the input. It is possible to connect these feature maps to a
fully-connected layer for classification, but this presents an inordinately
large number of calculations.

**Pooling** layers consist of neurons that, like convolutional layer neurons,
are activated by square regions in their input. However, the input regions of
pooling neurons are _non-overlapping._ **Max pooling** neurons output the
maximum value detected in an input region. You can think of them as
highlighting a feature in a region. **Mean pooling** neurons output the average
(mean) value in their input region. You can think of them as summarizing the
features in a region. 

Pooling layers perform calculations during forward propagation, but they have
no parameters, so they don't add to the calculation of gradients during
backpropagataion.

Because each neuron in a pooling layer is activated by a non-overlapping region
of inputs, the size of the output is a fraction of the size of the input. 