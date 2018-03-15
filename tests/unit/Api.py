# -*- coding: utf-8 -*-
import os

import tweepy

from twitter.Api import Api


def test_api_init(patch):
    patch.object(os, 'getenv')
    patch.many(tweepy, ['API', 'OAuthHandler'])
    api = Api()
    tweepy.OAuthHandler.asssert_called_with(os.getenv(), os.getenv())
    tweepy.OAuthHandler().set_access_token.asssert_called_with(os.getenv(),
                                                               os.getenv())
    tweepy.API.asssert_called_with(tweepy.OAuthHandler())
    assert api.api == tweepy.API()
