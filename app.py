# -*- coding: utf-8 -*-

from flask import Flask, make_response, request
import tweepy
import os
from http import HTTPStatus
from json import dumps
from threading import Thread

from twitter import *
from twitter.stream import TwitterStream, Timeout, HeartbeatTimeout, Hangup

from stream import Stream

app = Flask(__name__)

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']

def getOauth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


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
    t = getOauth()
    data = request.json
    if data.get('status') is None or data.get('status') == "":
        res = {
            'status': 'failed',
            'reason': 'Status must be specified.',
        }
        response_code = 400
        return dumps(res), response_code
    return dumps(t.update_status(data.pop("status"))._json)


@app.route('/retweet', methods=['POST'])
def retweet():
    t = getOauth()
    data = request.json
    if data.get('id') is None or data.get('id') == "":
        res = {
            'status': 'failed',
            'reason': 'Id must be specified.'
        }
        response_code = 400
        return dumps(res), response_code
    response = t.retweet(data.pop("id"))
    return dumps(response._json)


@app.route('/follow', methods=['POST'])
def follow():
    t = getOauth()
    data = request.json
    if data.get('id') is not None:
        return dumps(t.create_friendship(data.pop("id"),follow=True)._json)
    elif data.get('screen_name') is not None:
        return dumps(t.create_friendship(data.pop("screen_name"),follow=True)._json)
    else:
        res = {
            'status': 'failed',
            'reason': "At least one of 'id' or 'screen_name' must be specified."
        }
        response_code = 400
        return dumps(res), response_code


@app.route('/unfollow', methods=['POST'])
def unfollow():
    t = getOauth()
    data = request.json
    if data.get('id') is not None:
        return dumps(t.destroy_friendship(data.pop("id"))._json)
    elif data.get('screen_name') is not None:
        return dumps(t.destroy_friendship(data.pop("screen_name"))._json)
    else:
        res = {
            'status': 'failed',
            'reason': "At least one of 'id' or 'screen_name' must be specified."
        }
        response_code = 400
        return dumps(res), response_code


subscriptions = {}


@app.route('/stream/subscribe', methods=['POST'])
def stream_subscribe():
    auth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    data = body()
    if data["data"].get("track") is None or data["data"].get("track") == "":
        res = {
            'status': 'failed',
            'reason': "Track must be specified."
        }
        response_code = 400
        return dumps(res), response_code
    subscriptions.setdefault(data['id'], Stream(auth, data).start())
    return 'Subscribed'


@app.route('/stream/unsubscribe', methods=['POST'])
def stream_unsubscribe():
    if body()['id'] is None or body()['id'] == "":
        res = {
            'status': 'failed',
            'reason': "Id must be specified."
        }
        response_code = 400
        return dumps(res), response_code
    s = subscriptions.pop(body()['id'], None)
    if s:
        s.stop()
    return 'Unsubscribed'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
