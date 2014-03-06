import calendar
from collections import Counter
from datetime import datetime
import json
from guppy import hpy
import string
import re
import sys

import math

import numpy as np

def countPeriods(tweetFile, periodLength=60):
    start = '2014-02-02 23:30:00'
    startdate = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    secsStart = calendar.timegm(startdate.utctimetuple())
    
    periods = {}
    punct = re.compile("[%s]" % re.escape(string.punctuation))

    dateFormat = "%a %b %d %H:%M:%S +0000 %Y"
    i = 0
    for line in tweetFile:
        i += 1
        if i % 10000 == 0: print "Did line ", i;
        tweet = json.loads(line)
        raw = tweet['text']
        if not raw: 
            continue;
        if not tweet['created_at']: 
            continue;
        words = punct.sub("", raw).lower().split(" ")
        date = datetime.strptime(tweet['created_at'], dateFormat)
        secs = calendar.timegm(date.utctimetuple())
        period = int((secs - secsStart) / periodLength)
        for i in range(1, len(words) - 1):
            threeGram = (words[i-1], words[i], words[i+1])
            if not all(threeGram): continue; # get rid of empty words
            if period not in periods:
                periods[period] = Counter()
            periods[period][threeGram] += 1
    return periods

def extractStats(periods):
    stats = {}
    for period in periods:
        for threeGram in periods[period]:
            periodCount = periods[period][threeGram] 
            if threeGram not in stats:
                stats[threeGram] = []
            stats[threeGram].append(periodCount) 
    
    totalPeriod = float(max(periods.keys()) - min(periods.keys()))
    for threeGram in stats:
        avg = np.sum(stats[threeGram]) / totalPeriod
        var = np.sum( (np.array(stats[threeGram]) - avg)**2 ) / totalPeriod
        std = math.sqrt(var) 
        stats[threeGram] = (avg, std)
    return stats


def main(tweetFile=sys.stdin, outFile=sys.stdout):
    periods = countPeriods(tweetFile) 
    stats = extractStats(periods)


    topResults = {}
    # normalize the counts per period
    byZ = lambda x: -x[1]
    for period, counter in periods.items():
        for threeGram in counter:
            count = counter[threeGram]
            avg, stdDev = stats[threeGram]
            if stdDev > 0:
                counter[threeGram] = ( (count - avg) / stdDev, avg, count ) 
            else:
                counter[threeGram] = (0., 0.)

        significant = [(threeGram, z[0], z[1]) for threeGram, z in counter.items() if z[0] *  z[1] > 20]
        if significant:
            significant.sort(key=byZ)
            topResults[period] = significant
            s = json.dumps({
                    "per" : period, "top" : significant
                })
            print >>outFile, s
        print "Finished updating top 3grams for", period

if __name__ == '__main__':
    if len(sys.argv)  < 2: main();
    elif len(sys.argv) < 3:
        with open(sys.argv[1]) as f:
            main(f)
    else:
        with open(sys.argv[1]) as tweetFile:
            with open(sys.argv[2], 'w') as outFile:
                main(tweetFile, outFile)
