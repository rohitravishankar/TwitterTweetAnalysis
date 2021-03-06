"""
This microservice handles the process to consume the Kafka messages on the topic
to which Twitter Streaming API is producing data.

Author: Rohit Ravishankar
Email: rr9105@rit.edu
"""

import logging
import yaml
import json
from flask import Flask
from kafka import KafkaConsumer
from pymongo import MongoClient
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

with open('storetweetsconfig.yaml') as config_file:
    try:
        twitter_streaming_config = yaml.safe_load(config_file)
    except yaml.YAMLError as exc:
        print(exc)

# Adding basic config values to the logger
logging.basicConfig(
    filename=twitter_streaming_config['logging']['filename'],
    format=twitter_streaming_config['logging']['format'],
    level=logging.INFO,
    datefmt=twitter_streaming_config['logging']['datefmt']
)


@api.route('/receive-stream')
class TwitterConsumer(Resource):
    """
    Class to handle consumption of twitter stream data
    """

    @api.expect(
        api.model(
            'Start-Stream',
            {
                'topic': fields.String('The topic name'),
            }
        )
    )
    def post(self):
        """
        This handles consuming for the given topic

        :return: None
        """
        consumer = KafkaConsumer(
            api.payload['topic'],
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=None,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        for tweet in consumer:
            client = MongoClient('localhost', 27017)
            db = client['twitter_data']
            collection = db['twitter_stream_data']
            tweet = json.loads(tweet.value)
            collection.insert_one(tweet)
            print(tweet)


if __name__ == '__main__':
    app.run()
