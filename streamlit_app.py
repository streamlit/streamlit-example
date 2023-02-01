import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import pyspark
from pyspark.sql import SparkSession

st.title("Quality Checker")
st.write("This application will allow you to upload your dataset and run a quality check on it.")
st.markdown("---")

st.subheader("Upload your files here : ")

upload_data = st.file_uploader("Choose a CSV file", type = ['CSV'])
if upload_data is not None:
    read_data = pd.read_csv(upload_data, encoding='latin-1',on_bad_lines='skip')

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


st.write("Dataset Schema ")
schema = read_data.printSchema()
st.markdown("---")
