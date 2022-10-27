# pylint: disable= W0703, W0622, W0401, W0613
'''
Fetches raw tweets from twitter's api and pushes them to a kafka topic
'''
from pathlib import Path
import os
from json import dumps
import tweepy
from kafka import KafkaProducer
from retry import retry
from dotenv import load_dotenv
from requests.exceptions import RequestException
from requests.models import HTTPError
from requests.sessions import TooManyRedirects

dotenv_path = Path('/home/zain/Documents/credentials.env')
DATA=load_dotenv(dotenv_path=dotenv_path)
bearer_token = os.getenv("bearer_token")
KAFKA_BOOTSTRAP_SERVER=os.getenv("KAFKA_BOOTSTRAP_SERVER")

search_terms = ["formula 1", "f1", "formula1"]
producer = KafkaProducer(bootstrap_servers=\
[KAFKA_BOOTSTRAP_SERVER],\
value_serializer=lambda x: dumps(x).encode('utf-8'))

class MyStream(tweepy.StreamingClient):
    '''
    Inheritd twitter's streaming client and pushes the tweet to a kafka topic
    '''
    def on_connect(self):
        print("Connected")
    @retry((ValueError, TypeError, ConnectionError, \
    HTTPError, TimeoutError, TooManyRedirects, \
    RequestException), delay=5, tries=10, max_delay=4)
    def on_tweet(self, tweet):

        if tweet.referenced_tweets is None:
            data = {'tweet' : tweet.text}
            try:
                producer.send('tweets', value=data)
            except Exception as error:
                print(error)
# Creating Stream object
@retry((ValueError, TypeError, ConnectionError, \
HTTPError, TimeoutError, TooManyRedirects, \
RequestException), delay=5, tries=10, max_delay=4)
def main():
    '''
    Authenticates twitter's streaming API, adds rules and filters stream on matches
    '''
    try:
        stream = MyStream(bearer_token=bearer_token)
    except Exception as error:
        print(error)
    for term in search_terms:
        try:
            stream.add_rules(tweepy.StreamRule(term))
        except Exception as error:
            print(error)
            continue
    # Starting stream
    try:
        stream.filter(tweet_fields=["referenced_tweets"])
    except Exception as error:
        print(error)
if __name__ == "__main__":
    main()
