import tweepy
import os
#Hello!
consumer_key=os.environ['TWITTER_CONSUMER_KEY']
consumer_secret=os.environ['TWITTER_CONSUMER_SECRET']
access_token=os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']

auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
    tweet="Hello It's me"
    api.update_status("이거 좀 올려줘...")
except:
    print("Error during authentication")
"""
user=api.get_user("naver_news_bot")

print("User details: ")
print(user.name)
print(user.description)
print(user.location)
print("Last 20 Followers:")
for follower in user.followers():
    print(follower.name)

"""
