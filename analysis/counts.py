from datetime import datetime
import csv
import calendar
import string

interval = 60
start = '2014-02-02 18:30:00'
startdate = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
millistart = calendar.timegm(startdate.utctimetuple())
buckets = {}
wordcount = {}
unicodeerrors = 0

with open('geo-text-time.tsv', 'rt') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    i = 0
    for row in tsvin:
        if len(row) > 1:
            timedate = row[1]
            date = datetime.strptime(timedate, "%Y-%m-%d %H:%M:%S")
            milli = calendar.timegm(date.utctimetuple())
            keyvalue = int((milli - millistart) / 60)
            if keyvalue in buckets:
                buckets[keyvalue]["tweets"] += row
            else:
                buckets[keyvalue] = {"tweets" : [row], "counts" : {}}
            
            tweet = row[0]
            listofblocks = tweet.split();
            for block in listofblocks:
                word = str(block).lower()
                for char in block:
                    if char in string.punctuation:
                        word = word.replace(char, "")
                if word in wordcount:
                    wordcount[word] += 1
                else:
                    wordcount[word] = 1
                if word in buckets[keyvalue]["counts"]:
                    buckets[keyvalue]["counts"][word] += 1   
                else:
                    buckets[keyvalue]["counts"][word] = 1

averages = {}

for word in wordcount:
    value = wordcount[word] / float(len(buckets.values()))
    averages[word] = value
    
over = {}

for interval, tweets in buckets.items():
    for word in wordcount:
        if word in buckets[interval]["counts"]:
            num = buckets[interval]["counts"][word]
            if num > (2 * averages[word]):
                if word in over:
                    over[word] += (interval,)
                if word not in over:
                    over[word] = (interval,)

exactover = {}

for keyword, tup in over.items():
    for interval in tup:
        if interval < 0:
            interval = 240 - interval # ??????
        """
        if interval == 0:
            exactover[keyword] = start
        elif interval <= 60:
            time = # add interval minutes to start
            exactover[keyword] = time
        elif interval <= 120:
            time = # add 1 hour and interval - 60 minutes
            exactover[keyword] = time
        elif interval <= 180:
            time = # add 2 hours and interval - 120 minutes
            exactover[keyword] = time
        else:
            time = # add 3 hours and interval - 180 minutes
            exactover[keyword] = time
        """

seahawkstot = wordcount["seahawks"]
manningtot = wordcount["manning"]
seahawksavg = averages["seahawks"]
manningavg = averages["manning"]

print("\nSeahawks was tweeted {} times".format(seahawkstot))
print("\nManning was tweeted {} times".format(manningtot))
print("\nSeahawks was tweeted {:2f} times per minutes".format(seahawksavg))
print("\nManning was tweeted {:2f} times per minutes\n".fromat(manningavg))
print(over["seahawks"])







