import codecs
import datetime
from dateutil import tz
import json
import sys
import time

utc = tz.tzutc()
east = tz.tzlocal()
UTF8Writer = codecs.getwriter('utf-8')
sys.stdout = UTF8Writer(sys.stdout)

#print """text\ttime\tplaceName\tplaceLat\tplaceLong"""

for line in codecs.getreader('utf-8')(sys.stdin):
    if not line: continue;
    tweet = json.loads(line)
    if not u'place' in tweet or not tweet[u'place']\
            or u'bounding_box' not in tweet[u'place'] or not tweet[u'place'][u'bounding_box']\
            or u'full_name' not in tweet[u'place'] or not tweet[u'place'][u'full_name']\
            or u'coordinates' not in tweet[u'place'][u'bounding_box']\
            or not tweet[u'place'][u'bounding_box'][u'coordinates']\
            or not u'text' in tweet or not tweet[u'text']\
            or u'created_at' not in tweet or not tweet[u'created_at']:
                continue
    text, created, placeName, points = tweet[u'text'], tweet[u'created_at'],\
            tweet[u'place'][u'full_name'], tweet[u'place'][u'bounding_box'][u'coordinates'][0]
    text = text.replace("\n", " ")
    date = datetime.datetime.strptime(created,'%a %b %d %H:%M:%S +0000 %Y')
    date = date.replace(tzinfo=utc)
    eastDate = date.astimezone(east)
    eastDateStr = datetime.datetime.strftime(eastDate, "%Y-%m-%d %H:%M:%S")

    #twitter points are in long, lat format
    #https://dev.twitter.com/docs/platform-objects/places#obj-boundingbox
    finalLat = 0.0
    finalLong = 0.0
    count = 0
    for longit, latit in points:
        finalLat += latit
        finalLong += longit
        count += 1
    finalLat /= count
    finalLong /= count
    print u"%s\t%s\t%s\t%s\t%s" % (text, eastDateStr, placeName, str(finalLat), str(finalLong))

