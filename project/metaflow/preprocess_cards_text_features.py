# pylint: disable-all
import numpy as np
from pyspark.sql import functions as fn
import pyspark
import pyspark.sql.functions as fn
import pyspark.sql.types as t
from sklearn import preprocessing
import json
import os
import os.path
import shutil
import pickle
import itertools
from metaflow import FlowSpec, Parameter, step

import config
import preprocess_fn
import preprocess_fn_text_rules

from mf_common_base import MF_Common_Base

# Fetch of create spark session
spark = preprocess_fn.spark_session()


class BasicTextPreprocessing(FlowSpec, MF_Common_Base):
    VALID_CLEANUP = ["none", "all", "parquet", "models"]
    cleanUp = Parameter("cleanUp", type=str, default="none")

    @step
    def start(self):
        """ Begin here. """

        self.parse_keyruneCodes(ftype="parquet")

        # if self.cleanUp == "all":
        # for code in self.list_keyruneCodes:
        # self.cleanUp_for_code(code)

        self.next(self.process, foreach="list_keyruneCodes")

    @step
    def process(self):
        """ Read data. """

        self.code = self.input

        # if self.code in self.cleanUp:
        # self.cleanUp_for_code(self.code)
        # self.prepare_dirs_for_code(self.code)

        # Load parquet
        df = spark.read.parquet(f"{config.OUTPUT_DATASET}/{self.code}_cards.parquet")

        # Replace text with keywords based on a dictionary
        df = df.withColumn(
            "text_features1", preprocess_fn.udf_text_to_keywords("name", "originalText")
        )

        from_patterns = [
            fn.when(
                fn.regexp_extract("originalText", r"{0}".format(pattern), 0) != "",
                replace,
            ).otherwise("")
            for pattern, replace in preprocess_fn_text_rules.text_patterns.items()
        ]

        df = df.withColumn("text_features2", fn.array(*from_patterns))
        df = df.withColumn(
            "text_features", fn.array_union("text_features1", "text_features2")
        )

        # df.select("text_features").distinct().show(100, truncate=False)

        # Fetch all the text features from all the cards into one list
        all_text_feats = df.select("text_features").rdd.flatMap(lambda x: x).collect()

        filtered_text_feats = [items for items in all_text_feats if len(items) > 0]
        filtered_text_feats = list(itertools.chain.from_iterable(filtered_text_feats))

        # Encode the text features into ints
        label_encoder = preprocessing.LabelEncoder().fit(filtered_text_feats)
        with open(f"{config.TEMP}/labelencoder_text_feats.pkl", "wb") as fp:
            pickle.dump(label_encoder, fp)

        @fn.udf(returnType=t.ArrayType(t.IntegerType()))
        def text_to_vector(text_features):
            if len(text_features) > 0:
                enc_list = list()
                for item in text_features:
                    item = str(item)
                    encoded = label_encoder.transform([item])
                    encoded = int(encoded[0])
                    enc_list.append(encoded)
                #             print(f"{item} \t {encoded}")
                return enc_list
            return list()

        # if "text_features_vect" in df.columns:
        # df = df.drop("text_features_vect")

        df = df.withColumn("text_features_vect", text_to_vector("text_features"))

        all_text_feats = df.select("text_features").rdd.flatMap(lambda x: x).collect()

        filtered_text_feats = [items for items in all_text_feats if len(items) > 0]
        filtered_text_feats = list(itertools.chain.from_iterable(filtered_text_feats))

        df.createOrReplaceTempView("cards_features")

        tbl = spark.sql(
            """
            SELECT
                *
            FROM
                cards_features
        """
        )

        # Save to Parquet
        tbl.write.mode("overwrite").parquet(
            f"{config.TEMP}/{self.code}_cards_text.parquet"
        )

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
    BasicTextPreprocessing()
