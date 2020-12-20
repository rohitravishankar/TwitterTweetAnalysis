"""
This microservice handles the process to retrieve tweets data from the mongodb database
to clean it and push to a Kafka topic

Author: Rohit Ravishankar
Email: rr9105@rit.edu
"""

import logging
import yaml
from flask import Flask
from flask_restplus import Api, Resource, fields
from tweetprocessor import TweetProcessor

app = Flask(__name__)
api = Api(app)

with open('processtweetsconfig.yaml') as config_file:
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


@api.route('/clean-tweets')
class StreamTwitterData(Resource):

    @api.expect(
        api.model('Clean-Tweets',
              {
                  'topic': fields.String('The topic name to push the cleaned tweets towards'),
                  'stars': fields.String('The stars who are in consideration')
              }
        )
    )
    def post(self):
        """
        To read data from the database and process it by cleaning the tweets

        :return: Result from the TweetProcess class
        """
        return TweetProcessor(api.payload['topic'], api.payload['stars']).process_tweets()


if __name__ == '__main__':
    app.run()
