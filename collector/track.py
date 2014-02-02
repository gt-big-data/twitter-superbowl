from multiprocessing import Process
from pipes import RedisPipe, PrintPipe, MongoPipe
from streams import TwitterFilterStream
import sys
import time


if __name__ == '__main__':
    words = "seattle,seahawks,wilson,denver,broncos,manning,sb48,superbowl"
    pipes = []
    for word in words.split(","):
        pipes.append(RedisPipe(word, period=15, db=1, ns="track:" + word))
    pipes.append(MongoPipe())
    t = TwitterFilterStream(words, pipes=pipes)
    t.start()

