---
layout: post
title: "Neural Networks"
summary: "An introduction to neural networks and associated terminology."
date:   2018-07-04 17:30:00
---

Multi-layer perceptrons are in a class of machine learning models called
**neural networks.** The term arose among early computer scientists who
understood that vast numbers of highly-interconnected neurons comprised
mammalian brains. They envisioned the benefits of simulating the operation of
neurons in computers. Indeed, we are now seeing the power of neural networks to
solve problems recently considered intractable. However, modern computer
scientists do not claim that neural networks simulate brains with great
fidelity.

[<img src="/images/Neuron.png" />](https://en.wikipedia.org/wiki/Neuron)

In neural networks for machine learning, a <span id="neuron">**neuron**</span>
refers to a model that composes a linear combination of inputs with a nonlinear
function. The logistic regression model is a simple neuron, but other nonlinear
<span id="activation-functions">**activation functions**</span> can be used for
various applications. The parameters $$\vec{\theta}$$ are usually called the
<span id="weights">**weights**</span> of the model, because the linear
combination is a weighted sum of the inputs.

Neural networks can solve difficult problems with high accuracy when numerous
neurons are organized in layers. The [muli-layer
perceptron](/2018/07/01/multi-layer-perceptrons) is a simple example, having a
feature layer and an output layer. Layers between the input and output are
often called "hidden layers." With notable exceptions, each layer generates
output from values in the previous layer. Such networks are therefore called
"feedforward neural networks."

The number of layers, the number of neurons in each layer, and the choice of
nonlinear functions are all **hyperparameters** of a neural network and
comprise its **architecture** or **topology**.

The process of calculating the output of a neural network from a given input
is frequently called <span id="forward-propagation">**forward propagation,**</span> because calculations flow forward
from the inputs, through intermediate layers, to the output.

The process of adjusting the parameters during training is frequently called
**backward propagation** or "backprop," because calculations can be envisioned
to start with differences between the model output and the training output, and
then flow backward.

Neural networks with three or more layers are called "deep neural networks."
They were time consuming to study and train before the advent of modern
computers and fast linear algebra libraries, because of the large number of
calculations involved. However, it is deep neural networks that have spawned
resurgent interest in artificial intelligence by their ability to solve
computer vision, speech recognition and other types of problems.

