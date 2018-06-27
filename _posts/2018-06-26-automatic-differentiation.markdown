---
layout: post
title: "Automatic Differentiation with TensorFlow"
summary: "<a href='https://www.tensorflow.org/'>TensorFlow</a> is a fast, efficient open source library that can <em> automatically generate partial derivative functions from the definition of a complex cost function.</em>"
date:   2018-06-26 13:23:00
---

You may have noticed a recurring pattern in how we have approached machine
learning problems:

1. We assume a model of appropriate complexity, having parameters
  $$\vec{\theta}$$.

2. We define a cost function that is minimized when the $$\vec{\theta}$$ values
  best fit the model to the training data.

3. We find the partial derivative functions of the cost function, with respect
  to the parameters $$\vec{\theta}$$.

4. Starting with some initial values of the parameters, we calculate the
  gradients (the values of the partial derivative functions) and use the
  gradients to update the parameters.

As we look at models of increasing complexity, with increasing numbers of input
variables and parameters, it becomes difficult to find the partial
derivatives of cost functions with respect to the parameters. Fortunately, the open
source community has produced fast, efficient libraries that can _automatically
generate partial derivative functions from the definition of a complex cost
function._ One of these is maintained by Google engineers and it is called
[TensorFlow](https://www.tensorflow.org/).

The power of TensorFlow is rooted in your ability to represent a cost function
(or any other function) as an _operation graph._ An operation graph decomposes
a complex function into simpler operations. Nodes represent values or operators.
Vertices represent the flow of values into operations and the flow of results
out of operations.

As you can imagine, from such a representation of a cost function, it is
possible automatically to derive the graph representations of partial derivative
functions. The representation also yields another important benefit: For a large,
complex function composed of numerous simpler operations, it becomes possible to
distribute those operations
across multiple computers. Furthermore, in a single computer, specific
operations can be assigned to a GPU or other application-specific processor.
The result is fast, parallel execution of the function.

Unfortunately, this power comes at a cost to the data scientist: instead of
simply writing a function as, say, Python or Julia code and then executing that code,
you must write code that first represents the function as a graph and then _executes
the graph._ In the next post, we'll see how this is done.
