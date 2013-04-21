#!/usr/bin/env python
import sys
import tweepy

# http://talkfast.org/2010/05/31/twitter-from-the-command-line-in-python-using-oauth/
# http://api.mongodb.org/python/current/tutorial.html

CONSUMER_KEY = 'aXx2hwZulJXBLLp0lfPzEQ'
CONSUMER_SECRET = 'KfSaacldQ04RfLsUpVbCHMVFKnOU5RMW0cc8NivVR8'
ACCESS_KEY = '1367808150-XWGhtrrKe5ZyZiRk7HuCJfJRGAdOspg4W6hWme3'
ACCESS_SECRET = 'pKGZb2ZXp0GWVfhwOao4vFpKc650lwiixQVH9sW6U'

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
for i in col.find({ "start": { "$lt": now}, "end": { "$gt": now}, "tweet": { "$in" :[""]}}):
  tweet = 'The ' + i['source'] + ' satellite is now targetting ' + i['target'] + ' http://http://spacecalnyc.com/ #myspacecal @SpaceApps'
  print tweet
  api.update_status(tweet)
  i['tweet']='Yes'
  col.save(i)
  #print col.find_one({id: i['_id']})
