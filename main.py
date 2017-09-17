from tornado.ioloop import IOLoop
from tornado.web import Application, url
from server.MainHandler import MainHandler
from server.TwitterHandler import TwitterHandler
from server.RedditHandler import RedditHandler

def make_app():
  return Application([
    url(r"/", MainHandler),
    url(r"/reddit", RedditHandler),
    url(r"/twitter", TwitterHandler)
  ])

def main():
  app = make_app()
  app.listen(8888)
  print('Running app.')
  IOLoop.instance().start()

if __name__ == "__main__":
  main()