from twitter import *
import json

"""
Uses the twitter API to get the recent tweets of a user, 
and can send dm's to a user, and mention a user in a status.
"""
config = json.load(open("server/config.json"))
tt = Twitter(auth=OAuth(
  config['token'], 
  config['token_secret'], 
  config['consumer_key'], 
  config['consumer_secret']))
include_retweets = config['include_retweets']
  
def get_user_tweets(handler, num_tweets=200):
  """
  Get user's num_tweets most recent tweets.
  """
  tweets = tt.statuses.user_timeline(screen_name=handler, count=num_tweets)
  filtered_tweets = []
  for tweet in tweets:
    if (include_retweets == False):
      if ("retweeted_status" not in tweet):
    	    filtered_tweets.append(tweet['text'])
    else:
    	filtered_tweets.append(tweet['text'])
  print("Number of tweets: " + str(len(filtered_tweets)))
  return filtered_tweets

def send_dm(handler, text):
  """
  Send direct message to a user (but must be followed by them, first).
  """
  result = tt.direct_messages.new(user=handler, text=text)
  print result

def send_message(handler, text):
  """
  Mention a user in a status and write them a message.
  """
  status_msg = "Hello @" + handler + ". " + text
  result = tt.statuses.update(status=status_msg)