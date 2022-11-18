from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pymysql

conn = pymysql.connect(host='cse6242.czj7hqwhnoml.us-east-1.rds.amazonaws.com', user="admin",
                                        password="cse6242110", port=3306, database="realestate"
                                        )

zipcode = None

st.markdown("<h1 style='text-align: center; color: white;'>Where should you live?</h1>", unsafe_allow_html=True)

if zipcode is not None:
  st.out("You should live in " + zipcode)

query = "SELECT '' AS cbsatitle UNION SELECT DISTINCT cbsatitle FROM listings_enriched_final ORDER BY 1"
cbsa_data = pd.read_sql(query, conn)
cbsa_param = st.selectbox("Select CBSA", options=cbsa_data)

col1, col2, col3, col4 = st.columns(4)

with col1:
  home_type_options = ['', 'Condo', 'Single Family', 'Townhouse']
  home_type_param = st.selectbox("Home Type", options=home_type_options)  
  
  bedroom_param = st.number_input("# of Bedrooms", min_value=0, max_value=7)

  bathroom_param = st.number_input("# of Bathrooms", min_value=0, max_value=7)
  
  
with col2:
  year_built_param = st.number_input("Min Year Built", min_value=1900, max_value=2022)  
  
  square_feet_param = st.number_input("Min Square Feet", min_value=0, max_value=10000)
  
  price_param = st.number_input("Min price", min_value=0, max_value=1000000)  

  

with col3:
  age_param = st.number_input("Age", min_value=0, max_value=100)  
  
  education_options = ['', 'Graduate', 'Bachelors', 'High School Diploma', 'Associates or Equivelant', 'No Diploma']
  education_options_param = st.selectbox("Education level", options=education_options)  
  
  income_param = st.number_input("Income", min_value=0, max_value=300000)
  

with col4:
  family_options = ['', 'Yes', 'No']
  family_param = st.selectbox("Do you have a family?", options=family_options)    
  
  important_options = ['', 'Not Important', 'Little Important', 'Important', 'Very Important']
  school_param = st.selectbox("Importance of School", options=important_options)  
  centrality_param = st.selectbox("Closeness to Downtown", options=important_options)  

if cbsa_param is not None and cbsa_param != '':
  zipcode = '123456'
  
conn.close()
