import streamlit as st
import pandas as pd

df = pd.read_csv('test_streamlit_file.csv')

title = st.text_input('Movie title', 'Life of Brian')
