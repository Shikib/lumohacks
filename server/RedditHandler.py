from tornado.web import RequestHandler
import reddit

class RedditHandler(RequestHandler):

  def get(self, reddit_handler):
    result = reddit.get_user_activity(reddit_handler)
    self.finish({"reddit_results": result})

  def post(self, reddit_handler):
  	reddit.send_message(reddit_handler, "Get well soon", "Here are some resources.")

  	