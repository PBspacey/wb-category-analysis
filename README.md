# App for product picture and description market potential evaluation

In this repo you can find the packed application, that is supposed to help entrepreneurs to make more efficient and attractive descriptioins. 

## How it works? 

The engine of the app is composed of two separate machine learning pipelines: 
- Computer vision pipeline (image classification)
- Natural language processing pipeline (description classification)

At the end output of both pipelines combined to receive the evaluation of the picture and description simultaneously

<b>CV pipeline</b> 

ResNet-34 is used for image classification. This network is modified with fully connected layer enchancement: added some layers with dropouts.

<b>NLP pipeline</b>

Doc2Vec as embedding extractor and CatBoost Classifier for classification. 

## Training process 

For the training images and descriptions were parsed from russian marketplaces, then they were labeled as attractive and non-attractive by [Toloka](https://toloka.ai/tolokers/ru/) users. <b>Only tea data was parsed</b> and models were trainde only on this data, so for another specific purpose it is recommended to train models for specific product.

## Models quality 

- CV: Accuracy 0.83, F1 0.82, ROC-AUC 0.90
- NLP: Accuracy 0.77, F1 0.78, ROC-AUC 0.83

## How to launch the app? 
There are two ways to launch the app: 
1. Run api.py and go to your localhost in browser
2. Use [Docker](https://www.docker.com/)

For the Docker launch here are the next steps: 
1. Run docker daemon
2. Run ```init.sh``` and wait till the image and container are built
3. Run ```start.sh```
4. Go to localhost port that you specified in app.py, by default it is 4422 (open http://localhost:4422/ in your browser)

Enjoy:)
