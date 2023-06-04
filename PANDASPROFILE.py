import pandas as pd
import pandas_profiling
import streamlit as st

from streamlit_pandas_profiling import st_profile_report

df = pd.read_csv('https://drive.google.com/file/d/1dLzhkMdx58uzJIjhqyFSQBFPKAIiZXhT/view?usp=sharing')
#uploaded_file = st.file_uploader("Choose a file")
#if uploaded_file is not None:
#  df = pd.read_csv(uploaded_file)
  
pr = df.profile_report()

st_profile_report(pr)
