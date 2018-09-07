---
layout: post
title: "Multiclass Logistic Regression in Julia&mdash;with TensorFlow"
summary: "A Julia program that finds polynomial logistic models for three classes using TensorFlow."
date:   2018-06-28 06:09:00
---

In an [earlier post](/2018/06/22/logistic-regression-julia) you saw a program
that used gradient descent to find polynomial logistic models for three classes.
That program included a `Cost()` function written in Python as well as the
(handwritten) function `DCostDTheta()` that calculated the partial derivative
with respect to any element of $$\vec{\theta}$$.

Below, you will see the same program written using TensorFlow. Let's look at
how the cost function is defined and how the partial derivative function is
automatically generated.

First, be sure you have run `Pkg.add("TensorFlow")` or otherwise installed
the library so that you can begin `using` it.

The creation of the graph begins with the instantiation of `placeholder` objects.

<pre data-enlighter-language="julia" data-enlighter-lineoffset="56">
exampleInput = TensorFlow.placeholder(Float64, shape=[nothing, length(trainingExamples[1].featureVector)])
exampleOutput = TensorFlow.placeholder(Float64, shape=[nothing, length(trainingExamples[1].outputVector)])
</pre>

When the graph is executed, the placeholders will be assigned the 5-value input
and 3-value output vectors from the list of examples. The assignment of
placeholders to lists of actual values is made in a _feed dictionary:_

<pre data-enlighter-language="julia" data-enlighter-lineoffset="59">
feeds = Dict(
  exampleInput => [trainingExamples[i].featureVector[j] for i=1:length(trainingExamples), j=1:length(trainingExamples[1].featureVector)],
  exampleOutput => [trainingExamples[i].outputVector[j] for i=1:length(trainingExamples), j=1:length(trainingExamples[1].outputVector)]
)
</pre>

$$\vec{\theta}$$ is defined as a `Variable` matrix in the graph, initially
composed of zeroes:

<pre data-enlighter-language="julia" data-enlighter-lineoffset="69">
theta = TensorFlow.Variable(TensorFlow.zeros(thetaShape))
</pre>

The following lines look a lot like we are calculating a value of the model and
a cost---but don't be fooled! In reality, these lines only extend the graph to calculate the model value
and the cost from the example input, example output, and $$\vec{\theta}$$
defined above. The actual calculation will happen later, during execution of the
graph.

<pre data-enlighter-language="julia" data-enlighter-lineoffset="71">
model = 1.0 / (1.0 + TensorFlow.exp(TensorFlow.matmul(exampleInput, theta)))
cost = -1.0 / length(trainingExamples) * TensorFlow.reduce_sum(TensorFlow.multiply(exampleOutput, TensorFlow.log(model)) + TensorFlow.multiply((1 - exampleOutput), TensorFlow.log(1 - model)))
</pre>

Similarly, the following lines extend the graph to determine the
gradients of the cost function with respect to $$\vec{\theta}$$ and then update
`theta`. The `gradients()` function derives the partial derivatives of the cost
function and extends the graph to compute them.

Note that we don't write something like `theta -= TensorFlow.multiply(...)`. `theta` is a Python
variable referring to a
matrix in the graph. We don't want to re-assign `theta` at this point. We want to extend the
graph so that during execution, the value of the matrix is updated. `updateTheta`
refers to the portion of the graph that does this.

<pre data-enlighter-language="julia" data-enlighter-lineoffset="74">
calculateGradients = TensorFlow.gradients(cost, theta)
updateTheta = TensorFlow.assign(theta, theta - TensorFlow.multiply(learningRate, calculateGradients))
</pre>

The graph will execute in the context of a `Session`. We instantiate the
`Session` and initialize any global variables in the graph:

<pre data-enlighter-language="julia" data-enlighter-lineoffset="77">
sess = TensorFlow.Session()
run(sess, TensorFlow.global_variables_initializer())
</pre>

Finally, we are ready to _execute_ the graph. The following line executes the
portion of the graph referred to by `cost`, feeding the examples in through the
placeholders defined earlier:

<pre data-enlighter-language="julia" data-enlighter-lineoffset="79">
println("Starting cost: $(run(sess, cost, feeds))")
</pre>

`run()` returns the result of the execution, which in this case is the
initial cost, when all $$\vec{\theta}$$ values are initialized to zero.

The following lines execute the portion of the graph that calculates the
gradients and the portion that updates $$\vec{\theta}$$. We could ignore or discard the return
values, because the execution has already updated the $$\vec{\theta}$$ matrix.
But we need the values in `gradients` to know when to stop iterating. Also, it
helps debugging to keep and print the return values.

<pre data-enlighter-language="julia" data-enlighter-lineoffset="87">
gradients = run(sess, calculateGradients, feeds)
newTheta = run(sess, updateTheta, feeds)
</pre>

You can run the complete program below, take the `theta` values it produces, and
enter them [here](/2018/06/22/logistic-regression-julia#entry-table) to verify
that it has fit logistic models to the three classes of data.

<script src="https://gist.github.com/mspandit/ec5cefb9e86db80ab445e730d993a58f.js"></script>
