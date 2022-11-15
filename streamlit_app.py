from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pymysql

conn = pymysql.connect(host='cse6242.czj7hqwhnoml.us-east-1.rds.amazonaws.com', user="admin",
                                        password="cse6242110", port=3306, database="realestate"
                                        )
query = "SELECT * FROM listings_enriched_final"
df = pd.read_sql(query, conn)
conn.close()

st.dataframe(df.head(1))

age_param = st.number_input("Please enter your age", min_value=0, max_value=None)
if age_param > 0:
  st.text(age_param)
 
cbsa_options = ['', 'Test1', 'test2']
cbsa = st.selectbox("Please select CBSA", options=cbsa_options)
if cbsa != '':
  st.text(cbsa)
