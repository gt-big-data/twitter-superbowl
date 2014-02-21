from datetime import datetime
import csv
import calendar

interval = 60
start = '2014-02-02 18:30:00'
startdate = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
millistart = calendar.timegm(startdate.utctimetuple())
buckets = {}

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
                buckets[keyvalue] += row
            else:
                buckets[keyvalue] = [row]

for interval, tweets in buckets.items():
    length = len(tweets)
    thelength = str(length)
    theinterval = str(interval)
    print(theinterval + " " + thelength)
    
