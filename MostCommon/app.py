"""
This handles the API end points for the functionality provided, including,
listing the most commonly used words for the given subset of data got from Twitter's Streaming API

Author: Rohit Ravishankar
Email: rr9105@rit.edu
"""

import logging
import json
import yaml
from flask import Flask
from flask_restplus import Api, Resource, fields

with open('mostcommonwords.yaml') as config_file:
    try:
        most_common_words_config = yaml.safe_load(config_file)
    except yaml.YAMLError as exc:
        print(exc)
        
# Adding basic config values to the logger
logging.basicConfig(
    filename=most_common_words_config['logging']['filename'],
    format=most_common_words_config['logging']['format'],
    level=logging.INFO,
    datefmt=most_common_words_config['logging']['datefmt']
)


app = Flask(__name__)
api = Api(app)


@api.route('/mostcommonwords')
class MostCommonWord(Resource):
    """
    Class returns the most common words
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



if __name__ == '__main__':
    app.run()
