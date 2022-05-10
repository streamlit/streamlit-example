import streamlit as st
import pandas as pd

df = pd.read_csv('test_streamlit_file.csv')

st.write("Coef avg in germany: "+str(df['Coefficient'].mean()))
