import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import pyspark
import jdk
from utils import _initialize_spark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType 
from pyspark.sql.types import ArrayType, DoubleType, BooleanType
from pyspark.sql.functions import col,array_contains


st.write("# :tada: Hello Pyspark")

spark, sc = _initialize_spark()
st.write("[Link to Spark window](http://localhost:4040)")

st.write("## Create RDD from a Python list")
