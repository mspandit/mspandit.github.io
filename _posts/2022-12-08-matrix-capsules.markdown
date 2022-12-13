---
layout: post
title: "Matrix Capsules with EM Routing"
summary: "Notes on paper published by Geoffrey Hinton."
date:   2022-12-08 12:33:00
---

# Neural Networks

Neural networks typically apply a simple non-linear function to the scalar
output of a linear filter. They may also use softmax non-linearities to convert
a whole vector of activations into a vector of probabilities.

# Convolutional Neural Networks (CNNs)

A vision system needs to use the same feature-detection knowledge at all
locations in an image. CNNs achieve this by tying the weights of feature
detectors so that detectors learned in one location can detect features in
other locations.

Convolutional capsules extend this cross-location knowledge-sharing to include
knowledge about part-whole relationships.

A _pose matrix_ represents the relationship between an object in the real world
in an image. It captures the transformation between the real-world coordinate
frame and the viewer's coordinate frame. Changes in the viewpoint have complex
effects on pixel intensities in the image, but they have simple, linear effects
on the pose matrix.

# [Matrix Capsules with EM Routing][1]

A _capsule_ is a group of neurons whose activations represent different
properties of the same entity. In this paper, each capsule has

* a neuron $$a$$ with logistical output to represent the _presence_ of the
entity, and

* $$ 4 \times 4 = 16$$ neurons $$M$$ representing the _pose_ of the entity (the
relationship between the entity and the viewer)

Capsules make use of the linearity of effects on the pose matrix arising from
viewpoint changes. They also make use of the linearity to improve segmentation
decisions. (?)

A _capsule network_ consists of layers. Each layer consists of numerous
capsules. A capsule in one layer "votes" for the pose matrix of each capsule in
the layer above by multiplying its own pose matrix with a 4 &times; 4
transformation matrix $$W_{ij}$$. The transformation matrix is trainable,
viewpoint-invariant and represents the relationship between a part in the lower
layer and a whole in the upper layer. Each vote $$V_{ij} = M_iW_{ij}$$ is
weighted by an assignment coefficient (referred to as a "coupling" coefficient
[earlier][2].)

These coefficients are iteratively updated for each image using the
[Expectation Maximization (EM) algorithm][3]. Subsequently, the output of each
"child" capsule is routed to a "parent" capsule in the layer above that
receives a cluster of similar votes.

Each transformation matrix is trained discriminatively by backpropagating
through the unrolled iterations of EM between each pair of adjacent capsule
layers.

Detection of a familiar object by detecting agreement between votes for its
pose matrix (coming from parts that have already been detected) is
high-dimensional coincidence filtering. As the viewpoint changes, the pose
matrices of the parts and the whole will change in a coordinated way.
Consequently, agreement between votes from different parts remains robust
despite viewpoint changes.

One way to assign parts to wholes is by finding tight clusters of
high-dimensional votes that agree. A fast iterative process called "routing by
agreement" updates a part-whole assignment based on the proximity of the part's
vote to votes from other parts assigned to the same whole. The activation of a
capsule depends on multiple incoming pose predictions. This contrasts with
standard neural networks where the activity of a neuron depends on a single
incoming activation vector and a learned weight vector.

# How Capsules Work

Capsules use a more complex non-linearity than neural networks. This
non-linearity converts the whole set of activation probabilities and poses of
the capsules in one layer into the activation probabilities and poses of
capsules in the next layer.

The non-linear procedure is a version of the EM algorithm. It iteratively
adjusts the means, variances, and activation probabilities of the capsules in
the upper layer and the assignment probabilities between the lower and upper
layer.

# Using EM for Routing-by-Agreement

Suppose the poses and activation probabilities of all the capsules in one layer
have been decided. Now we want to decide which capsules in the layer above to
activate, and how to assign each active lower-level (child) capsule to an
active higher-level (parent) capsule.

The routing process has a strong resemblance to fitting a mixture of Gaussians
using EM, where the parent capsules play the role of Gaussians and the means of
the activated child capsules play the role of data points.

The E step in EM determines, for each data point, the probability with which it
is assigned to each of the Gaussians.

The M step determines, for each Gaussian, the mean of the weighted datapoints
and the variance around that mean.

# Capsule Architecture

1. 5 &times; 5 pixel kernel convolutional layer with $$A = 32$$ feature maps, a
stride of 2, and ReLU nonlinearity.

2. PrimaryCaps layer with $$B = 32$$ feature maps

3. ConvCaps1 layer with 3 &times; 3 kernel, $$C = 32$$ feature maps and a stride of 2

4. ConvCaps2 layer with 3 &times; 3 kernel, $$D = 32$$ feature maps and a stride of 1

5. Final capsule layer with one capsule per output class

The routing procedure is used between each adjacent pair of capsule layers. For
convolutional capsules, each capsule in the parent layer sends feedback only to
capsules within its receptive field in the child layer

[1]: <https://openreview.net/pdf?id=HJWLfGWRb> "Matrix Capsules with EM Routing"
[2]: <https://arxiv.org/pdf/1710.09829.pdf> "Dynamic Routing Between Capsules"
[3]: <https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm> "Expectation-Maximization Algorithm"