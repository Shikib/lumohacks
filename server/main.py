from tornado.ioloop import IOLoop
from tornado.web import Application, url
from MainHandler import MainHandler
from AnalyzeHandler import AnalyzeHandler

def make_app():
  return Application([
    url(r"/", MainHandler),
    url(r"/analyze", AnalyzeHandler)
  ])

def main():
  app = make_app()
  app.listen(8888)
  print('Running app.')
  IOLoop.instance().start()

if __name__ == "__main__":
  main()
