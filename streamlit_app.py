import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


st.title("Welcome to Heart Disease Risk Prediction!!")

st.header("Fill out the Following Questions:")

st.write("Personal Detail Question")
username = st.text_input("Enter your name")
sex = st.radio("Select Gender:", ("Male", "Female"))
age = st.selectbox("Select Age Group:", 
                   ["18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54",
                    "55-59", "60-64", "65-69", "70-74", "75-79", "80 or older"],
                    placeholder="Select One")
race = st.selectbox("Select Race:", ["White", "Hispanic", "Black", "Asian", "American Indian/Alaskan Native"],
                    placeholder="Select One")
height = st.number_input("Enter your Height (in centimeters):", min_value=100.00, max_value=250.00, 
                         value=150.00, step=5.00)
weight = st.number_input("Enter your Weight (in kilograms):", min_value=30.00, max_value=200.00, 
                         value=50.00, step=5.00)


st.text(" ")
st.text(" ")
st.write("Daily Activity Question")
sleep = st.number_input("Enter Average Sleep Time:", min_value=0.0, max_value=24.0, 
                        value=7.0, step=0.5)
activity = st.radio("During the past month, other than your regular job, did you participate in any physical activities or exercises such as running, calisthenics, golf, gardening, or walking for exercise?:", 
                    ("Yes", "No"), index=1)
smoking = st.radio("Have you smoked at least 100 cigarettes in your entire life?:", 
                   ("Yes", "No"), index=1)
drinking = st.radio("Do you drink a lot (adult men having more than 14 drinks per week or adult women having more than 7 drinks per week)?:", 
                    ("Yes", "No"), index=1)


st.text(" ")
st.text(" ")
st.write("Health Status")
genhealth = st.selectbox("Would you say that in general your health is:", ['Excellent', 'Very good', 'Good', 'Fair', 'Poor'],
                         index=2)
physicalhealth = st.selectbox("During the past month, how many days did you have physical health problem, which includes physical illness and injury?:", range(0, 31))
mentalhealth = st.selectbox("During the past month, how many days did you have mental health problem?:", range(0, 31))
diffwalking = st.radio("Do you have serious difficulty walking or climbing stairs?:", 
                       ("Yes", "No"), index=1)
asthma = st.radio("(Ever told) (you had) asthma?:", ("Yes", "No"), index=1)

st.text(" ")
st.text(" ")
button = st.button('Predict')

bmi = weight / ((height/100)**2)




# Creating a Machine Learning Model 

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

over_sampled_df = pd.read_csv("./over_sampled_df_fe.csv")
test_sampled_df = pd.read_csv("./test_sampled_df_fe.csv")

X_train_over = over_sampled_df.drop(columns="HeartDisease")
y_train_over = over_sampled_df["HeartDisease"]

X_test_sampled = test_sampled_df.drop(columns="HeartDisease")
y_test_sampled = test_sampled_df["HeartDisease"]

scaler = StandardScaler()
scaler.fit(X_train_over)
X_scaled_train = scaler.transform(X_train_over)
X_scaled_test = scaler.transform(X_test_sampled)
   
rfe_over = RFE(estimator=LogisticRegression(max_iter=1000, random_state=42), n_features_to_select=11)
rfe_over.fit(X_scaled_train,y_train_over)
import joblib
joblib.dump(rfe_over, "cap_rfe.sav")
    
scaler = StandardScaler()
scaler.fit(X_train_over.loc[:, rfe_over.support_])
X_scaled_train = scaler.transform(X_train_over.loc[:, rfe_over.support_])
X_scaled_test = scaler.transform(X_test_sampled.loc[:, rfe_over.support_])
import joblib
joblib.dump(scaler, "cap_scaler.sav")

my_PCA = PCA()
my_PCA.fit(X_scaled_train)
X_train_PCA = my_PCA.transform(X_scaled_train)
X_test_PCA = my_PCA.transform(X_scaled_test)
import joblib
joblib.dump(my_PCA, "cap_pca.sav")
    
cap_model = LogisticRegression(max_iter=1000, C=0.0001, penalty="l2", solver="liblinear", random_state=42)
cap_model.fit(X_train_PCA,y_train_over)
import joblib
joblib.dump(cap_model, "cap_model.sav")


#from prediction import predict
def predict(df):
    scaler = joblib.load("cap_scaler.sav")
    rfe_over = joblib.load("cap_rfe.sav")
    my_PCA = joblib.load("cap_pca.sav")
    cap_model = joblib.load("cap_model.sav")

    yes_no_columns = ["Smoking", "AlcoholDrinking", "DiffWalking", "PhysicalActivity", "Asthma"]

    for column in yes_no_columns:
        df[column] = df[column].map({"No":0, "Yes":1})

    df["Sex"] = df["Sex"].replace({"Male":1, "Female":0})

    df["AgeCategory"] = df["AgeCategory"].replace({'55-59':55, '80 or older':80, '65-69':65, '75-79':75,
                                                        '40-44':40, '70-74':70,'60-64':60, '50-54':50, '45-49':45,
                                                        '18-24':18, '35-39':35, '30-34':30, '25-29':25})
    
    df["GenHealth"] = df["GenHealth"].replace({'Very good':3, 'Fair':1, 'Good':2, 'Poor':0, 'Excellent':4})
    
   
    race_column = ["Race_American Indian/Alaskan Native", "Race_Asian", "Race_Black", "Race_Hispanic", "Race_Other", "Race_White"]
    df[race_column] = 0
    race_list = ["American Indian/Alaskan Native", "Asian", "Black", "Hispanic", "Other", "White"]
    for index in range(len(race_list)):
        if df.loc[0, "Race"] == race_list[index]:
            df[race_column[index]] = 1
    cap_df = df.drop(columns="Race")


    scaled_df = scaler.transform(cap_df.loc[:, rfe_over.support_])

    pca_df = my_PCA.transform(scaled_df)

    cap_proba = cap_model.predict_proba(pca_df)
    cap_pred = (cap_proba[:, 1] >= 0.52).astype(int)

    #import joblib
    joblib.dump(cap_proba, "cap_proba.sav")

    if cap_pred == 1:
        #result_high='<p style="color:Red; font-size: 25px;">HIGH</p>'
        st.markdown(f"Based from the Machine Learning model,")
        st.markdown(f"your risk of developing Heart Disease is:")
        #st.markdown(result_high, unsafe_allow_html=True)

        st.error('HIGH')

        
    else:
        st.balloons()
        #result_low='<p style="color:Blue; font-size: 25px;">LOW</p>'
        st.markdown(f"Based from the Machine Learning model, your risk of developing Heart Disease is:")
        #st.markdown(result_low, unsafe_allow_html=True)

        st.warning('LOW')

        
data = [bmi, smoking, drinking, physicalhealth, mentalhealth, diffwalking, sex, age, race, activity, genhealth, sleep, asthma]
user_df = pd.DataFrame(data, index = ["BMI", "Smoking", "AlcoholDrinking", "PhysicalHealth", "MentalHealth", "DiffWalking", "Sex", "AgeCategory", "Race", "PhysicalActivity", "GenHealth", "SleepTime", "Asthma"])
user_df = user_df.T


if button:
    st.text(f"Hi {username}!")
    predict(user_df)

    st.text(" ")
    st.text(" ")
    cap_proba = joblib.load("cap_proba.sav")
    st.markdown(f"According to the machine learning model:")
    st.success(f"The Probability that it will classify you as at risk for heart disease are:   {int(cap_proba[:, 1]*100)}%, the Probability that it will classify you as at no risk for heart disease are:   {int(cap_proba[:, 0]*100)}%")
    st.text(" ")
    st.text(" ")
    st.markdown(f"Note: If the Probability it will classify you at risk is over 52%, then the model will classify you as at risk for heart disease")
