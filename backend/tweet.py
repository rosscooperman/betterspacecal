#!/usr/bin/env python
import sys
import tweepy
import time
from random import randint

# http://talkfast.org/2010/05/31/twitter-from-the-command-line-in-python-using-oauth/
# http://api.mongodb.org/python/current/tutorial.html

CONSUMER_KEY = 'aXx2hwZulJXBLLp0lfPzEQ'
CONSUMER_SECRET = 'KfSaacldQ04RfLsUpVbCHMVFKnOU5RMW0cc8NivVR8'
ACCESS_KEY = '1367808150-XWGhtrrKe5ZyZiRk7HuCJfJRGAdOspg4W6hWme3'
ACCESS_SECRET = 'pKGZb2ZXp0GWVfhwOao4vFpKc650lwiixQVH9sW6U'

tweets = ["The #SOURCE# satellite is now targetting #TARGET# #mysspacecal @SpaceApps", "#myspacecal is reporting that #SOURCE# now observing #TARGET# @SpaceApps", "#TARGET# is now being reviewed by the #SOURCE# satellite @SpaceApps #myspacecal", "Viewing #TARGET# by #SOURCE# now happening. #myspacecal#"]
         
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

from pymongo import MongoClient
client = MongoClient()
db = client.spacecalnyc
col = db.schedules
import datetime
now = datetime.datetime.now()
print "Checking for schedules defined " + str(now)
for i in col.find({ "start": { "$lt": now}, "end": { "$gt": now}, "tweet": None}):
  print i['source'] + " at " + i['target']

i=col.find_one({ "start": { "$lt": now}, "end": { "$gt": now}, "tweet": None})
i['tweet']='Yes'
col.save(i)
tweet = tweets[randint(0,len(tweets)-1)].replace('#SOURCE#',i['source']).replace("#TARGET#",i['target'])
print tweet
api.update_status(tweet)
