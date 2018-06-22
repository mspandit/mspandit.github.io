---
layout: post
title: "Feature Scaling Caution"
summary: "Scaling inputs and features can help speed convergence with gradient descent."
date:   2018-06-22 09:10:00
---

In the last two posts, we looked at implementations of polynomial logistic
regression using gradient descent for 30 examples, each with two inputs $$x_1$$
and $$x_2$$ and each in one of three classes.

The five terms in the feature vector correspond to the constant and the
polynomial coefficients for $$x_1$$, $$x_2$$, $$x_1^2$$ and $$x_2^2$$
respectively.

If you looked closely at the [Python](/2018/06/14/logistic-regression-python)
or [Julia](/2018/06/22/logistic-regression-julia) code that implemented
multi-class logistic regression, you may have noticed some math in the feature
vector for each example. The feature vector took each input, subtracted 50, and
then divided by 50:

**Python**
```
self.feature_vector = numpy.array([[1], [(x1 - 50) / 50.0], [(x2 - 50) / 50.0], [((x1 - 50) / 50.0) ** 2], [((x2 - 50) / 50.0) ** 2]])
```

**Julia**
```
  [[1.0], [(x1 - 50.0) / 50.0], [(x2 - 50.0) / 50.0], [((x1 - 50.0) / 50.0)^2], [((x2 - 50.0) / 50.0)^2]],   
```

The reason for this is that gradient descent converges _faster when all the
features are within a similar range._

The inputs $$x_1$$ and $$x_2$$ were in the range 0--100. Therefore, the
features $$x_1^2$$ and $$x_2^2$$ would have been in the range 0--10,000. If we
had used these without modification, then the cost function would have looked
like a long narrow channel. To properly move across the width of the channel
would have required a very small learning rate, and to find the minimum pont
along the length of the channel would have taken many iterations.

By subtracting 50 and dividing by 50, we ensured that all features were in the
range -1 and 1. This is called **feature scaling** and it makes the cost
function look more like a shallow bowl. We can use a much larger learning rate
and find the minimum of the cost function in a much smaller number of
iterations.

You might be concerned that the $$\theta$$ values you end up with are trained
from different examples than the set you started with. However, it is a simple
matter to scale _any_ input in the same way you scaled the examples, and use
these $$\theta$$ values to get the correct classification results.

Try replacing one of the features with the unmodified input, and then run the
program again. You will see that the cost explodes---the model diverges. You
will have to reduce the learning rate, possibly by several orders of magnitude.
By the time you get the model to converge, it will require many more iterations
to do so.
