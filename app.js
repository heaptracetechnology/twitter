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
  data['screen_name'] = data['handle'] || null;
  delete data['handle'];
  client.post('friendships/create', data, function(error, tweet, response) {
    console.log(JSON.stringify(tweet));
    if(error) process.exit(1);
  });

} else if (cmd == 'unfollow') {
  // https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/post-friendships-destroy
  data['screen_name'] = data['handle'] || null;
  delete data['handle'];
  client.post('friendships/destory', data, function(error, tweet, response) {
    console.log(JSON.stringify(tweet));
    if(error) process.exit(1);
  });

} else if (cmd == 'follows') {

}
