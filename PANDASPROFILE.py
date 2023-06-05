import pandas as pd
import pandas_profiling
import streamlit as st

from streamlit_pandas_profiling import st_profile_report

st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data('https://drive.google.com/file/d/1TvB62joGvnJjfSfQ5GQSOcJ5vZzBxVar/view?usp=sharing')
#st.dataframe(df)

st.button("Rerun")

#df = pd.read_csv('https://drive.google.com/file/d/1TvB62joGvnJjfSfQ5GQSOcJ5vZzBxVar/view?usp=sharing')
#uploaded_file = st.file_uploader("Choose a file")
#if uploaded_file is not None:
#  df = pd.read_csv(uploaded_file)
  
pr = df.profile_report()

st_profile_report(pr)
