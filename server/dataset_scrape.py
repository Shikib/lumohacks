"""
Scraping script to identify posts from people with depression.
"""
import json
import praw

from collections import Counter, defaultdict

# Instantiate reddit instance
config = json.load(open("config.json"))
reddit = praw.Reddit(client_id=config["client_id"],
                     client_secret=config["client_secret"],
                     user_agent=config["client_username"],
                     username=config["client_username"],
                     password=config["client_password"])

def get_posts(num_posts, subs):
  # username -> # of posts in depressing subreddits
  users = Counter()
  for sub in subs:
    print("Scraping %s" % sub)
    user_list = [post.author for post in reddit.subreddit(sub).hot(limit=num_posts)]
    users.update([user.name for user in user_list if user is not None])

  return users

def get_user_activity(user, num_user_posts):
  print("Getting posts for: %s" % user)
  user_obj = reddit.redditor(user)
  return [
    post.title + " | " + post.selftext 
    if type(post) is praw.models.reddit.submission.Submission 
    else post.body
    for post in user_obj.hot(limit=num_user_posts)
  ]

# depressing subreddits
subs = ["depression", "suicidewatch"]

# Get 1000 posts from each subreddit
num_posts = 1000
users = get_posts(num_posts, subs)

# Get a number of posts/comments from user
user_activity = {}
num_user_posts = 100
for user in users:
  try:
    user_activity[user] = get_user_activity(user, num_user_posts)
  except:
    continue

lines = []
for user,post_text in user_activity.items():
  for text in post_text:
    line = user + "\t" + text + "\n"
    lines.append(line.encode("utf-8"))
    
open("depressed_data.csv", "w+").writelines(lines)

# non-depressing subreddits
subs = ["uplifting", "askreddit"]

# Get 1000 posts from each subreddit
num_posts = 1000
users = get_posts(num_posts, subs)

# Get a number of posts/comments from user
user_activity = {}
num_user_posts = 100
for user in users:
  try:
    user_activity[user] = get_user_activity(user, num_user_posts)
  except:
    continue

lines = []
for user,post_text in user_activity.items():
  for text in post_text:
    line = user + "\t" + text + "\n"
    lines.append(line.encode("utf-8"))
    
open("nondepressed_data.csv", "w+").writelines(lines)
