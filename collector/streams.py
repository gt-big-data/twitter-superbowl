import api_keys
from requests_oauthlib import OAuth1Session
import json

class TwitterFilterStream:
    def __init__(self, filterValues, pipes, include_geotag=None, api_keys=api_keys):
        self.twitter = OAuth1Session(api_keys.KEY, client_secret=api_keys.SECRET,
                                resource_owner_key=api_keys.TOKEN,
                                resource_owner_secret=api_keys.TOKEN_SECRET)
        self.stop = None
        if type(pipes) is not list and type(pipes) is not tuple:
            pipes = [pipes]
        self.pipes = pipes
        self.filterValues = filterValues
        self.include_geotag = include_geotag

    def start(self):
        data = {'track': self.filterValues}
        if self.include_geotag:
            data['locations'] = self.include_geotag
        resp = self.twitter.post(
            'https://stream.twitter.com/1.1/statuses/filter.json',
            data=data,
            stream=True
        )
        last = None
        autoparse = any(pipe.autoparse() for pipe in self.pipes)
        for line in resp.iter_lines():
            last = line
            parsed = None
            if autoparse:
              try:
                parsed = json.loads(line)
              except Exception as e:
                #it wasn't meant to be..
                print "Failed to parse tweet!", line 
                continue
            if line:
                for pipe in self.pipes:
                    if pipe.autoparse():
                        pipe.accept_tweet(parsed)
                    else:
                        pipe.accept_tweet(line)

            if self.stop:
                break
        print "Finished", self.filterValues, last

    def stop(self):
        self.stop = True

