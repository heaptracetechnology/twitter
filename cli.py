#!/usr/bin/env python
import os
import sys
import tweepy
import click


class Twitter:

    def __init__(self):
        consumer_secret = os.getenv('CONSUMER_SECRET')
        consumer_key = os.getenv('CONSUMER_KEY')
        access_token = os.getenv('ACCESS_TOKEN')
        access_token_secret = os.getenv('ACESS_TOKEN_SECRET')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)


class Cli:

    @click.group()
    def main():
        """
        Twitter container for Asyncy. Requires OAuth credential to be set in
        environment: CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
        """
        pass

    @main.command()
    @click.argument('content')
    def tweet(content):
        twitter = Twitter()
        twitter.api.update_status(content)

    @main.command()
    @click.argument('who')
    def follow(who):
        twitter = Twitter()
        twitter.api.create_friendship(who)


if __name__ == '__main__':
    Cli.main()
