import twitterapi
import reddit

from classify import predict

def analyze_user(twitter_handler, reddit_handler):
  def _remove_time(s):
    return " ".join(s.split("|")[:-1])

  tweets = twitterapi.get_user_tweets(twitter_handler)
  posts = reddit.get_user_activity(reddit_handler)

  sentences = [_remove_time(s) for s in tweets+posts] 

  y, merged_y = predict(sentences)

  return merged_y[0][1]
