from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

age_param = st.number_input("Please enter your age", min_value=0, max_value=None)
if age_param > 0:
  st.text(age_param)
 
cbsa_options = ['', 'Test1', 'test2']
cbsa = st.selectbox("Please select CBSA", options=cbsa_options)
if cbsa != '':
  st.text(cbsa)
