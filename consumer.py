import json
import threading
from kafka import KafkaConsumer
from kafka.structs import TopicPartition
from pymongo_get_database import get_database

def save_source_descriptions():
    collection_name = dbname["domain_name_description"]

    #Insert producer's messeges in MongoDB for topic sourceDomainNames
    for message in consumerOfDomainNames:
        print(message.value)
        data = json.loads(message.value)
        collection_name.insert_one({'description' : data})

 
def save_articles():
    #Insert producer's messeges in MongoDB for multi article topics
    for message in consumerOfTopics:
        collection_name = dbname[message.topic]
        data = json.loads(message.value)
        collection_name.insert_one({message.topic : data})



if __name__ == '__main__':
    #Connect with mongoDB
    dbname = get_database()    

    topics = ['tesla', 'apple', 'microsoft', 'nasa', 'amazon', 'BBC', 'cloud', 'fiat'] 

    # Kafka Consumers
    consumerOfTopics = KafkaConsumer(
        *topics,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )

    consumerOfDomainNames = KafkaConsumer(
        'sourcesDomainName',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )

    t1 = threading.Thread(target=save_source_descriptions)
    t2 = threading.Thread(target=save_articles)
 
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
 
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()