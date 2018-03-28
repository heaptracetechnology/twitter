# -*- coding: utf-8 -*-
import click

from .Twitter import Twitter


class Cli:
    
    @staticmethod
    def _strip_who(who):
        who = who.replace('https://twitter.com/', '')
        who = who.replace('http://twitter.com/', '')
        who = who.replace('@', '')
        return who

    @click.group()
    def main():
        """
        Twitter container for Asyncy. Requires OAuth credential to be set in
        environment: CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
        """
        pass

    @staticmethod
    @main.command()
    @click.argument('content')
    def tweet(content):
        twitter = Twitter()
        twitter.api.update_status(content)

    @staticmethod
    @main.command()
    @click.argument('tweet_id')
    def retweet(tweet_id):
        twitter = Twitter()
        twitter.api.retweet(tweet_id)

    @staticmethod
    @main.command()
    @click.argument('who')
    def follow(who):
        who = Cli._strip_who(who)
        twitter = Twitter()
        twitter.api.create_friendship(who)

    @staticmethod
    @main.command()
    @click.argument('who')
    def followers(who):
        who = Cli._strip_who(who)
        twitter = Twitter()
        followers = twitter.api.followers_ids(who)
        click.echo(followers)
