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
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump, load

# Utils
import joblib

# Load the dataset
df = pd.read_csv("movie_reviews.csv")

# Define the pipeline
pipeline = Pipeline([
    ('vectorizer', CountVectorizer(stop_words='english')),
    ('clf', LogisticRegression())
])

# Define the hyperparameters for the grid search
parameters = {
    'vectorizer__max_df': [0.5, 0.75, 1.0],
    'vectorizer__ngram_range': [(1, 1), (1, 2)],
    'clf__C': [0.1, 1, 10]
}

# Perform the grid search
grid_search = GridSearchCV(pipeline, parameters, cv=5, n_jobs=-1)
grid_search.fit(df['text'], df['sentiment'])

# Save the best model
dump(grid_search.best_estimator_, "model.pkl")

# Load the model
model = load("model.pkl")

# Function to classify movie reviews
def classify_review(review):
    prediction = model.predict([review])
    return prediction[0]

# Function to connect with our ML model
def get_prediction(review):
    prediction = classify_review(review)
    return prediction

# Main Application
def main():
    st.set_page_config(page_title="Movie Reviewer", layout="wide")
    st.title("😉 Movie Review classifier App 😉")

    # User input
    with st.form(key="emotion_clf_form"):
        movie_name = st.text_input("Enter the name of the movie", "")
        review = st.text_area("Enter your review here", "")
        submitted = st.form_submit_button("Submit")

    # Display the result
    if submitted:
        prediction = get_prediction(review)
        st.write(f"The predicted sentiment for the movie review of {movie_name} is {prediction}")
        image = Image.open('THANKYOU.jpeg')
        st.image(image, caption='THANK YOU FOR YOUR REVIEW !!')

if __name__ == "__main__":
    main()
