from pyspark.sql import types as T


COLOR_SCHEMA = T.StructType([
    T.StructField("color", T.StringType(), False),
    T.StructField("code", T.IntegerType(), False),
])