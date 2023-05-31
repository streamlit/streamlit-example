import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import datetime as dt

from pathlib import Path
#DATA_URL = Path(Training/Datascientist/Coursera).parents[1] / 'Motor_Vehicle_Collisions_-_Crashes.csv'

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  DATA_URL = pd.read_csv(uploaded_file).sample(n=100000)


df = DATA_URL

st.title("Road Accident in France")
st.markdown("This application is a Streamlit dashboard that can be use to analyze road accident in France🗼🥐🇫🇷🥖🚗💥🚙")

from PIL import Image
st.image("https://upload.wikimedia.org/wikipedia/commons/2/2f/Multi_vehicle_accident_-_M4_Motorway%2C_Sydney%2C_NSW_%288076208846%29.jpg",
            width=600 # Manually Adjust the width of the image as per requirement


"""
# Welcome to YAKOUT TEAM!

Bonsoir nia mouah !!!!!

"""
#st.image('https://images.app.goo.gl/qwTsY83KPUPpWGWJA')

