---
layout: post
title: "Dynamic Routing Between Capsules"
summary: "Notes on paper published by Geoffrey Hinton."
date:   2022-12-07 09:52:00
---
# Convolutional Neural Networks

Convolutional layers detect a feature in various positions in an image. The
presence of a feature at a specific position is represented by the activation
of a single neuron in a higher layer.

Pooling implements a kind of _routing:_ A neuron in a higher layer ignores all
but (in the case of max pooling) the most active neuron in a local pool in the
layer below.

# [Dynamic Routing Between Capsules](https://arxiv.org/pdf/1710.09829.pdf)

This paper assumes that the human visual system, composed of multiple layers,
creates a structure resembling a _parse tree_ from its input. The parse tree is
"carved out of a multilayer neural network like a sculpture is carved from a
rock" as described in [this paper][1].

The neurons in each layer are organized in small groups called _capsules,_
introduced in [this paper][2]. Within a capsule, a neuron represents the
presence and properties of an entity in the image:

* position
* size
* orientation
* deformation
* velocity
* albedo
* hue
* texture, etc.

A separate neuron (with logistic output) _could_ be used to represent the
probability that the entity is present in/absent from the image. This is the
approach used in [this paper][3]. However, in this paper, the overall length of
the capsule (magnitude of the vector of activation of neurons in the capsule)
represents the probability of the existence of the entity. (This length is
scaled to the range 0.0--1.0 using a non-linear _squash_ function.) The
orientation of the vector represents the properties of the entity.

Each node in the parse tree corresponds to an active capsule. In an iterative
process involving cooperation between parents and children, each active capsule
"chooses" a capsule in the layer above to be its parent in the tree---thereby
assigning visual parts to wholes.

The connections between children and parents are represented by _coupling
coefficients_ ranging from 0.0 to 1.0. At the beginning of training, a capsule
is routed to all possible parents. This is represented by equal-valued coupling
coefficients for all parents.

Then, for each possible parent, an active capsule computes a _prediction
vector_ by multiplying its own (vector) activation by a weight matrix.

The parents' activations are sums of the child prediction vectors, weighted by
the coupling coefficient. The coupling coefficient for any parent-child pair is
adjusted (for use in the following iteration) based on "agreement" between the
child prediction vector and the parent activation. The "agreement" is simply
computed as the scalar product of the child prediction vector for the parent
and the parent activation. Thus, in the subsequent iteration, children whose
predictions agree with parents get coupling coefficients closer to 1.0, and
children whose predictions disagree with parents get coupling coefficients
closer to 0.0.

In this manner, the prior probabilities that a lower-level capsule should be
coupled to a higher-level capsule get adjusted---and might even be entirely
overridden---by consideration of other regions within the image.

After training, the coupling coefficients represent the prior probabilities
that a lower-level capsule should be the child of a higher-level capsule. (The
probabilities are "prior" in the sense that they are unconditioned on other
regions within the image.)

Routing by agreement replaces max pooling in the selection of lower-level
activations for higher-level activations. [This paper][3] uses a different
algorithm for routing by agreement, and [this paper][4] uses an auto-encoder to
calculate routes.

Because a capsule represents a visual entity or feature, it necessarily
observes a region ("local grid") of the input space. All but the last layer of
capsules are convolutional. This ensures that, as in traditional CNNs,
knowledge of feature detection can be applied across the entire image. Hence,
for low-level capsule layers, the position of an entity is _place-coded,_
represented by activation of one capsule and not others. As in CNNs, higher
level capsules represent larger regions of the image. Within the region of a
capsule, the position (and other attributes) of the entity is
_rate-coded_---represented by the components of the activation vector.

While configuring layers from lower to higher, the dimensionality of each
capsule should increase because

* positional coding shifts from place-coding to rate coding
* higher-level capsules represent more complex entities
* more complex entities have more degrees of freedom

# Loss Function

The paper wants to allow for the presence of _multiple_ digits in the image.
Therefore, it uses a separate margin loss for each digit capsule. The total
loss is the sum of the losses of all digit capsules.

# Architecture

1. 28 &times; 28 pixel grayscale image

2. Convolutional layer. 9 &times; 9 pixel kernels. Stride = 1. 256 feature
maps, each 20 &times; 20 ($$= (28 - 9 + 1) / 1$$)

3. Primary Capsules layer. 9 &times; 9 input kernels. Stride = 2. 256 feature maps, each 6 &times; 6 ($$= (20 - 9 + 1) / 2$$), organized as 32 &times; 8-dimensional capsules

4. Squashing function

5. Routing by agreement

6. DigitCaps layer. 10 &times; 16-dimensional capsules

## Reconstruction Layers

Reconstruction loss is calculated as follows: During training, activity vectors
of capsules for incorrect digits are masked out. This encourages digit capsules
to encode instantiation parameters of the input digit. "The dimensions of a
digit capsule should learn to span the space of variations (stroke thickness,
skew, width) in the way digits of that class are instantiated." The activity
vector of the correct digit is used to reconstruct input image:

1. Fully connected layer with ReLU and 512 outputs

2. Fully connected layer with ReLU and 1024 outputs

3. Fully connected layer with Sigmoid and 784 outputs representing intensity of
28 &times; 28 pixel grayscale image

Calculate sum of squared differences between outputs and actual pixel
intensities.

# Implementations

The "official" implementation in Python with TensorFlow is available [here][5].
See an **annotated Python implementation** [here][6].

[1]: <https://www.cs.toronto.edu/~hinton/absps/nips99ywt.pdf> "Learning to Parse Images"
[2]: <https://www.cs.toronto.edu/~bonner/courses/2022s/csc2547/papers/capsules/transforming-autoencoders,-hinton,-icann-2011.pdf> "Transforming Auto-Encoders"
[3]: <https://openreview.net/pdf?id=HJWLfGWRb> "Matrix Capsules with EM Routing"
[4]: <https://arxiv.org/pdf/1906.06818.pdf> "Stacked Capsule Autoencoders"
[5]: <https://github.com/Sarasra/models/tree/master/research/capsules> "Sarasra's fork of tensorflow/models"
[6]: <https://nn.labml.ai/capsule_networks/index.html> "Capsule Networks"