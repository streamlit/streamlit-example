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
height = st.number_input("Enter your Height (in centimeters):", min_value=100, max_value=250, step=10)
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

bmi = weight / height**2


### Creating a Machine Learning Model ###
pip install scikit-learn
from sklearn.feature_selection import RFE
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

over_sampled_df = pd.read_csv("./over_sampled_df_fe.csv")
test_sampled_df = pd.read_csv("./test_sampled_df_fe.csv")

scaler = StandardScaler()
scaler.fit(X_train_over)
X_scaled_train = scaler.transform(X_train_over)
X_scaled_test = scaler.transform(X_test_sampled)
   
rfe_over = RFE(estimator=LogisticRegression(max_iter=1000, random_state=42), n_features_to_select=11)
rfe_over.fit(X_scaled_train,y_train_over)
    
scaler = StandardScaler()
scaler.fit(X_train_over.loc[:, rfe_over.support_])
X_scaled_train = scaler.transform(X_train_over.loc[:, rfe_over.support_])
X_scaled_test = scaler.transform(X_test_sampled.loc[:, rfe_over.support_])
    
my_PCA = PCA()
my_PCA.fit(X_scaled_train)

X_train_PCA = my_PCA.transform(X_scaled_train)
X_test_PCA = my_PCA.transform(X_scaled_test)
    
cap_model = LogisticRegression(max_iter=1000, C=0.0001, penalty="l2", solver="liblinear", random_state=42)
cap_model.fit(X_train_PCA,y_train_over)




"""


Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
