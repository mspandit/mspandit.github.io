---
layout: post
title: "R-CNN for Object Detection"
summary: ""
date:   2019-01-27 11:31:00
---

# R-CNN

[Rich Feature Hierarchies for Accurate Object Detection and Semantic
Segmentation](https://arxiv.org/pdf/1311.2524.pdf)

our method generates around 2000 category-independent region proposals for the
input image, extracts a fixed-length feature vector from each proposal using a
CNN, and then classifies each region with category-specific linear SVMs. Since
our system combines region proposals with CNNs, we dub the method R-CNN:
Regions with CNN features.

Our object detection system consists of three modules. The first generates
category-independent region proposals. These proposals define the set of
candidate detections available to our detector. The second module is a large
convolutional neural network that extracts a fixed-length feature vector from
each region. The third module is a set of classspecific linear SVMs.

we use selective search to enable a controlled comparison with prior
detection work

We extract a 4096-dimensional feature vector from each region proposal using
the Caffe [24] implementation of the CNN described by Krizhevsky et al.

R-CNN first finetunes a ConvNet on object proposals using log loss. Then, it
fits SVMs to ConvNet features. These SVMs act as object detectors, replacing
the softmax classifier learnt by fine-tuning. In the third training stage,
bounding-box regressors are learned.

For SVM and bounding-box regressor training, features are extracted from each
object proposal in each image and written to disk. With very deep networks,
such as VGG16, this process takes 2.5 GPU-days for the 5k images of the VOC07
trainval set. These features require hundreds of gigabytes of storage.

At test-time, features are extracted from each object proposal in each test
image. Detection with VGG16 takes 47s / image (on a GPU).

R-CNN is slow because it performs a ConvNet forward pass for each object
proposal, without sharing computation.

# [Fast R-CNN](https://arxiv.org/pdf/1504.08083.pdf)

We propose a single-stage training algorithm that jointly learns to
classify object proposals and refine their spatial locations.

A Fast R-CNN network takes as input an entire image and a set of object
proposals. The network first processes the whole image with several
convolutional (conv) and max pooling layers to produce a conv feature map.
Then, for each object proposal a region of interest (RoI) pooling layer
extracts a fixed-length feature vector from the feature map. Each feature
vector is fed into a sequence of fully connected (fc) layers that finally
branch into two sibling output layers: one that produces softmax probability
estimates over K object classes plus a catch-all “background” class and another
layer that outputs four real-valued numbers for each of the K object classes.
Each set of 4 values encodes refined bounding-box positions for one of the K
classes.

The RoI pooling layer uses max pooling to convert the features inside any valid
region of interest into a small feature map with a fixed spatial extent of H ×
W (e.g., 7 × 7), where H and W are layer hyper-parameters that are independent
of any particular RoI. In this paper, an RoI is a rectangular window into a
conv feature map. Each RoI is defined by a four-tuple (r, c, h, w) that
specifies its top-left corner (r, c) and its height and width (h, w).

RoI max pooling works by dividing the h × w RoI window into an H × W grid of
sub-windows of approximate size h/H × w/W and then max-pooling the values in
each sub-window into the corresponding output grid cell. Pooling is applied
independently to each feature map channel, as in standard max pooling.

When a pre-trained network initializes a Fast R-CNN network, it undergoes three
transformations. First, the last max pooling layer is replaced by a RoI pooling
layer that is configured by setting H and W to be compatible with the net’s
first fully connected layer (e.g., H = W = 7 for VGG16). Second, the network’s
last fully connected layer and softmax (which were trained for 1000-way
ImageNet classification) are replaced with the two sibling layers described
earlier (a fully connected layer and softmax over K + 1 categories and
category-specific bounding-box regressors). Third, the network is modified to
take two data inputs: a list of images and a list of RoIs in those images.
