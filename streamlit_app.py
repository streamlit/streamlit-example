import streamlit as st
import pickle

file_name = 'evaluation_asherlishlomo-011.txt.p.p'
with open(file_name, 'rb') as file:
    data = pickle.load(file)
text = data['text']
html = f'<div style="direction: rtl; text-align: right;">{text}</div>'
st.markdown(f"<div style='direction: rtl; text-align: right;'>{html}</div></br>", unsafe_allow_html=True)

