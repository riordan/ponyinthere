#Takes Twitter archive CSV and grabs all source tweets


import csv
import redis
from markov.markov import add_line_to_index
from markov import Markov
import re


def setup():

  GRUBER = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

  corpus = []
  with open ('tweets/tweets.csv', 'rb') as tweesv:
    tweetreader = csv.reader(tweesv, delimiter=',', quotechar='"')
    for row in tweetreader:
      if not row[6] and not row[5].startswith('RT @') and not row[5].startswith('rt @') and not row[5].startswith('@'):
        tweettext = row[5]
        for url in GRUBER.findall(tweettext):
          tweettext=tweettext.replace(url[0],'')
      
        corpus.append(tweettext)

  client = redis.Redis()
  twitter_data = Markov(prefix="twitter")
  for tweet in corpus:
    add_line_to_index(tweet.split(), client, prefix="tweets")

#tweet_data.client=client

def newTweet():
    tweet_data = Markov(prefix="tweets")
    tweetline = tweet_data.generate()
    tweet = ""
    for word in tweetline:
        tweet += word + " "
    
    tweet = tweet.rstrip()
    
    if len(tweet)>140:
        return newTweet()
    else:
        return tweet


