---
layout: post
title: "Attention is All You Need"
summary: "Notes on paper published by Google Brain."
date:   2022-12-21 15:26:00 -0700
---

[Attention is All You Need][1]

# Introduction

The inherently sequential nature of recurrent neural networks prevent parallel
computing _within_ training examples. Parallel computing remains possible
_across_ training examples---the examples in a batch can be processed
simultaneously even though each example is processed serially. However, as
sequence length grows, this approach consumes too much memory.

Attention mechanisms have allowed modeling of dependencies without regard to
their distance in the input sequence (for an encoder) or the output sequence
(for a decoder). Such mechanisms are usually used with a recurrent network.

The Transformer model architecture relies entirely on attention to draw global
dependencies between input and output. Because it eschews recurrence, it allows
for significantly more parallel computation.

# Model Architecture

The Transformer model architecture follows the overall architecture of neural
sequence-to-sequence models:

* An encoder maps a sequence of symbols $$(x_1, x_2, ..., x_n)$$ to a sequence
of continuous representations $$(z_1, z_2, ..., z_n)$$

```python
class Encoder(object):
    def forward(symbols):
        continuous_representations = []
        for symbol in symbol:
            # ...
            continuous_representations.append(continuous_representation)
        return continuous_representations
```

* A decoder maps $$(z_1, z_2, ..., z_n)$$ to an output sequence $$(y_1, y_2,
..., y_m)$$

```python
class Decoder(object):
    def forward(continuous_representations):
        output_sequence = []
        for continuous_representation in continuous_representations:
            # ...
            output_sequence.append(output)
        return output_sequence
```

* At each step, the model is _autoregressive,_ it consumes the
previously-generated symbols as additional input when generating the next

## Encoder and Decoder Stacks

### Encoder 

The encoder is composed of a stack of $$N = 6$$ identical layers. Each layer
has two sub-layers:

* Multi-Head Self Attention. See an **annotated Python implementation**
[here](https://nn.labml.ai/transformers/mha.html).

* Position-Wise Fully Connected Feed-Forward Network

There is a residual connection [2] around each sub-layer followed by layer
normalization [3]. See an **annotated Python implementation** of layer normalization [here](https://nn.labml.ai/normalization/layer_norm/index.html) In other words, the output of each sub-layer is

$$ LayerNorm(x + Sublayer(x)) $$

where $$Sublayer()$$ is either Multi-Head Self Attention or Position-Wise Fully
Connected Feed-Forward Network.

All sub-layers produce output of dimension $$d_{model} = 512$$.

```python
class MultiHeadSelfAttention(EncoderLayer):
    def forward(x):

class PositionWiseFullyConnectedFeedForward(EncoderLayer):
    def forward(x):

class EncoderLayer(object):
    def __init__():
        self.attention = MultiHeadSelfAttention()
        self.fully_connected = PositionWiseFullyConnectedFeedForward()

    def forward(x):
        intermediate = LayerNorm(x + self.attention.forward(x))
        return LayerNorm(intermediate + self.fully_connected.forward(intermediate)))

class Encoder(object):
    def __init__(number_of_layers_N=6):
        self.stack = [EncoderLayer() for n in range(0, number_of_layers_N)]

    def forward(symbols):
        continuous_representations = []
        for symbol in symbol:
            # ...
            continuous_representations.append(continuous_representation)
        return continuous_representations
```

### Decoder

The decoder is also composed of a stack of $$N = 6$$ identical layers. Each
layer has three sub-layers:

* Masked Multi-Head Self Attention (Multi-Head Self Attention modified to
prevent attending to later positions. This, combined with the fact that the
output embeddings are offset by one position ensure that the predictions for
position $$i$$ can only depend on the known inputs at positions less than
$$i$$.)

* Position-Wise Fully Connected Feed-Forward Network

* Multi-Head Encoder Attention (over the output of the encoder stack)

There is a residual connection [2] around each sub-layer followed by layer
normalization [3]. In other words, the output of each sub-layer is

$$ LayerNorm(x + Sublayer(x)) $$

where $$Sublayer()$$ is either Multi-Head Self Attention, Position-Wise Fully
Connected Feed-Forward Network, or Multi-Head Encoder Attention.

```python
class MaskedMultiHeadSelfAttention(DecoderLayer):
    def forward(x):

class PositionWiseFullyConnectedFeedForward(DecoderLayer):
    def forward(x):

class MultiHeadEncoderAttention(DecoderLayer):
    def forward(x):

class DecoderLayer(object):
    def __init__():
        self.self_attention = MaskedMultiHeadSelfAttention()
        self.fully_connected = PositionWiseFullyConnectedFeedForward()
        self.encoder_attention = MultiHeadEncoderAttention()

    def forward(x):
        intermediate = LayerNorm(x + self.self_attention(x))
        intermediate = LayerNorm(intermediate + self.fully_connected(intermediate))
        return LayerNorm(intermediate + self.encoder_attention(intermediate))

class Decoder(object):
    def __init__(number_of_layers_N=6):
        self.stack = [DecoderLayer() for n in range(0, number_of_layers_N)]

    def forward(continuous_representations):
        output_sequence = []
        for continuous_representation in continuous_representations:
            # ...
            output_sequence.append(output)
        return output_sequence
```

## Attention

An attention function can be described as mapping a query and a set of
key-value pairs to an output. (The query, keys, values, and output are all
vectors.)

```python
def attention(query_vector, key_value_vector_pairs):
    return output_vector
```

In the paper's _Scaled Dot-Product Attention,_ the queries and keys are of
dimension $$d_k$$ and the values are of dimension $$d_v$$.

A sub-function measures the compatibility between a query and a key to generate
a weight. The output of the attention function is the sum, over all the
key-value pairs, of the values multiplied by the weights.

```python
def attention(query_vector, key_value_vector_pairs):
    def sub_function(query, key):
        return weight
    return output_vector
```

In the paper's _Scaled Dot-Product Attention,_ the sub-function computes the
dot product of the query and a key. The authors suspect that, for large values
of $$d_k$$, the dot products grow in magnitude, pushing the softmax function
into regions where it has extremely small gradients. Consequently, they divide
each dot product by $$\sqrt{d_k}$$ and then apply the softmax function to
generate the weight.

```python
def attention(query_vector, key_value_vector_pairs):
    def sub_function(query, key):
        return softmax(dot(query, key) / math.sqrt(DIMENSION_KEY))
    weighted_sum = 0.0
    output_vector = numpy.zeros()
    for key in key_value_vector_pairs.keys:
        output_vector += sub_function(query_vector, key) * key_value_vector_pairs[key]
    return output_vector
```
### Multi-Head Attention

_Multi-Head Attention_ allows the model to "jointly attend to information from
different representation subspaces at different positions."

Instead of performing a single attention function, the authors found it
beneficial to

1. linearly project the queries, values, and keys $$h$$ times with different
(learned) projections,

2. perform the attention function, in parallel, on each of these projected
queries, values, and keys,

3. concatenate the resulting $$d_v$$ dimensional outputs, and

4. linearly project the concatenated outputs with a learned projection

The authors used $$h=8$$ and $$d_v = d_k = d_{model} / h = 64$$

### Applications of Attention

In Multi-Head Encoder Attention sub-layers, the queries come from the prior
decoder layer. The key-value pairs come from the output of the encoder.
Consequently, every decoder position can attend to any position in the input
sequence.

In Multi-Head Self Attention sub-layers, the keys, values, and queries come
from the output of the previous layer in the encoder. Consequently, every
encoder position can attend to any position in the previous layer

In Masked Multi-Head Self Attention sub-layers, each position in the decoder
can attend to all positions in the decoder up to and including its own
position. This masking is implemented in Scaled Dot Product attention by setting all values in the input to the softmax corresponding to illegal connections to $$-\infty$$. 

## Position-Wise Fully Connected Feed-Forward Network

The Position-Wise Fully Connected Feed-Forward Network is applied to each
position separately and identically. This consists of a linear transformation
followed by a ReLU followed by a second linear transformation:

$$ FFN(x) = max(0, xW_1 + b_1)W_2 + b_2 $$

The linear transformations are the same across different positions, allowing
them to be described as **convolutions with kernel size 1**. The input and
output dimensionality is $$d_{model} = 512$$ while the inner layer has
dimensionality $$d_{ff} = 2048$$.

## Embeddings

Learned embeddings convert the input tokens to vectors of dimension $$d_{model}
= 512$$. Learned linear transformations and softmax convert the decoder output
to predicted next-token probabilities.

The same weight matrix is shared between the two embedding layers and the
linear transformation preceding softmax. In the embedding layers, the weights
are multiplied by $$\sqrt{d_{model}}$$.

## Positional Encoding

For the model to make use of the order of the sequence, information about the
relative or absolute position of each token must be injected. Therefore, they
add _positional encodings_ to the input embeddings at the bottoms of the
encoder and decoder stacks. The $$d_{model}$$-dimensional positional encodings
are summed with the embeddings.

For the position $$pos$$ and the dimension $$i$$, the positional encoding is

$$ PE_{(pos, 2i)} = sin(pos/10000^{2i/d_{model}}) $$

$$ PE_{(pos, 2i + 1)} = cos(pos / 10000^{2i/d_{model}}) $$

The authors chose this function because they hypothesized that

* the model would learn to attend by relative position, because for any offset
$$k$$, $$PE_{pos+k}$$ can be represented as a linear function of $$PE_{pos}$$

* the model would extrapolate to sequence lengths longer than those encountered
during training

# Why Self-Attention

1. Total computational complexity. A self-attention layer connects all
positions with a constant number of sequentially executed operations. Contrast
this with a recurrent layer, which requires $$O(n)$$ sequential operations. In
sentence representations used by state of the art models in machine
translation, the sequence length $$n$$ is usually less than the representation
dimensionality $$d$$. In this case, self-attention layers are faster than
recurrent layers.

2. Amount of computation that can be parallelized

3. Path length between long-range dependencies in the network. Signals have to
traverse paths forward and backward in the network. The length of these paths
affects the ability to learn dependencies. The shorter the path between any
input and any output, the easier it is to learn long-range dependencies.

# Code

Available for TensorFlow [here][4] and for PyTorch [here][6] and [here][5].

[1]: <https://arxiv.org/abs/1706.03762> "Attention is All You Need"
[2]: <https://arxiv.org/abs/1512.03385> "Deep Residual Learning for Image Recognition"
[3]: <https://arxiv.org/abs/1607.06450> "Layer Normalization"
[4]: <https://github.com/tensorflow/tensor2tensor> "Tensor2Tensor"
[5]: <https://github.com/tunz/transformer-pytorch> "PyTorch Transformer"
[6]: <https://github.com/huggingface/transformers> "Huggingface Transformers"
