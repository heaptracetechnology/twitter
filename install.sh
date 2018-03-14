#!/bin/sh
set -e

# install eventbrite from pypi
apk update
apk add --no-cache python py-pip

pip install tweepy

rm -rf /var/cache/apk/*
