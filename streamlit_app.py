import spacy
import streamlit as st
nlp = spacy.load("en_core_web_sm")

def return_NER(value):
    doc = nlp(value)
    return [(X.text, X.label_) for X in doc.ents]

# Add title on the page
st.title("Spacy - Named Entity Recognition")

# Ask user for input text
input_sent = st.text_input("Input Sentence", "Your input sentence goes here")

# Display named entities
for res in return_NER(input_sent):
    st.write(res[0], "-->", res[1])
