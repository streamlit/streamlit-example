import numpy as np
import pandas as pd
from pyspark import SparkConf
from pyspark.sql import SparkSession

def _initialize_spark() -> SparkSession:
    """Create a Spark Session for Streamlit app"""
    conf = SparkConf().setAppName("lecture-lyon2").setMaster("local")
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    return spark, spark.sparkContext
