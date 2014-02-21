import json
import sys
import time
import codecs
import re

def ngrams(text, delim=" ", n=3):
    sent = re.split("\s+", text) 
    grams = [tuple(sent[i:(i + n)]) for i in range(len(sent) - (n - 1))]
    return grams


def main(f=sys.stdin):
    UTF8Writer = codecs.getwriter('utf8')
    sys.stdout = UTF8Writer(sys.stdout)
    counts = {}
    for line in f:
        j = json.loads(line)
        date = time.strptime(j['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        seconds = time.mktime(date)
        for gram in ngrams(j['text'], n=3):
            actual = " ".join(gram).lower()
            if actual not in counts:
                counts[actual] = []
            counts[actual].append(seconds)
    finals = []
    for gram in counts:
        if len(counts[gram]) > 3:
            finals.append((gram, len(counts[gram]), counts[gram]))
    finals.sort(key=lambda e: e[1])
    for pair in finals:
        print "\t".join([pair[0], str(pair[1]), json.dumps(pair[2])])

if __name__ == '__main__':
    main(sys.stdin)
