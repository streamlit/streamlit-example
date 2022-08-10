import streamlit as st
import pandas as pd

df = pd.read_csv('cricket_entry.csv')

title = st.text_input('Movie title', 'Life of Brian')
