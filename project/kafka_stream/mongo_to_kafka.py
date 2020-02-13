from time import sleep
from json import dumps
import sys
import os
from pymongo import MongoClient
from kafka import KafkaProducer

if __name__ == "__main__":
    os.system(
        "/home/vagrant/opt/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic tweets"
    )

    mongo_client = MongoClient("localhost:27017")
    collection = mongo_client.mtg_tweets.all

    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda x: dumps(x).encode("utf-8"),
    )

    topic = "tweets"
    for e in range(1000):
        data = {"number": e}
        # print("{0} {1}".format(topic, data))
        producer.send(topic, value=data)
        # sleep(5)

    print("Done.")
