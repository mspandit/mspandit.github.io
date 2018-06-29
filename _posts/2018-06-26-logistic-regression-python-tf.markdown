---
layout: post
title: "Multiclass Logistic Regression in Python&mdash;with TensorFlow"
summary: "A Python program that finds polynomial logistic models for three classes using TensorFlow."
date:   2018-06-26 14:32:00
---

In an [earlier post](/2018/06/14/logistic-regression-python) you saw a program
that used gradient descent to find polynomial logistic models for three classes.
That program included a `cost()` function written in Python as well as the
(handwritten) function `d_cost_d_theta()` that calculated the partial derivative
with respect to any element of $$\vec{\theta}$$.

Below, you will see the same program written using TensorFlow. Let's look at
how the cost function is defined and how the partial derivative function is
automatically generated.

First, be sure you have run `pip install numpy tensorflow` or otherwise
installed the libraries so that you can `import` them.

The creation of the graph begins with the instantiation of `placeholder` objects.

{% highlight python %}
example_input = tf.placeholder(tf.float32, [None, len(training_examples[0].feature_vector)])
example_output = tf.placeholder(tf.float32, [None, len(training_examples[0].output_vector)])
{% endhighlight %}

When the graph is executed, the placeholders will be assigned the 5-value input
and 3-value output vectors from the list of examples. The assignment of
placeholders to lists of actual values is made in a _feed dictionary:_

{% highlight python %}
feeds = {
    example_input: [ex.feature_vector for ex in training_examples],
    example_output: [ex.output_vector for ex in training_examples]
}
{% endhighlight %}

$$\vec{\theta}$$ is defined as a `Variable` matrix in the graph, initially
composed of zeroes:

{% highlight python %}
theta = tf.Variable(tf.zeros(theta_shape))
{% endhighlight %}

The following lines look a lot like we are calculating a value of the model and
a cost---but don't be fooled! In reality, these lines only extend the graph to calculate the model value
and the cost from the example input, example output, and $$\vec{\theta}$$
defined above. The actual calculation will happen later, during execution of the
graph.

{% highlight python %}
model = 1.0 / (1 + tf.exp(tf.matmul(example_input, theta)))
cost = -1.0 / len(training_examples) * tf.reduce_sum(tf.multiply(example_output, tf.log(model)) + tf.multiply((1 - example_output), tf.log(1 - model)))
{% endhighlight %}

Similarly, the following lines extend the graph to determine the
gradients of the cost function with respect to $$\vec{\theta}$$ and then update
`theta`. The `gradients()` function derives the partial derivatives of the cost
function and extends the graph to compute them.

Note that we don't write something like `theta -= tf.multiply(...)`. `theta` is a Python
variable referring to a
matrix in the graph. We don't want to re-assign `theta` at this point. We want to extend the
graph so that during execution, the value of the matrix is updated. `update_theta`
refers to the portion of the graph that does this.

{% highlight python %}
calculate_gradients = tf.gradients(xs=theta, ys=cost)[0]
update_theta = theta.assign(theta - tf.multiply(learning_rate, calculate_gradients))
{% endhighlight %}

The graph will execute in the context of a `Session`. We instantiate the
`Session` and initialize any global variables in the graph:

{% highlight python %}
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
{% endhighlight %}

Finally, we are ready to _execute_ the graph. The following line executes the
portion of the graph referred to by `cost`, feeding the examples in through the
placeholders defined earlier:

{% highlight python %}
    print("Starting cost: %s" % sess.run(cost, feed_dict=feeds))
{% endhighlight %}

`Session.run()` returns the result of the execution, which in this case is the
initial cost, when all $$\vec{\theta}$$ values are initialized to zero.

The following lines execute the portion of the graph that calculates the
gradients and the portion that updates $$\vec{\theta}$$. We could ignore or discard the return
values, because the execution has already updated the $$\vec{\theta}$$ matrix.
But we need the values in `gradients` to know when to stop iterating. Also, it
helps debugging to keep and print the return values.
{% highlight python %}
      gradients = sess.run(calculate_gradients, feed_dict=feeds)
      new_theta = sess.run(update_theta, feed_dict=feeds)
{% endhighlight %}


You can run the complete program below, take the `theta` values it produces, and
enter them [here](/2018/06/14/logistic-regression-python#entry-table) to verify
that it has fit logistic models to the three classes of data.

<script src="https://gist.github.com/mspandit/05347025718749feeb7a3c206469c6af.js"></script>
