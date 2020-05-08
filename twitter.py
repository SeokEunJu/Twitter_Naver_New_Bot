import tweepy

consumer_key='Your_consumer_key'
consumer_secret='Your_consumer_secret'
access_token='Your_access_token'
access_token_secret='Your_access_token_secret'

auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)

tweet="Hello It's me"
api.update_status(status=tweet)
"""
user=api.get_user("solya_xd")

print("User details: ")
print(user.name)
print(user.description)
print(user.location)
print("Last 20 Followers:")
for follower in user.followers():
    print(follower.name)
"""

