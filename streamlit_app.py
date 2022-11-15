# Core Packages
import streamlit as st
import altair as alt
# Decoration
primaryColor="#2214c7"
backgroundColor="#ffffff"
secondaryBackgroundColor="#e8eef9"
textColor="#000000"
font="sans serif"

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
    
st.set_page_config(page_title="Movie Reviewer", layout="wide")
#st.write([![Follow](<https://img.shields.io/twitter/follow/><Cody_coder017>?style=social)](<https://www.twitter.com/><Cody_coder017>))

# Main Application
def main():
    st.title("😉 DR Soumyendra  & Team One's Movie Review classifier App 😉")
    with st.form(key="emotion_clf_form"):
        raw_text1 = st.text_area(" Your latest movie name")
        raw_text = st.text_area("Feed your review here for your latest movie")
        submit_text = st.form_submit_button(label="Submit")
        

    if submit_text:
            # Apply the linkage function here
            col1= st.columns(1)
            results = pipeline.predict([raw_text])
            st.write("{}".format(results))
            from PIL import Image
            image = Image.open('THANKYOU.jpeg')
            st.image(image, caption='tHANK YOU FOR REVIEW !!')
            
        

if __name__ == "__main__":
    main()
