import tweepy
import logging
from config import create_api
import time
import naver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if any(keyword in tweet.text.lower() for keyword in keywords):
            if not tweet.user.following:
                tweet.user.follow()
            reply_id=tweet.id
            mention_tweet=tweet.text.split()
            logger.info(mention_tweet[2])
            returned_result=' '.join(naver.search(mention_tweet[2]))
            user_id=tweet.user.screen_name
            status="@"+user_id+" "+returned_result
            api.update_status(status,
                in_reply_to_status_id=reply_id)
            continue
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, ["뉴스","블로그","이미지"], since_id)
        logger.info("Waiting...")
        time.sleep(3)

if __name__ == "__main__":
    main()
