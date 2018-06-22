---
layout: post
title: "Logistic Regression with <em>Multiple</em> Classes"
summary: "The logistic model can be extended to classify its input into one of several classes."
date:   2018-06-12 09:31:00
---

Many useful problems involve classifying an input in one of _multiple_ classes,
for example,

* Is an e-mail spam, work-related, or personal?

* Which numeral between 0 and 9 is shown in an image?

* Which of several thousand words was uttered in a clip of audio?

You might be tempted to handle such problems using a model whose output is an
integer identifying the class. However, a more straightforward approach is to
have a logistic model _for each class_ whose output indicates the probability
that the input is in that class. For a given input, the model that produces the
highest probability corresponds to the predicted class.

It is a simple matter to divide each output by the sum of the outputs. This
ensures that the sum of the probabilities is 1.0. This combination of outputs
is a predicted _probability distribution_ across classes.

In this case, the training data consists of examples $$ (\vec{x}^{(1)},
\vec{y}^{(1)}), (\vec{x}^{(2)}, \vec{y}^{(2)}), \dots, (\vec{x}^{(m)},
\vec{y}^{(m)}) $$ where each $$ \vec{y}^{(i)} $$ is the target probability
distribution---a vector with a 1 corresponding to the expected class and zeroes
elsewhere (conventionally called a **[one-hot <i class="fa
fa-external-link-alt"></i>](https://en.wikipedia.org/wiki/One-hot) vector**).

We can use matrices to keep track of the multiple models. 
Let \\( \vec{\theta} = \\) \` [[\theta_0^{(1)}, \theta_0^{(2)}, ...], [\theta_1^{(1)}, \theta_1^{(2)}, ...]]\` with a column for each class. Then the model equation can be compactly expressed as before:

$$ \vec{y}(\vec{x}) = \frac{1}{\vec{1} + e^{\vec{\theta^T}\times\vec{x}}} $$

The matrices and operations will become clearer in the computer code, but

* $$ \theta^T $$ is a matrix with a row for each class and a column for each input or
feature.

* $$ \theta^T \times \vec{x} $$ is a matrix multiplication operation resulting
  in a row for each class.

* $$ e^{\vec{\theta^T}\times\vec{x}} $$ is an **elementwise** operation,
resulting in a row for each class.

* $$ \vec{1} $$ is a column vector with a 1 for each class, and $$ \vec{1} +
  e^{\vec{\theta^T}\times\vec{x}} $$ is a matrix addition operation, resulting
  in a row for each class.

* $$ \frac{1}{\vec{1} + e^{\vec{\theta^T}\times\vec{x}}} $$ is also an
elementwise operation, resulting in a row for each class.

