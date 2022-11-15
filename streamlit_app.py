from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pymysql

conn = pymysql.connect(host='cse6242.czj7hqwhnoml.us-east-1.rds.amazonaws.com', user="admin",
                                        password="cse6242110", port=3306, database="realestate"
                                        )
query = "SELECT '' AS cbsatitle UNION SELECT DISTINCT cbsatitle FROM listings_enriched_final ORDER BY 1"
cbsa_data = pd.read_sql(query, conn)

st.selectbox("Please select CBSA", options=cbsa_data)

# if cbsa != '':
#   st.text(cbsa)

age_param = st.number_input("Please enter your age", min_value=0, max_value=None)
if age_param > 0:
  st.text(age_param)

conn.close()
