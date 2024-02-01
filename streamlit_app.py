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
  feet_height = st.selectbox("Select Feet:", range(3, 8))
  inch_height = st.selectbox("Select Inches", range(0, 12))

weight = st.number_input("Enter Weight (in kg):", min_value=30.00, max_value=150.00)


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
