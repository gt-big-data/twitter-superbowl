from multiprocessing import Process
from pipes import RedisPipe, PrintPipe, MongoPipe
from streams import TwitterFilterStream
import sys

def streamToRedis(words=['twitter']):
    api_call = " ".join(words)
    print "Tracking words", words
    r = RedisPipe(period=15, db=1, ns="track:" + "&".join(words))
    t = TwitterFilterStream(api_call, pipes=[r, MongoPipe(keywords=api_call)])
    t.start()

if __name__ == '__main__':
    track = [
                ["seahawks"],
                ["broncos"]
            ]

    procs = [Process(target=streamToRedis, args=(words,)) for words in track]
    for p in procs:
        p.start()

    for p in procs:
        p.join()
