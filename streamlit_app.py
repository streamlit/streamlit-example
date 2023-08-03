import streamlit as st
import pickle
import os

file_list = os.listdir('test_files')
file_name = st.selectbox('Select File', file_list)

with open(file_name, 'rb') as file:
    data = pickle.load('test_files/' + file_name)
text = data['text']
html = f'<div style="direction: rtl; text-align: right;">{text}</div>'
st.markdown(f"<div style='direction: rtl; text-align: right;'>{html}</div></br>", unsafe_allow_html=True)

