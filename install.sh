#!/bin/sh
set -e

# install eventbrite from pypi
apk update
apk add --no-cache python py-pip

pip install tweepy click

rm -rf /var/cache/apk/*
