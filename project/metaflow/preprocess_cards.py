# pylint: disable-all
import numpy as np
from pyspark.sql import functions as fn
import json
import os
import os.path
import shutil
from metaflow import FlowSpec, Parameter, step

import config
import preprocess_fn

from mf_common_base import MF_Common_Base

# Fetch of create spark session
spark = preprocess_fn.spark_session()


class BasicPreprocessing(FlowSpec, MF_Common_Base):
    VALID_CLEANUP = ["none", "all", "parquet", "models"]
    cleanUp = Parameter("cleanUp", type=str, default="none")

    @step
    def start(self):
        """ Begin here. """

        self.list_keyruneCodes = list()

        keyruneCodes = self.keyruneCodes
        if "," not in keyruneCodes:
            keyruneCodes += ","

        for code in keyruneCodes.split(","):
            json_file = f"{config.OUTPUT_DATASET}/{code}.json"

            if os.path.exists(json_file):
                self.list_keyruneCodes.append(code)

        if self.cleanUp == "all":
            for code in self.list_keyruneCodes:
                self.cleanUp_for_code(code)

        self.next(self.process, foreach="list_keyruneCodes")

    @step
    def process(self):
        """ Read data. """

        self.code = self.input

        if self.code in self.cleanUp:
            self.cleanUp_for_code(self.code)
        self.prepare_dirs_for_code(self.code)

        # Load json
        df = spark.read.json(f"{config.OUTPUT_DATASET}/{self.code}.json")

        # Remove duplicates
        df_filtered = preprocess_fn.remove_duplicate_cards(df)

        # Drop columns
        df_filtered = preprocess_fn.drop_columns(df_filtered)

        # Filter the text
        df_filtered = df_filtered.withColumn(
            "filtered_text", preprocess_fn.udf_filter_text("name", "text")
        )

        # Explode the selected arrays in a string, separated by ","
        df_filtered = preprocess_fn.explode_to_strs(
            df_filtered, ["colorIdentity", "types", "subtypes", "supertypes"]
        )

        # Encode the newly created strings
        df_filtered = preprocess_fn.encode_strings(
            df_filtered,
            [
                "rarity",
                "str_colorIdentity",
                "str_types",
                "str_subtypes",
                "str_supertypes",
            ],
            self.code,
        )

        # Count the number of colors
        df_filtered = df_filtered.withColumn("num_colors", fn.size("colors"))

        # Add keyruneCode column (will be useful when exporting the cards to MongoDB)
        df_filtered = df_filtered.withColumn("keyruneCode", fn.lit(self.code))

        # Create an SQL table
        df_filtered.createOrReplaceTempView(f"{self.code}_cards")

        tbl = spark.sql(
            f"""
            SELECT
                CAST(number as Integer),
                scryfallId,
                keyruneCode,
                name,
                rarity,
                CAST(convertedManaCost as Integer),
                CAST(num_colors as Integer) as numColors,
                str_colorIdentity as colorIdentity,
                CAST(encoded_str_colorIdentity as Integer) as encodedColorIdentity,
                str_types as types,
                CAST(encoded_str_types as Integer) as encodedTypes,
                str_subtypes as subTypes,
                CAST(encoded_str_subtypes as Integer) as encodedSubTypes,
                str_supertypes as superTypes,
                CAST(encoded_str_supertypes as Integer) as encodedSuperTypes,
                text as originalText,
                filtered_text as filteredText,
                CAST(power as Integer),
                CAST(toughness as Integer)
            FROM
                {self.code}_cards
            """
        )

        # Save to Parquet.
        tbl.write.mode("overwrite").parquet(f"{config.TEMP}/{self.code}_cards.parquet")

        # Move to our project's directory.
        shutil.copytree(
            f"{config.TEMP}/{self.code}_cards.parquet",
            f"{config.OUTPUT_DATASET}/{self.code}_cards.parquet",
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
    BasicPreprocessing()
