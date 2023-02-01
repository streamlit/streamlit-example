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

st.title("Quality Checker")
st.write("This application will allow you to upload your dataset and run a quality check on it.")
st.markdown("---")


# Uploading the dataset
st.subheader("Upload your files here : ")

upload_data = st.file_uploader("Choose a CSV file", type = ['CSV'])
if upload_data is not None:
    read_data = spark.read.csv(upload_data, sep=',',inferSchema=True, header=True)

#read_data = read_data
#st.subheader('Data Quality Dashboard')
#null_values = read_data.isnull().sum()/len(read_data)*100
#st.progress(null_values)
st.markdown("---")


st.write("Dataset Overview : ")
try:
    number_of_rows = st.slider("No of rows:",5,10)
    head = st.radio("View from Top or Bottom",('Head','Tail'))
    if head=='Head':
        st.dataframe(read_data.head(number_of_rows))
    else:
        st.dataframe(read_data.tail(number_of_rows))
except:
    st.info("KINDLY UPLOAD YOUR CSV FILE !!!")
    st.stop()
st.markdown("---")

read_data.printSchema()

st.markdown("---")
