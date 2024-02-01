import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

"""
# Heart Disease Risk Prediction

## Fill out the Following Questions:
"""

st.write("Personal Detail Question")
username = st.text_input("Enter your name")
sex = st.radio("Select Gender:", ("Male", "Female"))
age = st.selectbox("Select Age Group:", ["Select One", "18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54",
                                        "55-59", "60-64", "65-69", "70-74", "75-79", "80 or older"])
race = ("Select Race:", ["Select One", "White", "Hispanic", "Black", "Asian", "American Indian/Alaskan Native"])
height_unit = st.selectbox("Select Height Unit:", ["Centimeters", "Feet and Inches"])

if height_unit == "Centimeters":
  cm_height = st.number_input("Enter your Height (in centimeters):", min_value=100, max_value=250, step=10)
else:
  feet_height = st.selectbox("Select Feet:", range(3, 8))
  inch_height = st.selectbox("Select Inches", range(0, 12))

weight = st.number_input("Enter your Weight (in kilograms):", min_value=30.00, max_value=200.00, step=10.00)


st.write("Daily Activity Question")
sleep = st.number_input("Enter Average Sleep Time:", min_value=0.0, max_value=24.0, step=1.0)
activity = st.radio("During the past month, other than your regular job, did you participate in any physical activities or exercises such as running, calisthenics, golf, gardening, or walking for exercise?:", ("Yes", "No"))
smoking = st.radio("Have you smoked at least 100 cigarettes in your entire life?:", ("Yes", "No"))
drinking = st.radio("Do you drink a lot (adult men having more than 14 drinks per week or adult women having more than 7 drinks per week)?:", ("Yes", "No"))

st.write("Health Status")
genhealth = st.selectbox("Would you say that in general your health is:", ['Excellent', 'Very good', 'Good', 'Fair', 'Poor'])
physicalhealth = st.selectbox("During the past month, how many days did you have physical health problem, which includes physical illness and injury?:", range(0, 31))
mentalhealth = st.selectbox("During the past month, how many days did you have mental health problem?:", range(0, 31))
diffwalking = st.radio("Do you have serious difficulty walking or climbing stairs?:", ("Yes", "No"))
asthma = st.radio("(Ever told) (you had) asthma?:", ("Yes", "No"))

"""


Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
