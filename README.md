Twitter Superbowl
=================

# Purpose
How do the frequencies of people tweeting about a given subject change in real-time? 
Can we correlate these to events that happened?

## Superbowl
The superbowl is a good candidate for trying this out, as
* Well known players and team names are known ahead of time
* It has well defined time boundaries

# Results
![alt text](https://github.com/gt-big-data/twitter-superbowl/raw/master/superbowl-tweets.png "Tweets over time")
Here is a screenshot of frequencies of tweets from 3pm - 12am on Superbowl XLVIII. The game started at 6:30 PM.
Qualitative events:
* halftime by the decrease in tweets about individual teams, and increase about superbowl
* Seahawk victory shown by the spike at the end
* People talking much more about broncos than seahawks, probably frustrated by the former's performance

# Install / run
We used Redis to keep statistics, and dumped each tweet into a text file and mongodb. We used Node to connect to Redis
and rendered the data in D3.js.

## Python tracking
Code in track.py opens a streaming connection to the Twitter streaming API, then passes the 
tweet to a list of handlers (pipes) for processing.

To run this specific example, ```pip install -r requirments.txt```. You'll also need to install Redis and Mongo,
or you can add your own pipes and modify the code to use them. Pipes implement ```accept_tweet(self, tweet)```
and boolean ```autoparse``` which indicates whether to load the tweet into a Python dictionary (true) or leave it as
raw text (false)

## Node
```npm start``` starts a simple express server that makes requests to Redis for data and sends them to the client,
which renders a static D3 graph.


