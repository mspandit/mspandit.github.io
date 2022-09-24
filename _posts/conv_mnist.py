import argparse
import sys

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

FLAGS = None


def deepnn(example_input):
    def conv2d(x, W):
      """conv2d returns a 2d convolution layer with full stride."""
      return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


    def max_pool_2x2(x):
      """max_pool_2x2 downsamples a feature map by 2X."""
      return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                            strides=[1, 2, 2, 1], padding='SAME')


    def weight_variable(shape):
      """weight_variable generates a weight variable of a given shape."""
      return tf.Variable(tf.truncated_normal(shape, stddev=0.1))


    def bias_variable(shape):
      """bias_variable generates a bias variable of a given shape."""
      return tf.Variable(tf.constant(0.1, shape=shape))

    example_image = tf.reshape(example_input, [-1, 28, 28, 1])

    # First convolutional layer - maps one grayscale image to 32 feature maps.
    thetas_conv1 = weight_variable([5, 5, 1, 32])
    theta0_conv1 = bias_variable([32])
    activation_conv1 = tf.nn.relu(conv2d(example_image, thetas_conv1) + theta0_conv1)

    # Pooling layer - downsamples by 2X.
    activation_pool1 = max_pool_2x2(activation_conv1)

    # Second convolutional layer -- maps 32 feature maps to 64.
    thetas_conv2 = weight_variable([5, 5, 32, 64])
    theta0_conv2 = bias_variable([64])
    activation_conv2 = tf.nn.relu(conv2d(activation_pool1, thetas_conv2) + theta0_conv2)

    # Second pooling layer.
    activation_pool2 = max_pool_2x2(activation_conv2)

    # Fully connected layer 1 -- after 2 round of downsampling, our 28x28 image
    # is down to 7x7x64 feature maps -- maps this to 1024 features.
    thetas_fc1 = weight_variable([7 * 7 * 64, 500])
    theta0_fc1 = bias_variable([500])

    activation_pool2_flat = tf.reshape(activation_pool2, [-1, 7 * 7 * 64])
    activation_fc1 = tf.nn.relu(tf.matmul(activation_pool2_flat, thetas_fc1) + theta0_fc1)

    # Map the 1024 features to 10 classes, one for each digit
    thetas_fc2 = weight_variable([500, 10])
    theta0_fc2 = bias_variable([10])

    return tf.matmul(activation_fc1, thetas_fc2) + theta0_fc2


if __name__ == '__main__':
    # Import data
    mnist = input_data.read_data_sets("/tmp/mnist_data", one_hot=True)

    # Create the model
    example_output = tf.placeholder(tf.float32, [None, 10])
    example_input = tf.placeholder(tf.float32, [None, 784])
    model_output = deepnn(example_input)

    cross_entropy = tf.reduce_mean(
      tf.nn.softmax_cross_entropy_with_logits(labels=example_output, logits=model_output))
    train_step = tf.train.GradientDescentOptimizer(5e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(model_output, 1), tf.argmax(example_output, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(20000):
          batch = mnist.train.next_batch(128)
          if i % 100 == 0:
            train_accuracy = accuracy.eval(feed_dict={
                example_input: batch[0], example_output: batch[1]})
            print('step %d, training accuracy %g' % (i, train_accuracy))
          train_step.run(feed_dict={example_input: batch[0], example_output: batch[1]})

        print('test accuracy %g' % accuracy.eval(feed_dict={
            example_input: mnist.test.images, example_output: mnist.test.labels}))
