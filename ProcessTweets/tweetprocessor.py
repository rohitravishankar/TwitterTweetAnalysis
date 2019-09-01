"""
This handles the process to get data from the MongoDB database, process it and produce the cleaned tweets towards
a topic in Kafka

Author: Rohit Ravishankar
Email: rr9105@rit.edu
"""
import logging
import time
import json
import preprocessor
from pymongo import MongoClient
from kafka import KafkaProducer


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
        for document in collection.find({}):
            clean_tweet_dict = self.cleaned_tweet_information(document)
            producer = KafkaProducer(bootstrap_servers=['localhost:9092']
                                     , value_serializer=lambda x: json.dumps(x).encode('utf-8'))
            print(clean_tweet_dict)
            producer.send(self.topic, value=clean_tweet_dict)

    def cleaned_tweet_information(self, document):
        """
        To create a JSON/dictionary representation of the information after cleaning the tweet

        :param document: The MongoDB document or tweet to be cleaned
        :return: dictionary representing the cleaned tweet
        """
        clean_tweet_dict = dict()
        clean_tweet_dict['created_at'] = self.normalize_timestamp(document['created_at'])
        clean_tweet_dict['source'] = self.get_source(document['source'])
        clean_tweet_dict['text'], clean_tweet_dict['tags'] = self.clean_tweet_text(document['text'])
        clean_tweet_dict['user_friends_count'] = document['user']['friends_count']
        clean_tweet_dict['user_favourites_count'] = document['user']['favourites_count']
        clean_tweet_dict['user_statuses_count'] = document['user']['statuses_count']
        clean_tweet_dict['user_created_at'] = self.normalize_timestamp(document['user']['created_at'])
        return clean_tweet_dict

    def get_source(self, source):
        """
        To get the source of the tweet for the user

        :param source: The source text from the tweet to extract the source
        :return: Source of the tweet, i.e., Web, iPhone or Android
        """
        if 'Web' in source:
            return 'Web'
        elif 'iPhone' in source:
            return 'iPhone'
        else:
            return 'Android'

    def clean_tweet_text(self, text):
        """
        To clean the tweet text

        :param text: The text to be cleaned
        :return: Cleaned text
        """
        text = preprocessor.clean(text)
        text = text.lower()
        list_of_words = text.split(" ")

        # We want to eliminate the first word if the text has "RT", implying it is a re-tweet
        if list_of_words[0] == "rt":
            list_of_words.pop(0)
        tags = list(set(list_of_words).intersection(self.stars))

        # Tagging the list so as to aid indexing and searching capability
        tags.extend([tags[0] + " " + tags[1], tags[1] + " " + tags[0]])
        return text, tags

    def normalize_timestamp(self, time_stamp):
        """
        To normalize the time stamp from "Day Month Date H:M:S Timezone Year" to
        "YYYY-MM-DD H:M:S" format

        :param time_stamp: The time stamp in the aforementioned format
        :return: time in Python datetime format of "YYYY-MM-DD H:M:S"
        """
        return time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(time_stamp, '%a %b %d %H:%M:%S +0000 %Y'))
