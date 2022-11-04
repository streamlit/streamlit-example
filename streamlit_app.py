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
    
logo_url=https://www.google.com/url?sa=i&url=https%3A%2F%2Fsites.umiacs.umd.edu%2Felm%2F2016%2F02%2F01%2Fmistakes-reviewers-make%2F&psig=AOvVaw0mE0u66b1sQ6gBtNUYPN-X&ust=1667634411456000&source=images&cd=vfe&ved=0CA0QjRxqFwoTCICfiLeElPsCFQAAAAAdAAAAABAE
st.image(logo_url, width=100)
st.set_page_config(layout="wide")

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
