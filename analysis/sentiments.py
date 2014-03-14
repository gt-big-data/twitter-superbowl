from mrjob.job import MRJob
import json
import re


class MRWordFrequencyCount(MRJob):

    def mapper_init(self):
        self.weights = {}
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
            ls = tweet["text"].lower().split()
            count = 0
            for word in ls:
                if word in self.weights:
                    count += self.weights[word]
            for word in ls:
                if word not in self.weights:
                    yield word, count

    def reducer(self, key, values):
        values = list(values)
        yield key, sum(values) / len(values)


if __name__ == '__main__':
    MRWordFrequencyCount.run()