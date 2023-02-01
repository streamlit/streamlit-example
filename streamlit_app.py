from pyspark.rdd import RDD
from pyspark.sql import Row
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import pyspark
import jdk
from pyspark.sql import SparkSession
from utils import _initialize_spark


st.write("# :tada: Hello Pyspark")

spark, sc = _initialize_spark()
st.write("[Link to Spark window](http://localhost:4040)")

st.write("## Create RDD from a Python list")
