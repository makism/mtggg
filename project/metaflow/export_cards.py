# pylint: disable-all

import json
import os.path
from metaflow import FlowSpec, Parameter, step
from jinja2 import Environment, FileSystemLoader, Template
from datetime import datetime as dt
import requests
import shutil

import config
import preprocess_fn

from mf_common_base import MF_Common_Base


class ExportCards(FlowSpec, MF_Common_Base):
    elasticsearch_clean = Parameter("elasticsearch-clean", type=str, default="none")
    mongodb_clean = Parameter("mongodb-clean", type=str, default="none")

    @step
    def start(self):
        """ Begin here. """

        self.parse_keyruneCodes(ftype="parquet")

        #################
        # Clean MongoDB #
        #################
        if self.mongodb_clean == "all":
            from pymongo import MongoClient

            client = MongoClient("mongodb://localhost:27017/")
            db = client["mtggg"]
            col = db["cards"]
            col.drop()

        #######################
        # Clean ElasticSearch #
        #######################
        if self.elasticsearch_clean == "all":
            requests.delete("http://localhost:9200/mtggg")
            requests.put(
                "http://localhost:9200/mtggg",
                data={
                    '"settings": {"index": {"number_of_shards": 1, "number_of_replicas": 1}}'
                },
            )

        self.next(self.export_to_mongo, foreach="list_keyruneCodes")

    @step
    def export_to_mongo(self):
        """ Export data to MongoDB. """
        self.code = self.input

        # Remove cards for a specific set
        if self.code in self.mongodb_clean:
            from pymongo import MongoClient

            client = MongoClient("mongodb://localhost:27017/")
            db = client["mtggg"]
            col = db["cards"]

            col.delete_many({"keyruneCode": self.code})

        df = self.load_parquet_for_keyrune(self.code)

        import pymongo_spark

        pymongo_spark.activate()
        as_dict = df.rdd.map(lambda row: row.asDict())
        as_dict.saveToMongoDB(f"mongodb://localhost:27017/mtggg.cards")

        self.next(self.export_to_es)

    @step
    def export_to_es(self):
        """ Export to ElasticSearch. """
        self.code = self.input

        # Remove cards for a specific set
        if self.code in self.elasticsearch_clean:
            requests.post(
                "http://localhost:9200/mtggg/cards/_delete_by_query",
                data="""
        {
          "query": {
            "match" : {
                "keyruneCode" : "{self.code}"
            }
          }
        }
        """.replace(
                    "{self.code}", self.code
                ),
            )

        df = self.load_parquet_for_keyrune(self.code)

        df.write.format("org.elasticsearch.spark.sql").option(
            "es.resource", "mtggg/cards"
        ).option("es.batch.size.entries", "100").mode("overwrite").save()

        self.next(self.join)

    @step
    def join(self, inputs):
        """Join our parallel branches."""

        self.next(self.end)

    @step
    def end(self):
        """ Finalize and clean up. """

        print("All done.")


if __name__ == "__main__":
    ExportCards()
