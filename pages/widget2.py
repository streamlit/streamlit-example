import streamlit as st
st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name