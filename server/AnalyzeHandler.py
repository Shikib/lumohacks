from tornado.web import RequestHandler
import analyze
import reddit
import twitterapi

class AnalyzeHandler(RequestHandler):

  def get(self, twitter_handler, reddit_handler):
    results = analyze.analyze_user(twitter_handler, reddit_handler)
    self.finish({"results": results})

  def post(self, twitter_handler, reddit_handler):
  	if twitter_handler is not None:
  	  twitterapi.send_message(twitter_handler, "Here are some resources.")
  	if reddit_handler is not None:
  	  reddit.send_message(reddit_handler, "Get well soon", "Here are some resources.")

  	
