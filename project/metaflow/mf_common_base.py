# pylint: disable-all

import os.path
import shutil
from metaflow import FlowSpec, Parameter, step

import config
import preprocess_fn


class MF_Common_Base(object):
    VALID_KEYRUNECODES = ["M21", "IKO", "THB", "ELD", "M20", "WAR"]
    keyruneCodes = Parameter(
        "keyruneCodes", default=",".join(keyrune for keyrune in VALID_KEYRUNECODES)
    )

    file_json = f"{config.DATASET}/%s.json"
    file_parquet = f"{config.OUTPUT_DATASET}/%s_cards.parquet"

    def parse_keyruneCodes(self, ftype="json"):
        """ """
        self.list_keyruneCodes = list()
        result = list()

        keyruneCodes = self.keyruneCodes
        if "," not in keyruneCodes:
            keyruneCodes += ","

        fpattern = (
            MF_Common_Base.file_json if ftype == "json" else MF_Common_Base.file_parquet
        )

        for code in keyruneCodes.split(","):
            if code in MF_Common_Base.VALID_KEYRUNECODES:
                check_file = fpattern % (code)

                if os.path.exists(check_file):
                    result.append(code)

        self.list_keyruneCodes = result

        return result

    def load_parquet_for_keyrune(self, code):
        """ Load a Parquet file into a DataFrame. """
        parquet_file = f"{config.OUTPUT_DATASET}/{code}_cards.parquet"

        spark = preprocess_fn.spark_session()

        df = spark.read.parquet(parquet_file)

        return df

    def cleanUp_for_code(self, code):
        tmp_dir = f"{config.TEMP}/{code}_cards.parquet"
        models_dir = f"{config.SPARK_MODELS}/{code}"
        dataset_dir = f"{config.OUTPUT_DATASET}/{code}_cards.parquet"

        clean_dirs = [tmp_dir, models_dir, dataset_dir]
        for clean_whichdir in clean_dirs:
            print(f"Will clean {clean_whichdir}...")
            shutil.rmtree(clean_whichdir, ignore_errors=True)

    def prepare_dirs_for_code(self, code):
        dir_spark_models = f"{config.SPARK_MODELS}/{code}/"

        if not os.path.exists(dir_spark_models):
            os.mkdir(f"{config.SPARK_MODELS}/{code}/")
