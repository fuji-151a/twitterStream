# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import sys
import os.path
import codecs
import simplejson
import ConfigParser
import re

argv = sys.argv
pFile = argv[1]
fileName = argv[2]
def readProperties(pFile):
    properties = {}
    f = open(pFile, 'r')
    for line in f:
        data = line.split("=")
        properties[data[0]]=data[1].replace('\n', '') 
    f.close
    return properties

class StdOutListener(StreamListener):
    def on_data(self, data):
        global fileName, start, start_create_at
        size = os.path.getsize(fileName)
        lang = ""
        create_at = ""
        if data.startswith("{"):
            try:
                f = codecs.open(fileName,"a","utf-8")
                tweet = simplejson.loads(data + "\n","utf-8")
                lang = self.checkKeys("lang", tweet)
                if lang == "ja":
                    if start == 0:
                        simplejson.dump(tweet,f,indent=4,ensure_ascii=False)
                        start_create_at = self.checkKeys("created_at", tweet)
                        start = 1
                    else:
                        f.write(',')
                        create_at = self.checkKeys("created_at", tweet)
                        simplejson.dump(tweet,f,indent=4,ensure_ascii=False)
                        if size > 1200000:
                            print "System End"
                            print size
                            sys.exit()
            except IOError,e:
                print e.message
            finally:
                f.close()
        return True

    def on_error(self, status):
        print "on_error"
        print status

    def checkKeys(self, key, tweet):
        if tweet.has_key(key):
            return tweet[key]
        else:
            return ""

if __name__ == '__main__':
    start = 0
    properties = readProperties(pFile)
    sol = StdOutListener()
    auth = OAuthHandler(
            properties["oauth.consumerKey"], 
            properties["oauth.consumerSecret"]
        )
    auth.set_access_token(
            properties["oauth.accessToken"], 
            properties["oauth.accessTokenSecret"]
        )
    stream = tweepy.Stream(auth, sol)
    stream.sample()
