"""
Reddit package.
""" 
import json
import praw

# Instantiate reddit instance
config = json.load(open("server/config.json"))
reddit = praw.Reddit(client_id=config["client_id"],
                     client_secret=config["client_secret"],
                     user_agent=config["client_username"],
                     username=config["client_username"],
                     password=config["client_password"])

def get_users(subs, num_posts=1000):
  """
  Get users (based on num posts hot posts) for subs.
  """
  users = Counter()
  for sub in subs:
    print("Scraping %s" % sub)
    user_list = [post.author for post in reddit.subreddit(sub).hot(limit=num_posts)]
    users.update([user.name for user in user_list if user is not None])

  return users

def get_user_activity(user, num_user_posts=200):
  """
  Get list of posts for user.
  """
  print("Getting posts for: %s" % user)
  user_obj = reddit.redditor(user)
  return [
    post.title + " | " + post.selftext 
    if type(post) is praw.models.reddit.submission.Submission 
    else post.body
    for post in user_obj.hot(limit=num_user_posts)
  ]

def send_message(user, subject, text):
  """
  Send a message to the user, with a subject/text.
  """
  redditor = reddit.redditor(user)
  redditor.message(subject, text)
