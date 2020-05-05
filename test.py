import tweepy

consumer_key='OlAM80bpKx236YynXey1FT2p8'
consumer_secret='Ih16XOXeZwjpxSV4RwdyJb3Kp5FtrhqRPu7kThG4VjvplMpjDS'
access_token='2852023525-ThqdLXvbegUvx5uVpxZHc1EwjNEAefOP2EBUoVa'
access_token_secret='mXx5AA9j80FQVUm86LPfECbUvZELUzeXL8Dx3W1itm1q8'

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

