"""
This handles the process to get data from the MongoDB database, process it and produce the cleaned tweets towards
a topic in Kafka

Author: Rohit Ravishankar
Email: rr9105@rit.edu
"""
import logging
import json
from pymongo import MongoClient
from kafka import KafkaProducer
from tweetcleaner import TweetClean


class TweetProcessor:
    """
    Class to process the Python tweets
    """
    def __init__(self, topic_name, stars):
        self.topic = topic_name
        self.stars = self.create_tags(stars)

    def create_tags(self, stars):
        """
        To create tags for the stars in concern

        :param stars: List of stars for whom we are performing analysis
        :return: List of tags to tag each tweet
        """
        list_of_tags = list()
        list_of_tags.extend(stars)
        for i in stars:
            list_of_tags.extend(i.split(" "))
        return list_of_tags

    def process_tweets(self):
        """
        To read the tweets from the MongoDB database, process the tweets, clean the text
        and push the cleaned tweets to a Kafka topic

        :return: None
        """
        try:
            client = MongoClient('localhost', 27017)
        except Exception as e:
            logging.error("Error connecting to DB")
        db = client['twitter_data']
        collection = db['twitter_stream_data']
        producer = KafkaProducer(bootstrap_servers=['localhost:9092']
                                 , value_serializer=lambda x: json.dumps(x).encode('utf-8'))
        document = None
        while document in collection.find({}):
            clean_tweet_dict = TweetClean(self.stars).cleaned_tweet_information(document)
            print(clean_tweet_dict)
            if clean_tweet_dict:
                producer.send(self.topic, value=str(clean_tweet_dict))
            else:
                continue

