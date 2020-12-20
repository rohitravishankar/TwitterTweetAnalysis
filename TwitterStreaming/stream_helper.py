"""
This handles the process to get stream data from twitter and use a Kafka Producer to produce towards a topic

Author: Rohit Ravishankar
Email: rr9105@rit.edu
"""

import tweepy
import os
import logging
import json
from kafka import KafkaProducer
from http.client import IncompleteRead

# Credentials to access Twitter Streaming Data
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']


class TwitterStreamer:
    """
    Class for streaming tweets from Twitter
    """

    def __init__(self, topic_name, hash_tag_list):
        self.topic_name = topic_name
        self.hash_tag_list = hash_tag_list

    def stream_tweets(self):
        """
        This handles Twitter authentication and the connection to Twitter Streaming API

        :return: None
        """
        # This handles Twitter authentication and the connection to Twitter Streaming API
        listener = StdOutListener(self.topic_name)
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        stream = tweepy.Stream(auth, listener)

        while True:
            try:
                # This line filter Twitter Streams to capture data by the keywords:
                stream.filter(track=self.hash_tag_list, stall_warnings=True)
            except IncompleteRead:
                # If my consumer falls behind don't error out but continue
                continue
            except KeyboardInterrupt:
                # Or however you want to exit this loop
                stream.disconnect()
                break


class StdOutListener(tweepy.StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, topic_name):
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092']
                                      , value_serializer=lambda x: json.dumps(x).encode('utf-8'))
        self.topic_name = topic_name

    def on_data(self, data):
        try:
            self.producer.send(self.topic_name, value=data)
            # sleep(3)
            print(data)
            return data
        except BaseException as e:
            logging.error("StdOutListener: Error found with error %s" % str(e))
        return True

    def on_error(self, status):
        if status != 200:
            logging.error("StdOutListener: Returning false on on_data method if rate limit is reached")
            return False

