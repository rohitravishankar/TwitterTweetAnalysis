"""
This handles the process to clean the tweet data

Author: Rohit Ravishankar
Email: rr9105@rit.edu
"""
import string
import time
import preprocessor
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# HappyEmoticons
emoticons_happy = [
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ]

# Sad Emoticons
emoticons_sad = [
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ]

#Emoji patterns
emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)

# combine sad and happy emoticons
emoticons = set(emoticons_happy).union(set(emoticons_sad))


class TweetClean:
    def __init__(self, stars):
        self.stars = stars

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
        return False if not clean_tweet_dict['text'] else clean_tweet_dict

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

        tags = list(set(text.split(" ")).intersection(self.stars))
        if not tags:
            return False, False
        # Tagging the list so as to aid indexing and searching capability
        tags.extend([tags[0] + " " + tags[1], tags[1] + " " + tags[0]])

        stop_words = set(stopwords.words('english'))
        text = re.sub(r':', '', text)
        text = re.sub(r'‚Ä¶', '', text)
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        text = emoji_pattern.sub(r'', text)
        word_tokens = word_tokenize(text)
        filtered_text = []
        # looping through conditions
        for w in word_tokens:
            # check tokens against stop words , emoticons and punctuations
            if w not in stop_words and w not in emoticons and w not in string.punctuation:
                filtered_text.append(w)
        text = ' '.join(filtered_text)

        return text, tags

    def normalize_timestamp(self, time_stamp):
        """
        To normalize the time stamp from "Day Month Date H:M:S Timezone Year" to
        "YYYY-MM-DD H:M:S" format

        :param time_stamp: The time stamp in the aforementioned format
        :return: time in Python datetime format of "YYYY-MM-DD H:M:S"
        """
        return time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(time_stamp, '%a %b %d %H:%M:%S +0000 %Y'))