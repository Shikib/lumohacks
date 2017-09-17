from twitter import *
import json

"""
A class that uses the twitter API to get the recent tweets of a user, 
and can send dm's to a user, and mention a user in a status.

Example:
	scraper = TwitterScrape()
	scraper.scrape_recent("yeah568")
	scraper.send_message("kaabistar")
"""
class TwitterScrape:
  def __init__(self):
  	with open('config.json') as configfile:
  	  configs = json.load(configfile)
	  self.consumer_key = configs['consumer_key']
	  self.token = configs['token']
	  self.token_secret = configs['token_secret']
	  self.consumer_secret = configs['consumer_secret']
	  self.include_retweets = configs['include_retweets']
  	self.twitter = Twitter(auth=OAuth(self.token, self.token_secret, self.consumer_key, self.consumer_secret))
  
  def scrape_recent(self, handler):
    tweets = self.twitter.statuses.user_timeline(screen_name=handler, count=200)
    filtered_tweets = []
    for tweet in tweets:
      	if (self.include_retweets == False):
          if "retweeted_status" not in tweet:
      	    filtered_tweets.append(tweet['text'])
      	else:
      		filtered_tweets.append(tweet['text'])
    print("Number of tweets: " + str(len(filtered_tweets)))
    return filtered_tweets

  def send_dm(self, handler):
  	result = self.twitter.direct_messages.new(user=handler, text="I think yer swell!")
  	print result

  def send_message(self, handler):
  	status_msg = "Hello @" + handler + " you are a star!"
  	result = self.twitter.statuses.update(status=status_msg)