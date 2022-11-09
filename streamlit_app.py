from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

age_param = st.number_input("Please enter your age", min_value=0, max_value=None)
if age_param > 0:
  st.text(age_param)
  
