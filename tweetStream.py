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
        global fileName,size
        if data.startswith("{"):
            try:
                f = codecs.open(fileName,"a","utf-8")
                tweet = simplejson.loads(data + "\n","utf-8")
                if tweet["lang"] == "ja" and (tweet.has_key("lang")):
                    if size == 2:
                        simplejson.dump(tweet,f,indent=4,ensure_ascii=False)
                        size = 0
                    else:
                        f.write(',')
                        simplejson.dump(tweet,f,indent=4,ensure_ascii=False)
            except Exception,e:
                print e.message
            finally:
                f.close()
        return True

    def on_error(self, status):
        print "on_error"
        print status

if __name__ == '__main__':
    size = os.path.getsize(fileName)
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
