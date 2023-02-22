import json
import threading
from kafka import KafkaConsumer
from pymongo_get_database import get_database
from datetime import datetime
from data_generator import createGraph

def save_source_descriptions():
    collection_name = dbname["domain_name_description"]

    #Insert producer's messeges in MongoDB for topic sourceDomainNames
    for message in consumerOfDomainNames:
        data = json.loads(message.value)
        for value in data:
            if value is not None:
                collection_name.insert_one({
                    'title' :value.get('title') ,
                    'description' : value['description']
                })
 
def save_author_tweets():
    collection_name = dbname["tweets"]
    #Insert producer's messeges in MongoDB for topic sourceDomainNames
    for message in consumerOfTweets:
        data = json.loads(message.value)
        print(data)
        for value in data:
            if value is not None:
                collection_name.insert_one({
                    'author' :value[0] ,
                    'tweets' : value[1]
            })

def save_articles():
    #Insert producer's messeges in MongoDB for multi article topics
    for message in consumerOfTopics:
        collection_name = dbname[message.topic]
        articles = json.loads(message.value)
        for article in articles.get('articles'):
            collection_name.insert_one({'Published':datetime.now(),'article' : article})
        createGraph()



if __name__ == '__main__':
    #Connect with mongoDB
    dbname = get_database()    

    topics = ['tesla', 'apple', 'microsoft', 'nasa', 'amazon', 'BBC', 'cloud', 'fiat'] 

    # Kafka Consumers
    consumerOfTopics = KafkaConsumer(
        *topics,
        bootstrap_servers='34.138.148.38:9092',
        auto_offset_reset='earliest'
    )

    consumerOfDomainNames = KafkaConsumer(
        'sourcesDomainName',
        bootstrap_servers='34.138.148.38:9092',
        auto_offset_reset='earliest'
    )

    consumerOfTweets = KafkaConsumer(
        'tweets_for_authors',
        bootstrap_servers='34.138.148.38:9092',
        auto_offset_reset='earliest'
    )

    t1 = threading.Thread(target=save_source_descriptions)
    t2 = threading.Thread(target=save_articles)
    t3 = threading.Thread(target=save_author_tweets)
 
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
    t3.start()
 
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()

    t3.join()