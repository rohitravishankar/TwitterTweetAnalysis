"""
This microservice handles the process to get stream data from twitter and
uses a Kafka Producer to produce towards a topic

Author: Rohit Ravishankar
Email: rr9105@rit.edu
"""

import logging
import yaml
from flask import Flask
from stream_helper import TwitterStreamer
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

with open('twitterstreamingconfig.yaml') as config_file:
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


@api.route('/start-stream')
class StreamTwitterData(Resource):

    @api.expect(
        api.model('Start-Stream',
              {
                  'topic': fields.String('The topic name'),
                  'hash-tags': fields.String('A list of hash tags')
              }
        )
    )
    def post(self):
        """
        To stream twitter data from the twitter API when this end point is hit

        :return: Result from the TwitterStreamer class which is the status code
        """
        return TwitterStreamer(api.payload['topic'], api.payload['hash-tags']).stream_tweets()


if __name__ == '__main__':
    app.run()
