---
layout: post
title: "The Google Inception Network"
summary: ""
date:   2019-01-28 11:31:00
---

# [Going Deeper with Convolutions](https://arxiv.org/abs/1409.4842)

Starting with LeNet-5 [10], convolutional neural networks (CNN) have typically
had a standard structure – stacked convolutional layers (optionally followed by
contrast normalization and maxpooling) are followed by one or more
fully-connected layers.

The most straightforward way of improving the performance of deep neural
networks is by increasing their size. This includes both increasing the depth –
the number of levels – of the network and its width: the number of units at
each level. This is as an easy and safe way of training higher quality models,
especially given the availability of a large amount of labeled training data.
However this simple solution comes with two major drawbacks. Bigger size
typically means a larger number of parameters, which makes the enlarged network
more prone to overfitting, especially if the number of labeled examples in the
training set is limited.

Another drawback of uniformly increased network size is the dramatically
increased use of computational resources. For example, in a deep vision
network, if two convolutional layers are chained, any uniform increase in the
number of their filters results in a quadratic increase of computation. If the
added capacity is used inefficiently (for example, if most weights end up to be
close to zero), then a lot of computation is wasted

The fundamental way of solving both issues would be by ultimately moving from
fully connected to sparsely connected architectures, even inside the
convolutions. Besides mimicking biological systems, this would also have the
advantage of firmer theoretical underpinnings due to the groundbreaking work of
Arora et al. [2]. Their main result states that if the probability distribution
of the data-set is representable by a large, very sparse deep neural network,
then the optimal network topology can be constructed layer by layer by
analyzing the correlation statistics of the activations of the last layer and
clustering neurons with highly correlated outputs. Although the strict
mathematical proof requires very strong conditions, the fact that this
statement resonates with the well known Hebbian principle – neurons that fire
together, wire together – suggests that the underlying idea is applicable even
under less strict conditions, in practice.

This raises the question whether there is any hope for a next, intermediate
step: an architecture that makes use of the extra sparsity, even at filter
level, as suggested by the theory, but exploits our current hardware by
utilizing computations on dense matrices. The vast literature on sparse matrix
computations (e.g. [3]) suggests that clustering sparse matrices into
relatively dense submatrices tends to give state of the art practical
performance for sparse matrix multiplication.

The main idea of the Inception architecture is based on finding out how an
optimal local sparse structure in a convolutional vision network can be
approximated and covered by readily available dense components.

A Python implementation is available [here](https://github.com/tensorflow/models/blob/master/research/slim/nets/inception_v1.py).