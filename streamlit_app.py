# Core Packages
import streamlit as st
import altair as alt

# Exploratory data analysis Packages
import pandas as pd
import numpy as np
from datetime import datetime

# Utils
import joblib

pipeline = joblib.load(
    open("model/model.pkl", "rb")
)
# Function to connect with our ML model
def predict_emotions(docx):
    results = pipeline.predict([docx])
    return results[0]


def get_prediction_proba(docx):
    results = pipeline.predict_proba([docx])
    return results


emotions_emoji_dict = {
    "anger": "😠",
    "disgust": "🤮",
    "fear": "😨😱",
    "happy": "🤗",
    "joy": "😂",
    "neutral": "😐",
    "sad": "😔",
    "sadness": "😔",
    "shame": "😳",
    "surprise": "😮",
}

# Main Application
def main():
    st.title("Emotion Classifier App")
    menu = ["Home"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        ("Home", datetime.now())
        st.subheader("Emotion In Text")

        with st.form(key="emotion_clf_form"):
            raw_text = st.text_area("Type Here")
            submit_text = st.form_submit_button(label="Submit")

        if submit_text:
            col1, col2 = st.columns(2)

            # Apply the linkage function here
            prediction = predict_emotions(raw_text)
            probability = get_prediction_proba(raw_text)

            with col1:
                st.success("Original Text")
                st.write(raw_text)

                st.success("Prediction")
                emoji_icon = emotions_emoji_dict[prediction]
                st.write("{}:{}".format(prediction, emoji_icon))
                st.write("Confidence:{}".format(np.max(probability)))

            with col2:
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
