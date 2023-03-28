import streamlit as st
import openai

st.set_page_config(page_title="Experiment: AI Právní poradna")

st.write("""
# Ptejte se poradny Frank Bold
""")

title = st.text_input('Jaký máš dotaz?', placeholder='např. "Jak dosáhnout odstranění černé skládky?"')


temp = st.sidebar.slider('Míra kreativity v odpovědi', min_value=0.0, max_value=1.0, step=0.1)
typ = st.sidebar.selectbox("Jaký typ model použít?", ('gpt-3.5-turbo', 'gpt-4'))
