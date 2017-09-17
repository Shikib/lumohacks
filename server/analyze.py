import twitterapi
import reddit

from classify import predict

def analyze_user(twitter_handler, reddit_handler):
  def _remove_time(s):
    return " ".join(s.split("|")[:-1])

  sentences = []

  if twitter_handler is not None:
    try:
      sentences = sentences + twitterapi.get_user_tweets(twitter_handler)
    except:
      print("USER DNE")
  if reddit_handler is not None:
    try:
      sentences = sentences + reddit.get_user_activity(reddit_handler)
    except:
      print("USER DNE")

  y, merged_y = predict(sentences)

  return merged_y[0][1]
