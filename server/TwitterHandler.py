from tornado.web import RequestHandler
import twitterapi

class TwitterHandler(RequestHandler):

  def get(self, twitter_handler):
    results = twitterapi.get_user_tweets(twitter_handler)
    self.finish({"twitter_results": results})

  def post(self, twitter_handler):
    twitterapi.send_message(twitter_handler, "Here are some resources.")
  	
