---
layout: post
title: "Cloud AI Service Survey"
summary: "A comparison of artificial intelligence capabilities provided by cloud service providers."
date:   2018-09-13 14:41:00
---

This is a survey of artificial intelligence capabilities provided by Amazon
Web Services, Google Cloud, IBM, and Microsoft.

# Automatic Machine Learning

## [Google Cloud Auto ML](https://cloud.google.com/automl/)

# Machine Learning Model Training and Deployment

## [Amazon SageMaker](https://aws.amazon.com/sagemaker/?nc2=h_a1)

Jupyter Notebook, API

Amazon SageMaker is an online environment for defining, training, testing, and
deploying machine learning models. It gives you a Jupyter notebook from which
to do development, and a library to import. The library provides 

* good integration with Amazon's Elastic Cloud Compute (EC2) service so that as
  your models can be run on a variety of hardware and software infrastructures,
  whether during development or deployment. 
  
* hyperparameter tuning, so that you need not resort to brute-force grid
  searches through the space of hyperparameters
  
* good integration with Amazon's Simple Storage Service (S3), where many data
  scientists store training and testing data anyway.
  
* a number of standard machine learning algorithms, but you can also develop
  your own using TensorFlow or MxNet.

## [Amazon Machine Learning](https://aws.amazon.com/aml/?nc2=h_m1)

Web Application, API

For a lightweight introduction to machine learning, there is Amazon Machine
Learning. You specify that it should import data from AWS data sources
including S3, Redshift, or RDS. You get some visual tools for previewing the
data.

You specify one of the columns in your data as a _target attribute_ that the
system will learn to predict. It automatically divides your data into a
training set and a test set. It uses the training set to train the model, and
then tells you how the model did on the test set, and lets you set a prediction
threshold. You need not deal with any complexities of the model itself.

Once you're happy with the model, you can deploy it for real-time (on-demand)
predictions through the web interface, or for batch prediction on data in a
file or in S3.

## [Google Cloud Machine Learning (ML) Engine](https://cloud.google.com/ml-engine/)

Command-line interface, Tensorboard

Google Cloud ML Engine includes freely downloadable components for developing
machine learning models on a development system. The models can use
scikit-learn, XGBoost, Keras, or TensorFlow. Once your models are running
locally, you can copy your data into the cloud, and train your model on a cloud
instance or in distributed fashion across multiple cloud instances.

Cloud ML Engine can also run in a mode that tunes hyperparameters on your model.

Once the model is trained, you can deploy it to perform prediction on new data.
Cloud ML Engine supports "online" prediction via a REST API, or batch
prediction.

## [IBM Machine Learning](https://console.bluemix.net/catalog/services/machine-learning)

Command-line interface, REST API


## [IBM Watson Studio](https://console.bluemix.net/catalog/services/data-science-experience)

Web application

IBM Watson Studio lets you upload data, cleanse and refine it, and visualize it
to discover patterns and trends.

Jupyter notebooks or RStudio let you analyze the data.

Built-in models let you classify image or natural language data. A graphical 
model builder lets you define a Spark ML model. 

The service lets you run experiments in parallel and automates evaluation of 
model performance under various hyperparameter configurations.

It lets you accelerate training by distributing models across multiple servers
and using multiple GPUs.

# Image Processing (Computer Vision)

## [Google Cloud Vision](https://cloud.google.com/vision/)

REST API

When you submit an image through its REST API, Google Cloud Vision 
* classifies it into thousands of categories, providing scores for the most likely ones, 
* detects faces within it, 
* detects topical entities including celebrities and logos,
* determines the likelihood of several types of inappropriate content, and 
* reads printed words contained within it

Google Cloud AutoML Vision lets you upload images and labels and uses this data
to train a recognition model. There is also an option to upload images and have
human beings label them. 

## [Amazon Rekognition](https://aws.amazon.com/rekognition/?nc2=h_a1)

REST API

When you submit an image through its REST API, Amazon Rekognition will identify
objects, celebrities, text, and activities, as well as detect any inappropriate
content. It also provides face recognition and analysis (sex, eyes open/closed,
glasses, facial hair, happiness and age range).

## [Microsoft Azure Computer Vision](https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/)

## [Microsoft Azure Custom Vision](https://azure.microsoft.com/en-us/services/cognitive-services/custom-vision-service/)

## [Microsoft Azure Face](https://azure.microsoft.com/en-us/services/cognitive-services/face/)

## [Microsoft Azure Content Moderator](https://azure.microsoft.com/en-us/services/cognitive-services/content-moderator/)

## [IBM Visual Recognition](https://console.bluemix.net/catalog/services/visual-recognition)

# Video Intelligence (Computer Vision)

## [Google Cloud Video Intelligence](https://cloud.google.com/video-intelligence/)

## [Amazon Rekognition](https://aws.amazon.com/rekognition/?nc2=h_a1)

REST API

When you submit a video through its REST API, Amazon Rekognition will identify
objects, people, their paths, celebrities, scenes, and activities, as well as
detect any inappropriate content. It also provides face recognition and
analysis (sex, eyes open/closed, glasses, facial hair, happiness and age range).

## [Microsoft Azure Video Indexer](https://azure.microsoft.com/en-us/services/media-services/video-indexer/)

## [Microsoft Azure Content Moderator](https://azure.microsoft.com/en-us/services/cognitive-services/content-moderator/)

# HR Hiring

## [Google Cloud Talent Solution](https://cloud.google.com/solutions/talent-solution/)

# Natural Language Intent Classification

## [Google Dialogflow Enterprise Edition](https://cloud.google.com/dialogflow-enterprise/)

## [Amazon Lex](https://aws.amazon.com/lex/details/)

## [Microsoft Azure Language Understanding](https://azure.microsoft.com/en-us/services/cognitive-services/language-understanding-intelligent-service/)

## [IBM Watson Assistant](https://console.bluemix.net/catalog/services/watson-assistant-formerly-conversation)

## [IBM Natural Language Classifier](https://console.bluemix.net/catalog/services/natural-language-classifier)

## [Facebook Wit.ai](https://wit.ai/)

# Natural Language Entity Recognition

## [Google Cloud Natural Language](https://cloud.google.com/natural-language/)

## [Amazon Comprehend](https://aws.amazon.com/comprehend/?nc2=h_a1)

## [Microsoft Azure Text Analytics](https://azure.microsoft.com/en-us/services/cognitive-services/text-analytics/)

## [IBM Natural Language Understanding](https://console.bluemix.net/catalog/services/natural-language-understanding)

# Natural Language Sentiment Analysis

## [Google Cloud Natural Language](https://cloud.google.com/natural-language/)

## [Amazon Comprehend](https://aws.amazon.com/comprehend/?nc2=h_a1)

## [Microsoft Azure Content Moderator](https://azure.microsoft.com/en-us/services/cognitive-services/content-moderator/)

## [Microsoft Azure Text Analytics](https://azure.microsoft.com/en-us/services/cognitive-services/text-analytics/)

## [IBM Natural Language Understanding](https://console.bluemix.net/catalog/services/natural-language-understanding)

# Natural Language Syntactic Parsing

## [Google Cloud Natural Language](https://cloud.google.com/natural-language/)

## [Amazon Comprehend](https://aws.amazon.com/comprehend/?nc2=h_a1)

# Natural Language Content Categorization

## [Google Cloud Natural Language](https://cloud.google.com/natural-language/)

## [Amazon Comprehend](https://aws.amazon.com/comprehend/?nc2=h_a1)

## [IBM Natural Language Understanding](https://console.bluemix.net/catalog/services/natural-language-understanding)

# Natural Language Identification

## [Microsoft Azure Text Analytics](https://azure.microsoft.com/en-us/services/cognitive-services/text-analytics/)


# Natural Language Knowledge Extraction

## [Microsoft Azure QnA Maker](https://azure.microsoft.com/en-us/services/cognitive-services/directory/vision/)

# Speech Recognition (Speech-to-Text)

## [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text/)

## [Amazon Lex](https://aws.amazon.com/lex/details/)

## [Amazon Transcribe](https://aws.amazon.com/transcribe/?nc2=h_m1)

## [Microsoft Azure Speech-to-Text](https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/)

## [IBM Speech to Text](https://console.bluemix.net/catalog/services/speech-to-text)

# Speech Synthesis (Text-to-Speech)

## [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech/)

## [Amazon Polly](https://aws.amazon.com/polly/?nc2=h_a1)

## [Microsoft Azure Text to Speech](https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/)

## [IBM Text to Speech](https://console.bluemix.net/catalog/services/text-to-speech)

# Speaker Identification

## [Microsoft Azure Speaker Recognition](https://azure.microsoft.com/en-us/services/cognitive-services/speaker-recognition/)

# Natural Language Translation

## [Google Cloud Translation](https://cloud.google.com/translate/)

## [Amazon Translate](https://aws.amazon.com/translate/?nc2=h_m1)

## [Microsoft Azure Speech Translation](https://azure.microsoft.com/en-us/services/cognitive-services/speech-translation/)

## [Microsoft Azure Text Translation](https://azure.microsoft.com/en-us/services/cognitive-services/translator-text-api/)

## [IBM Language Translator](https://console.bluemix.net/catalog/services/language-translator)
