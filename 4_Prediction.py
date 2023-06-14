
### This is the prediction subpage of streamlit webapp
import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost import XGBClassifier

# Set page title
st.set_page_config(
    page_title="France Road Accident Data Analysis - Prediction",
    layout='wide'
)

st.markdown(f'<b><h0 style="color:#00008B;font-size:35px;">{"Prediction:"}</h0><br><br>', unsafe_allow_html=True)

# Content of the page
areaZone = st.number_input("Area Zone")
collisionType = st.number_input("Collision Type")
municipality = st.number_input("Municipality")
roadCategory = st.number_input("Road Category")
trafficRegime = st.number_input("Traffic Regime")
nrOfTrafficLanes = st.number_input("Number Of Traffic Lanes")
accidentSituation = st.number_input("Accident Situation")
struckWithFixedObject = st.number_input("Struck With Fixed Object")
struckWithMovingObject = st.number_input("Struck With MovingObject")
initialShockPoint = st.number_input("Initial Shock Point")
intersectionType = st.number_input("Intersection Type")

    
#Loading up the XGBoost model we created

xgb_cl = xgb.XGBClassifier()
xgb_cl.load_model('Models/xgb_model.json')


if st.button('Predict Accident Severity'):
    prediction = xgb_cl.predict(pd.DataFrame([[areaZone, collisionType, municipality, roadCategory, trafficRegime, nrOfTrafficLanes, accidentSituation, struckWithFixedObject, struckWithMovingObject, initialShockPoint, intersectionType ]], columns=[areaZone, collisionType, municipality, roadCategory, trafficRegime, nrOfTrafficLanes, accidentSituation, struckWithFixedObject, struckWithMovingObject, initialShockPoint, intersectionType]))
    st.write('Predict Accident Severity clicked : ', prediction) 
else:
    st.write('Predict Accident Severity not clicked') 
   
# To set the background image of the page
st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://img.freepik.com/free-photo/abstract-luxury-gradient-blue-background-smooth-dark-blue-with-black-vignette-studio-banner_1258-63452.jpg?size=626&ext=jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
