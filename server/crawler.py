from analyze import analyze_user
from dataset_scrape import get_posts
from reddit import send_message

users = [e[0] for e in get_posts(100, ["depression", "suicidewatch"])]

friendly_message = """
Hey there! Just wanted to reach out to you and let you know that you're awesome.

Just wanted to let you knkow that if you ever need somebody talk to feel free to talk to, send me a message and I'd be happy to chat!

If you're ever feeling suicidal please take a look at /r/SWResources.

You're an amazing person and I hope you have a great day.
"""

for user in users:
  if analyze_user(None, user) > 0.5:
    send_message(user, "Just checking in!", friendly_message)
