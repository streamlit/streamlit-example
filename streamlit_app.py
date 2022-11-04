# Core Packages
import streamlit as st
import altair as alt

# Exploratory data analysis Packages
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
vec = CountVectorizer(stop_words='english')
# Utils
import joblib

pipeline = joblib.load(
    open("model/model1.pkl", "rb")
)
# Function to connect with our ML model
    

st.set_page_config(layout="wide")
st.write("[![Star](<https://img.shields.io/github/stars/><username>/<repo>.svg?logo=github&style=social)](<https://gitHub.com/Venkatakrishnan-Ramesh/)")

# Main Application
def main():
    st.title("Movie Review classifier App")
    with st.form(key="emotion_clf_form"):
        raw_text = st.text_area("Type Here")
        submit_text = st.form_submit_button(label="Submit")
        

    if submit_text:
            # Apply the linkage function here
            col1= st.columns(1)
            results = pipeline.predict([raw_text])
            st.write("{}".format(results))
            
        

if __name__ == "__main__":
    main()
