# -*- coding: utf-8 -*-
"""twitterapi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Lfwbl56enlwzLOqeZQeaPezwLePP3QQ_
"""

import os
#os.chdir("drive/My Drive/sentiment")

#nltk.download('punkt')
from statistics import mode

from nltk.classify import ClassifierI
import nltk
class VoteClassifier(ClassifierI):
  def __init__(self, *classifiers):
    self._classifiers = classifiers
  def classify(self, features):
    votes = []
    for classifier in self._classifiers:
      vote = classifier.classify(features)
      votes.append(vote)
      return mode(votes)
  def confidence(self, features):
    votes = []
    for classifier in self._classifiers:
      vote = classifier.classify(features)
      votes.append(vote)
      return votes.count(mode(votes)) / len(votes)

import pickle

pickle_loader = open("BernoulliNB.pickle","rb") 
bernoulli = pickle.load(pickle_loader)

pickle_loader = open("Logistic.pickle","rb") 
logistic = pickle.load(pickle_loader)

pickle_loader = open("MultiNB.pickle","rb") 
multi = pickle.load(pickle_loader)

pickle_loader = open("NaiveBayes.pickle","rb") 
naive = pickle.load(pickle_loader)

pickle_loader = open("SGD.pickle","rb") 
sgd = pickle.load(pickle_loader)

pickle_loader = open("word_features.pickle","rb") 
word_features = pickle.load(pickle_loader)

def get_features(doc):
  word_set = set(nltk.word_tokenize(doc))
  features = {}
  for word in word_features:
    features[word] = (word in word_set)
  return features

voted_classifier = VoteClassifier(sgd, logistic, bernoulli, multi, naive)
# review = "This movie was amazing. Would recommend to Everyone"
# print(f"Class : {voted_classifier.classify(get_features(review))}")
# print(f"Confidence : {voted_classifier.confidence(get_features(review))}")

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
TOPIC = "messi"


ckey=""
csecret=""
atoken=""
asecret=""

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)

        tweet = all_data["text"]
        sentiment = voted_classifier.classify(get_features(tweet))
        conf = voted_classifier.confidence(get_features(tweet))
        #print(tweet, sentiment)
        if conf > 0.8 :
          fil = open("sentiment-twitter.txt", "a")
          fil.write(sentiment)
          fil.write("\n")
          fil.close()
        
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=[TOPIC], languages=["en"])

