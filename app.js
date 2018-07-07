#!/usr/bin/env node

var Twitter = require('twitter');

var client = new Twitter({
  consumer_key: process.env.CONSUMER_KEY,
  consumer_secret: process.env.CONSUMER_SECRET,
  access_token_key: process.env.ACCESS_TOKEN,
  access_token_secret: process.env.ACCESS_TOKEN_SECRET
});

var cmd = process.argv[2];

var data = JSON.parse(process.argv[3]);
if (data['handle']) {
  data['screen_name'] = data['handle'];
  delete data['handle'];
}
if (data['user']) {
  data['user_id'] = data['user'];
  delete data['user'];
}

if (cmd == 'tweet') {
  client.post('statuses/update', data, function(error, tweet, response) {
    console.log(JSON.stringify(tweet));
    if(error) process.exit(1);
  });

} else if (cmd == 'retweet') {
  client.post('statuses/retweet/' + data.tweet, function(error, tweet, response) {
    console.log(JSON.stringify(tweet));
    if(error) process.exit(1);
  });

} else if (cmd == 'follow') {
  // https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/post-friendships-create.html
  client.post('friendships/create', data, function(error, tweet, response) {
    console.log(JSON.stringify(tweet));
    if(error) process.exit(1);
  });

} else if (cmd == 'unfollow') {
  // https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/post-friendships-destroy
  client.post('friendships/destory', data, function(error, tweet, response) {
    console.log(JSON.stringify(tweet));
    if(error) process.exit(1);
  });

} else if (cmd == 'followers') {
  // https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-followers-list
  client.post('followers/list', data, function(error, tweet, response) {
    console.log(JSON.stringify(tweet));
    if(error) process.exit(1);
  });

} else if (cmd == 'stream') {
  var request = require('request');
  var _ = require('lodash');

  const isTweet = _.conforms({
    contributors: _.isObject,
    id_str: _.isString,
    text: _.isString,
  })

  // https://www.npmjs.com/package/twitter#streaming-api
  var stream = client.stream('statuses/filter', {track: data.hashtag});
  stream.on('data', function(event) {
    if (data.tweets_only && !isTweet(event)) {
      return null;
    }
    request.post({
      url: process.env.OMG_URL,
      body: JSON.stringify(event),
    }, function (error, response, body) {
        if (error) {
          console.log('error:', error);
          console.log('statusCode:', response && response.statusCode);
        } else {
          // send metric of tweet found
        }
      }
    );
  });

  stream.on('error', function(error) {
    throw error;
  });

}
