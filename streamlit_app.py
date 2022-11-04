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
            st.write(results)
            st.success("Prediction Probability")
            # st.write(probability)
            proba_df = pd.DataFrame(probability, columns=pipeline.classes_)
            # st.write(proba_df.T)
            proba_df_clean = proba_df.T.reset_index()
            proba_df_clean.columns = ["emotions", "probability"]

            fig = (
                alt.Chart(proba_df_clean)
                .mark_bar()
                .encode(x="emotions", y="probability", color="emotions")
            )
            st.altair_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
