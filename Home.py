### This is the main page of the web app .
import streamlit as st

# Set page title
st.set_page_config(
    page_title="France Road Accident Data Analysis",
    layout='wide'
)

# Content of the page
st.markdown(f'<b><h0 style="color:#ffffff;font-size:35px;">{"France Road Accidents Data Analysis & Severity Prediction !"}</h0><br><br>', unsafe_allow_html=True)
st.markdown(f'<b><h1 style="color:#ffffff;font-size:25px;">{"In this project it is aimed to analyse the road accidents data in France from 2005 till 2016. The input data contains lot of information about the  accident, users and involved vehicles. The aim would be to predict the severity of the accident - whether the injured person is Slightly Injured/Not injured at all Vs Heavily Injured/Died."}</h1><br><br>', unsafe_allow_html=True)

# To set the background image of the page
st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
