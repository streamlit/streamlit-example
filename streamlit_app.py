import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

"""
# Heart Disease Risk Prediction

## Fill out the Following Questions:
"""

st.title("Personal Detail Question")
username = st.text_input("Enter your name")
sex = st.radio("Select Gender:", ("Male", "Female"))
age = st.selectbox("Select Age Group:", ["Select One", "18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54",
                                        "55-59", "60-64", "65-69", "70-74", "75-79", "80 or older"])
race = ("Select Race:", ["Select One", "White", "Hispanic", "Black", "Asian", "American Indian/Alaskan Native"])
height_unit = st.selectbox("Select Height Unit:", ["Centimeters", "Feet and Inches"])

if height_unit == "Centimeters":
  cm_height = st.slider("Select Height (in centimeters):", min_value=100, max_value=250)
else:
  feet_height = st.selectbox("Select Feet:", range(3, 8), placeholder="Feet")
  inch_height = st.selectbox("Select Inches", range(0, 12), placeholder="Inches")

weight = st.slider("Select Weight (in centimeters):", min_value=100, max_value=250)
if 'weight' not in st.session_state:
    st.session_state.weight = 70.0

# Create buttons for adjusting weight
if st.button('-'):
    st.session_state.weight = max(30.0, st.session_state.weight - 0.01)
if st.button('+'):
    st.session_state.weight = min(150.0, st.session_state.weight + 0.01)

# Display the adjusted weight
st.success(f"Adjusted Weight: {st.session_state.weight:.2f} kg")


"""
sleep = 
activity = 
smoking = 
drinking =

genhealth = 
physicalhealth =
mentalhealth =
diffwalking = 
asthma = 




Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
