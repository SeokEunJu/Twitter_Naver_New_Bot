import naverAPIClient
import os
import time
import tweepy
from twitter_set_api import create_api
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    naverAPI = naverAPIClient.NaverAPIClient()
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id = since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        #find tweet that include "뉴스" keyword
        if any(keyword in tweet.text.lower() for keyword in keywords):
            #if a bot didn't follow a user, follow the user
            if not tweet.user.following:
                tweet.user.follow()
            #remember original tweet's id to reply to that
            reply_id = tweet.id
            mention_tweet = tweet.text.replace('@',' ').split()
            for i in range(len(mention_tweet)):
                if(mention_tweet[i] == "뉴스"):
                    #search_keyword is set to the argument following "뉴스"
                    search_keyword = mention_tweet[i+1]
                    break
            logger.info(search_keyword)
            returned_result = naverAPI.search(search_keyword)
            user_id = tweet.user.screen_name
            #Set the mention string
            status = f"@{user_id} {returned_result}"
            #tweet!
            try:
                api.update_status(status,
                in_reply_to_status_id = reply_id)
            except tweepy.error.TweepError:
                print("duplicated")
                api.update_status("중복된 트윗입니다. 다른 키워드를 넣어주세요.",
                in_reply_to_status_id = reply_id)
            continue

    return new_since_id

def main():
    api = create_api()
    SINCE_ID = open("SINCE_ID", "r")
    since_id = int(SINCE_ID.read())
    SINCE_ID.close()
    while True:
        since_id = check_mentions(api, ["뉴스"], since_id)
        #clear since_id file
        clear_file = open("SINCE_ID", "w")
        clear_file.close()
        #update since_id file
        write_file = open("SINCE_ID", "w")
        write_file.write(str(since_id))
        write_file.close()
        logger.info("Waiting...")
        time.sleep(3)

if __name__ == "__main__":
    main()
