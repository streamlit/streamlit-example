
import streamlit as st

"""
# Open Ai Based ChatBot

"""
st.write("Please type a question regarding the vision pro headset!!")
st.text_input("Question", key="question")
question = st.session_state.question
print(question)