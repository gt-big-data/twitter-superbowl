from mrjob.job import MRJob
import json
import re
from datetime import datetime
import calendar


class MRSentiment(MRJob):

    def mapper_init(self):
        self.weights = {}
        start = '2014-02-02 18:30:00'
        startdate = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        self.millistart = calendar.timegm(startdate.utctimetuple())
        with open("sentiments.txt", "r") as f:
            for line in f:
                ls = re.split('\s+', line.strip().lower())
                if len(ls) == 2:
                    word = ls[0]
                    word = re.sub('\W', '', word)
                    self.weights[word] = float(ls[1])

    def mapper(self, _, tweet):
        tweet = json.loads(tweet)
        if tweet["text"]:
            timedate = tweet["created_at"].split()
            time = "2014-02-02 " + timedate[3]
            date = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            milli = calendar.timegm(date.utctimetuple());
            minute = int((milli - self.millistart) / 60)
            ls = tweet["text"].lower().split()
            ls = [word for word in ls if not word.startswith('@')]
            ls = [word for word in ls if not word.startswith('\\')]
            count = 0
            for word in ls:
                if word in self.weights:
                    count += self.weights[word]
            yield minute, count

    def reducer(self, key, values):
        tot, n = 0.0, 0.0
        for sent in values:
            n += 1
            tot += sent
        yield (key, tot / n)

if __name__ == '__main__':
    MRSentiment.run()