import time
import json
from datetime import datetime
from data_generator import  get_articles, mediaWiki, domain_names_description, tweets_for_authors
from kafka import KafkaProducer
from pymongo_get_database import get_database
from bson import json_util


# Messages will be serialized as JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')


# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['34.138.148.38:9092'],
    value_serializer=serializer
)

if __name__ == '__main__':

    # Infinite loop - runs until you kill the program
    while True:

        topics = ['tesla', 'apple', 'microsoft', 'nasa', 'amazon', 'BBC', 'cloud', 'fiat'] 

        # Send article to our consumer
        for topic in topics:
            articles = get_articles(topic)
            authors_tweets = tweets_for_authors(articles)
            description = domain_names_description(articles)
            producer.send('tweets_for_authors', authors_tweets)
            producer.send(topic,  articles)
            producer.send('sourcesDomainName', description)

        # Sleep for two hours
        time_to_sleep = 3600 * 1000
        time.sleep(time_to_sleep)