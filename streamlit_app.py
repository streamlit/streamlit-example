import streamlit as st
from transformers import pipeline

# Load the text-to-speech pipeline
tts_pipeline = pipeline("text-to-speech", model="your_chosen_model_name")

# Text input field
text_input = st.text_input("Enter text to be spoken:")

# Generate audio and play it
if text_input:
    audio = tts_pipeline(text_input)
    st.audio(audio)
