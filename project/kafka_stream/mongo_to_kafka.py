from time import sleep
from json import dumps
import sys
from pymongo import MongoClient
from kafka import KafkaProducer

if __name__ == "__main__":
    mongo_client = MongoClient("localhost:27017")
    collection = mongo_client.mtg_tweets.all

    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda x: dumps(x).encode("utf-8"),
    )

    # topic = "numtest"
    # for e in range(1000):
    #     data = {"number": e}
    #     producer.send(topic, value=data)
    #     print("{0} {1}".format(topic, data))
    #     sleep(5)

    print("Done.")
