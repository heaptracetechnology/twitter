# -*- coding: utf-8 -*-
import os

import tweepy


class Twitter:

    def __init__(self):
        consumer_secret = os.getenv('CONSUMER_SECRET')
        consumer_key = os.getenv('CONSUMER_KEY')
        access_token = os.getenv('ACCESS_TOKEN')
        access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
