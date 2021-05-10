#!/usr/bin/env python3

import tweepy
import logging
from config import create_api
import requests
import time
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue

        if any("la jolla" in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()
                
            url = "https://goweather.herokuapp.com/weather/lajolla"
            response = requests.get(url)
            temperature = int(re.sub("[^0-9]", "", response.json()["temperature"]))
            temp_f = str(temperature*9/5 + 32)

            api.update_status(
                status = "@" + tweet.user.screen_name + " It's currently " + temp_f + " degrees Fahrenheit outside in La Jolla",
                in_reply_to_status_id = tweet.id,
            )
        elif any("virginia beach" in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")
                
            url = "https://goweather.herokuapp.com/weather/norfolk"
            response = requests.get(url)
            temperature = int(re.sub("[^0-9]", "", response.json()["temperature"]))
            temp_f = str(temperature*9/5 + 32)

            api.update_status(
                status = "@" + tweet.user.screen_name + " It's currently " + temp_f + " degrees Fahrenheit at Virginia Beach",
                in_reply_to_status_id = tweet.id,
            )
        elif any("help" in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(
                status= "@" + tweet.user.screen_name + " Would you like to find out the current temperature in La Jolla or Virginia Beach?",
                in_reply_to_status_id = tweet.id,
            )
        else:
            logger.info(f"Answering to {tweet.user.name}")

            api.update_status(
            status= "@" + tweet.user.screen_name + " Could you please clarify where you want weather for? (La Jolla or Virginia Beach)",
            in_reply_to_status_id = tweet.id,)
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, ["help", "virginia beach", "la jolla"], since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()