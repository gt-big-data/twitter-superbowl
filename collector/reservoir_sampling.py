import json
import random
# import pymongo

# m = pymongo.MongoClient(host="localhost", port=27017)
# db = m.superbowl

result = []

# tweetCursor = db.tweets.find()
# for tweet in tweetCursor:
#     tweets.append(tweet)

with open('tweets.json') as t:
    count = 0
    for line in t:
        tweet = json.loads(line)
        simpler_tweet = {}
        if "created_at" in tweet.keys():
            simpler_tweet["created_at"] = tweet["created_at"]
        if "text" in tweet.keys():
            simpler_tweet["text"] = tweet["text"]
        if count < 1000:
            result.append(simpler_tweet)
            count += 1
        else:
            j = random.randint(1, count)
            if j < 1000:
                result[j] = simpler_tweet
            count += 1

with open("sample_tweets.txt", "w") as f:
    for i in result:
        json.dump(i, f, indent=4)

