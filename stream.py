from twitter.stream import TwitterStream, Timeout, HeartbeatTimeout, Hangup
from json import dumps
import requests
import threading


class Stream(threading.Thread):
    def __init__(self, auth, subscription):
        threading.Thread.__init__(self)
        stream = TwitterStream(auth=auth, block=True)
        self.stopped = False
        self.endpoint = subscription['endpoint']

        if subscription['data'].get('filter'):
            self.iterator = stream.statuses.filter(
                track=subscription['data']['filter'])
        else:
            self.iterator = stream.statuses.sample()

    def stop(self):
        self.stopped = True

    def run(self):
        for tweet in self.iterator:
            if self.stopped:
                raise StopIteration
            elif tweet is None:
                print('Stream: No output')
            elif tweet is Timeout:
                print('Stream: Timeout')
            elif tweet is HeartbeatTimeout:
                print('Stream: Heartbeat Timeout')
            elif tweet is Hangup:
                print('Stream: Hangup')
            elif tweet.get('text'):
                requests.post(
                    self.endpoint,
                    headers={'Content-Type': 'application/json'},
                    data=dumps({
                        'eventType': 'tweet',
                        'cloudEventsVersion': '0.1',
                        'contentType': 'application/vnd.omg.object+json',
                        'eventID': tweet['id'],
                        'data': tweet
                    })
                )
            else:
                print(f'Stream: Other {str(tweet)}')
