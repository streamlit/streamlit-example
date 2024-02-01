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
  feet_height = st.selectbox("Enter Height in Centimeters:", "Select One", range(3, 8))
  inch_height = st.selectbox("Enter Height in Centimeters:", range(0, 12))

st.title("Weight Tab")

    # Initialize weight
weight = 30.00

    # Layout
col1, col2, col3 = st.columns([1, 3, 1])

    # Button to decrease weight
if col1.button("-"):
    weight = max(30.00, weight - 1.00)

    # Display weight
col2.write(f"Weight: {weight:.2f} kg")

    # Button to increase weight
if col3.button("+"):
    weight = min(150.00, weight + 1.00)


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
