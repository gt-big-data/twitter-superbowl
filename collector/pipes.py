import math
import pymongo
import redis
import time
import re, string 

class PrintPipe:
    def autoparse(self): return False;

    def accept_tweet(self, line):
        print line

class RedisPipe:
    def __init__(self, word, host="localhost", port=6379, db=0, ns="", period=15.):
        self.r = redis.StrictRedis(host=host, port=port, db=db)
        self.ns = ns
        self.word = word
        self.pattern = re.compile(".*" + word + ".*", flags=re.I) 
        self.prev = 0
        self.period = period

    def autoparse(self): return True;

    def accept_tweet(self, tweet):
        if self.prev == 0:
            self.prev = time.time()
            self.r.setnx(self.startKey(), time.time());
            self.r.set(self.periodKey(), self.period)
        timeElapsed = time.time() - self.prev 
        if u'text' in tweet and self.pattern.match(tweet[u'text']):
            count = self.r.incr(self.curKey())
        if timeElapsed > self.period:
            self.onNextTime()
            self.prev = time.time() 

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
    def __init__(self, host="localhost", port=27017):
        self.m = pymongo.MongoClient(host, port)
        self.db = self.m.superbowl
        self.writeBuf = [] 

    def autoparse(self): return True;

    def accept_tweet(self, tweet):
        if u'text' not in tweet and 'text' not in tweet:
            return
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
                      'hashtags' : tweet[u'entities'][u'hashtags'],
                      'urls' : tweet[u'entities'][u'urls']
                    }
            self.writeBuf.append(parsed)
            if len(self.writeBuf) > 1000:
                tweet_id = self.db.tweets.insert(self.writeBuf)
                del self.writeBuf[0:len(self.writeBuf)]
        except KeyError as e:
            print "Key error", e
            print tweet
            pass
        except Exception as e:
            print self.keywords, "Skip", e
            pass

class FilePipe:
    def __init__(self, filename="tweets.json"):
        self.filename = filename
        self.f = open(filename, 'a')

    def autoparse(self): return False;

    def accept_tweet(self, tweet):
        print >>self.f, tweet
