import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import datetime as dt

# Set page title
st.set_page_config(
    page_title="France Road Accident Data Analysis - Visualization",
    layout='wide'
)

st.markdown(f'<b><h0 style="color:#00008B;font-size:35px;">{"Data Visualizations:"}</h0><br>', unsafe_allow_html=True)

# Content of the page
option = st.selectbox(
    'Choose a data visualization:',
    ('Accident severity over years', 'Accidents reported over years', 'Accidents happened in day of week',
     'Impact of lighting on road accidents', 'Impact of atmospheric conditions on road accidents',
    'Impact of road category on accidents','Impact of intersection type on accidents','Impact of accident time on severity',
    'Impact of area zone on severity','Impact of collision type on severity','Impact of surface condition on severity',
    'Impact of accident situation on severity'))

st.markdown(f'<br>', unsafe_allow_html=True)
if option == 'Accident severity over years':
    # List down the observations
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;"><b>{"Observations:"}</b></p>', unsafe_allow_html=True)
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"- Death rate in accidents is slightly getting reduced over years."}</p>', unsafe_allow_html=True)
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"- Number of accidents also show a reducing trend over years."}</p>', unsafe_allow_html=True)
    st.image('visualizations/Accident Severity over years.png')
elif option == 'Accidents reported over years':
    # List down the observations
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;"><b>{"Observations:"}</b></p>', unsafe_allow_html=True)
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"- The number of accidents reported show a downward trend over years."}</p>', unsafe_allow_html=True)
    st.image('visualizations/Accident reported over years.png')
elif option == 'Accidents happened in day of week':
    # List down the observations
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;"><b>{"Observations:"}</b></p>', unsafe_allow_html=True)
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"- Friday is more prone to accidents while Sunday is the day with least number of accidents."}</p>', unsafe_allow_html=True)
    st.image('visualizations/Accident happened in day of week - Copy.png')
elif option == 'Impact of lighting on road accidents':
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;"><b>{"Observations:"}</b></p>', unsafe_allow_html=True)
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"- Lighting does not have an impact on the number of accidents as most of the accidents happened during day time."}</p>', unsafe_allow_html=True)
    st.image('visualizations/Impact of lighting on accidents.png')
elif option == 'Impact of atmospheric conditions on road accidents':
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;"><b>{"Observations:"}</b></p>', unsafe_allow_html=True)
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"- Could not see much impact of atmospheric condition on accidents, as most of the accidents happened during normal atmospheric condition."}</p>', unsafe_allow_html=True)
    st.image('visualizations/Impact of atmospheric condition on accidents.png')
elif option == 'Impact of road category on accidents':
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;"><b>{"Observations:"}</b></p>', unsafe_allow_html=True)
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"- Communal Roads are more prone to accidents and then comes the Departmental Roads."}</p>', unsafe_allow_html=True)
    st.image('visualizations/Impact of road category on accidents.png')    
elif option == 'Impact of intersection type on accidents':
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;"><b>{"Observations:"}</b></p>', unsafe_allow_html=True)
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"- Among the intersection types Out of the intersection, X-intersection and T-junction are more prone to accidents."}</p>', unsafe_allow_html=True)
    st.image('visualizations/Impact of intersection type on accidents.png')   
elif option == 'Impact of accident time on severity':
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;"><b>{"Observations:"}</b></p>', unsafe_allow_html=True)
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"- It looks like 16:00 PM till 20:00 PM is the most accident prone time."}</p>', unsafe_allow_html=True)
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"- Also morning till 7:00 AM , the number of accidents are very less."}</p>', unsafe_allow_html=True)
    st.image('visualizations/Impact of accident time severity.png')
elif option == 'Impact of area zone on severity':
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;"><b>{"Observations:"}</b></p>', unsafe_allow_html=True)
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"- It looks areazone In built up areas is more prone to accidents."}</p>', unsafe_allow_html=True)
    st.image('visualizations/Impact of areazone on severity.png')
elif option == 'Impact of collision type on severity':
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;"><b>{"Observations:"}</b></p>', unsafe_allow_html=True)
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"- Other collsion type has the most fatality."}</p>', unsafe_allow_html=True)
    st.image('visualizations/Impact of collission type on severity.png')
elif option == 'Impact of surface condition on severity':
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;"><b>{"Observations:"}</b></p>', unsafe_allow_html=True)
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"- Most of the accidents happened in normal surface condition."}</p>', unsafe_allow_html=True)
    st.image('visualizations/Impact of surface condition on severity.png')
elif option == 'Impact of accident situation on severity':
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;"><b>{"Observations:"}</b></p>', unsafe_allow_html=True)
    st.markdown(f'<p align="justify" font-family: "Times New Roman" style="color:#000000;">{"- Most of the accidents happened in road."}</p>', unsafe_allow_html=True)
    st.image('visualizations/Impact of accident situation on severity.png')

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










