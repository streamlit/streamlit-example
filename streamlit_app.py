import streamlit as st
import time

with st.button('Click me!!!'):
    with st.spinner('Wait for it...'):
        time.sleep(5)
    st.write("I love you Paulita, mi amor de mi corazon!!!")
    st.success('This is a success message!', icon="🥰")
