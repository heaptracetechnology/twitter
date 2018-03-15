# -*- coding: utf-8 -*-
import click
from click.testing import CliRunner

from pytest import fixture

from twitter.Cli import Cli
from twitter.Twitter import Twitter


@fixture
def runner():
    return CliRunner()


@fixture
def twitter(patch, magic):
    patch.init(Twitter)
    Twitter.api = magic()
    return Twitter


def test_cli_tweet(twitter, runner):
    result = runner.invoke(Cli.tweet, ['content'])
    twitter.api.update_status.assert_called_with('content')
    assert result.exit_code == 0


def test_cli_retweet(twitter, runner):
    result = runner.invoke(Cli.retweet, ['tweet_id'])
    twitter.api.retweet.assert_called_with('tweet_id')
    assert result.exit_code == 0


def test_cli_follow(twitter, runner):
    result = runner.invoke(Cli.follow, ['handle'])
    twitter.api.create_friendship.assert_called_with('handle')
    assert result.exit_code == 0


def test_cli_followers(patch, twitter, runner):
    patch.object(click, 'echo')
    result = runner.invoke(Cli.followers, ['handle'])
    twitter.api.followers_ids.assert_called_with('handle')
    click.echo.assert_called_with(twitter.api.followers_ids())
    assert result.exit_code == 0
