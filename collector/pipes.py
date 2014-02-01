import math
import pymongo
import redis
import time

class PrintPipe:
    def autoparse(self): return False;

    def accept_tweet(self, line):
        print line

class RedisPipe:
    def __init__(self, host="localhost", port=6379, db=0, ns="", period=15.):
        self.r = redis.StrictRedis(host=host, port=port, db=db)
        self.ns = ns
        self.prev = 0
        self.period = period

    def autoparse(self): return False;

    def accept_tweet(self, tweet):
        if self.prev == 0:
            self.prev = time.time()
            self.r.set(self.startKey(), self.prev)
            self.r.set(self.periodKey(), self.period)
        if time.time() - self.prev > self.period:
            self.onNextTime()
            self.prev = time.time() 
        count = self.r.incr(self.curKey())
        print "Got tweet", count

    def curKey(self):
        return self.ns + ":" + "cur"

    def startKey(self):
        return self.ns + ":" + "start"

    def endList(self):
        return self.ns + ":" + "end"

    def periodKey(self):
        return self.ns + ":period" 

    def onNextTime(self):
        curVal = self.r.getset(self.curKey(), 0)
        missed = int(math.floor((time.time() - self.prev) / self.period)) - 1
        for i in range(missed):
            self.r.rpush(self.endList(), 0)
        self.r.rpush(self.endList(), curVal)

class MongoPipe:
    def __init__(self, host="localhost", port=27017, keywords=""):
        self.m = pymongo.MongoClient(host, port)
        self.db = self.m.superbowl
        self.keywords = keywords

    def autoparse(self): return True;

    def accept_tweet(self, tweet):
        try:
            parsed = { 
                      'text' : tweet[u'text'],
                      'created_at' : tweet[u'created_at'],
                      'id' : tweet[u'id'],
                      'favorite_count' : tweet[u'favorite_count'],
                      'retweeted' : tweet[u'retweeted'],
                      'lang' : tweet[u'lang'],
                      'location' : {
                          'coordinates' : tweet[u'coordinates'],
                          'geo' : tweet[u'geo'],
                          'place' : tweet[u'place'],
                          'user_timezone' : tweet[u'user'][u'time_zone']
                       },
                      'keywords' : self.keywords
                    }
            tweet_id = self.db.tweets.insert(parsed)
            print "added tweet in mongodb!", tweet_id
        except KeyError as e:
            print "Key error", e
        except Exception as e:
            print e

