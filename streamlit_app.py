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
cbsa_param = st.selectbox("Please select CBSA", options=cbsa_data)

col1, col2, col3, col4 = st.columns(4)

with col1:
  bedroom_param = st.number_input("Please enter # of bedrooms", min_value=0, max_value=7)

  bathroom_param = st.number_input("Please enter # of bathrooms", min_value=0, max_value=7)
  
  year_built_param = st.number_input("Please enter min year built", min_value=1900, max_value=2022)
  
  
with col2:
  income_param = st.number_input("Please enter your income", min_value=0, max_value=300000)

  square_feet_param = st.number_input("Please enter min square feet", min_value=0, max_value=10000)
  
  price_param = st.number_input("Please enter min price", min_value=0, max_value=1000000)

  education_options = ['', 'Graduate', 'Bachelors', 'High School Diploma', 'Associates or Equivelant', 'No Diploma']
  education_options_param = st.selectbox("Please select education level", options=education_options)
  

with col3:
  age_param = st.number_input("Please enter your age", min_value=0, max_value=100)  
  
  home_type_options = ['', 'Condo', 'Single Family', 'Townhouse']
  home_type_param = st.selectbox("Please select your home type", options=home_type_options)

  family_options = ['', 'Yes', 'No']
  family_param = st.selectbox("Do you have a family", options=family_options)  
  

with col4:
  school_param = st.number_input("Please enter your importance of school (higher is more important)", min_value=0, max_value=10)  
  
  centrality_param = st.number_input("Please enter your desired closeness to downtown (higher is closer)", min_value=0.0, max_value=1.0)  


# if age_param > 0:
#   st.text(age_param)

conn.close()
