# -*- coding: utf-8 -*-

from flask import Flask, make_response, request
from twitter import *
from twitter.stream import TwitterStream, Timeout, HeartbeatTimeout, Hangup
import os
from json import dumps
from threading import Thread

from stream import Stream

app = Flask(__name__)

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']

auth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

t = Twitter(auth=auth)


def body():
    data = request.json
    if data.get('handler'):
        data['screen_name'] = data.pop('handler')
    if data.get('user'):
        data['user_id'] = data.pop('user')
    return data


def response(res):
    # TODO res.rate_limit_remaining
    # TODO res.rate_limit_limit
    # TODO res.rate_limit_reset
    return dict(res)


@app.route('/tweet', methods=['POST'])
def tweet():
    return dumps(response(t.statuses.update(**body())))


@app.route('/retweet', methods=['POST'])
def retweet():
    pass


@app.route('/follow', methods=['POST'])
def follow():
    pass


@app.route('/unfollow', methods=['POST'])
def unfollow():
    pass


subscriptions = {}


@app.route('/stream/subscribe', methods=['POST'])
def stream_subscribe():
    data = body()
    subscriptions.setdefault(data['id'], Stream(auth, data).start())
    return 'Subscribed'


@app.route('/stream/unsubscribe', methods=['POST'])
def stream_unsubscribe():
    s = subscriptions.pop(body()['id'], None)
    if s:
        s.stop()
    return 'Unsubscribed'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
