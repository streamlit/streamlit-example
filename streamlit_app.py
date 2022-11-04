from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
title = st.text_input('Enter sentiment', 'Life of Brian')
def detect_sentiment(self):

        # get a whole input content from text box
        sentence = self.entryMsg.get()

        # Create a SentimentIntensityAnalyzer object.
        obj = SentimentIntensityAnalyzer()

        dict1 = obj.polarity_scores(sentence)

        string = str(dict1['neg'] * 100) + "% Negative"
        self.negativeField.insert(10, string)

        string = str(dict1['neu'] * 100) + "% Neutral"
        self.neutralField.insert(10, string)

        string = str(dict1['pos'] * 100) + "% Positive"
        self.positiveField.insert(10, string)

        # decide sentiment as positive, negative and neutral
        if dict1['compound'] >= 0.05:
            string = "Positive"

        elif sentiment_dict['compound'] <= - 0.05:
            string = "Negative"


        else:
            string = "Neutral"

        self.overallField.insert(10, string)
        
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
