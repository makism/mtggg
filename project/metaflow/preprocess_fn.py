import sys
import pandas as pd
import numpy as np
import pyspark
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as fn
import pyspark.sql.types as t
from pyspark.sql.functions import udf
from pyspark.ml.feature import StringIndexer, IndexToString


sys.path.append("../config/")
import config

import preprocess_fn_text_rules

text_rules = preprocess_fn_text_rules.text_rules


def spark_session(spark=None) -> pyspark.sql.SparkSession:
    """ Create or, get an existing Spark session. """
    if spark is None:
        spark = SparkSession.builder.appName("mtggg").getOrCreate()
    return spark


def remove_duplicate_cards(df) -> pyspark.sql.DataFrame:
    """ Remove duplicate card entries based on their name. """
    pd_names = df.select(["number", "name"]).toPandas()

    unique_names, indices, counts = np.unique(
        pd_names["name"], return_index=True, return_counts=True
    )

    pd_unique_names = pd_names.loc[indices]

    df_filter = spark_session().createDataFrame(pd_unique_names)
    df_filtered = df_filter.join(df, on="number", how="left").drop(df_filter.name)

    return df_filtered


def drop_columns(df) -> pyspark.sql.DataFrame:
    """ Drop unwanted columns. """
    keep_cols = [
        "colorIdentity",
        "convertedManaCost",
        "colors",
        "manaCost",
        "name",
        "number",
        "text",
        "power",
        "rarity",
        "subtypes",
        "supertypes",
        "toughness",
        "types",
    ]

    remove_cols = list(set(df.columns) - set(keep_cols))

    df_filtered = df.drop(*remove_cols)

    return df_filtered


@udf
def udf_filter_text(name, text):
    """ A simple UDF to search & replace occurances of a card's name with a placeholder. """
    if isinstance(text, str):
        new_text = text
        new_text = new_text.replace(name, "CARDNAME")

        for line in new_text:
            for rule, replace in text_rules.items():
                new_text = new_text.replace(rule, replace)

        return new_text


@fn.udf(returnType=t.ArrayType(t.StringType()))
def udf_text_to_keywords(name, text) -> pyspark.sql.types.ArrayType:
    """ """
    feats = list()
    if isinstance(text, str):
        new_text = text.replace(name, "CARDNAME")
        for line in new_text.split("\n"):
            for rule, replace in text_rules.items():
                if line.startswith(rule):
                    line = line.replace(rule, replace)
                    feats.append(replace)
    return feats


@fn.udf(returnType=t.ArrayType(t.IntegerType()))
def text_to_vector(label_encoder, text_features):
    lenc = label_encoder

    if len(text_features) > 0:
        enc_list = list()
        for item in text_features:
            item = str(item)
            encoded = lenc.transform([item])
            encoded = int(encoded[0])
            enc_list.append(encoded)

            print(f"{item} \t {encoded}")
        return enc_list
    return list()


def explode_to_strs(df, cols) -> pyspark.sql.DataFrame:
    """ Explode the selected arrays in a string, separated by ','. """
    for col in cols:
        df_edited = df.selectExpr(["number", col]).select(
            "number", fn.expr(f"concat_ws(',', {col})").alias(f"str_{col}")
        )
        df = df.join(df_edited, on="number")
    return df


def encode_strings(df, cols) -> pyspark.sql.DataFrame:
    """ """
    for col in cols:
        indexer = StringIndexer(
            inputCol=f"{col}", outputCol=f"encoded_{col}", stringOrderType="alphabetAsc"
        )
        model = indexer.fit(df)
        df = model.transform(df)

        indexer.save(f"/tmp/pyspark/stringindexer_{col}")
        model.save(f"/tmp/pyspark/stringindexer_model_{col}")

        # indexer.save(f"{config.SPARK_MODELS}/stringindexer_{col}")
        # model.save(f"{config.SPARK_MODELS}/stringindexer_model_{col}")
    return df
