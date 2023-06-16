
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
agg = st.number_input("Area Zone")
catr = st.number_input("Category of road")
prof = st.number_input("Slope of the road")
com = st.number_input("Commune")
col = st.number_input("Type of collision")
larrout = st.number_input("widht of the road")
situ = st.number_input("situation of the accident")
dep = st.number_input("Department")
lartpc = st.number_input("Struck With MovingObject")
ints = st.number_input("Intersection")
lartpc = st.number_input("central solid land in meter")
circ = st.number_input("Trafic regime")
nbv = st.number_input("central solid land in meter")
atm = st.number_input("Atmospheric Condition")
year = st.number_input("year")
month = st.number_input("month")
day = st.number_input("day")
hrmm = st.number_input("hrmm")
dfpredict = pd.DataFrame([[agg, catr, prof, com, col, larrout, situ, dep, lartpc, ints, circ, nbv, atm, severity, year, month, day, hrmn]], columns=[agg, catr, prof, com, col, larrout, situ, dep, lartpc, int, circ, nbv, atm, severity, year, month, day, hrmn]))


def results(model):
    st.markdown('## Prediction')
    st.write(model.predict(X_test))

choices = ['XGBOOST','XGBOOST improved','Gradient Boosting','Gradient Boosting improved']
#choices = ['Gradient Boosting']
option = st.selectbox(
         'Which model do you want to try ?',
         choices)

st.write('You selected :', option)

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df



df = load_data('test_sample_15_06_2023.csv')

if dfpredict is not None:
    X_test = dfpredict

if option=='Gradient Boosting':
   st.write('Gradient Boosting score train 73.127 rmse train 0.518')
   GBC=joblib.load('GBC_model.joblib')
   results(GBC) 

if option=='Gradient Boosting improved':
   st.write('Gradient Boosting score train 78.535 rmse train 0.463')
   GBCi=joblib.load('GBC_improved_model.joblib')
   results(GBCi)


if option=='XGBOOST':
   st.write('XGBOOST score train 78.733 rmse train 0.461')
   xgb = joblib.load('xgb_model.joblib')
   results(xgb)


if option=='XGBOOST improved':
   st.write('XGBOOST score train 78.733 rmse train 0.461')
   xgbi = joblib.load('xgb_model.joblib')
   results(xgbi)

# #Loading up the XGBoost model we created

# xgb_cl = xgb.XGBClassifier()
# xgb_cl.load_model('xgb_model.json')


# if st.button('Predict Accident Severity'):
#     prediction = xgb_cl.predict(pd.DataFrame([[areaZone, collisionType, municipality, roadCategory, trafficRegime, nrOfTrafficLanes, accidentSituation, struckWithFixedObject, struckWithMovingObject, initialShockPoint, intersectionType ]], columns=[areaZone, collisionType, municipality, roadCategory, trafficRegime, nrOfTrafficLanes, accidentSituation, struckWithFixedObject, struckWithMovingObject, initialShockPoint, intersectionType]))
#     st.write('Predict Accident Severity clicked : ', prediction) 
# else:
#     st.write('Predict Accident Severity not clicked') 
   
# # To set the background image of the page
# st.markdown(
#          f"""
#          <style>
#          .stApp {{
#              background-image: url("https://img.freepik.com/free-photo/abstract-luxury-gradient-blue-background-smooth-dark-blue-with-black-vignette-studio-banner_1258-63452.jpg?size=626&ext=jpg");
#              background-attachment: fixed;
#              background-size: cover
#          }}
#          </style>
#          """,
#          unsafe_allow_html=True
#      )
