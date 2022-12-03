import pandas as pd
import streamlit as st
import os

from qa import get_answer_from_openai, Table

# Upload the file using the file_uploader function
uploaded_file = st.file_uploader("Upload your a csv file", type="csv")

# Show a dropdown to select a set of CSV files.
# The files are stored in the data folder.
# The user should also be able to upload a new file.
# The user should be able to select a table from the uploaded file.
# The first open should be empty file.

csv_files = os.listdir("data")
csv_files.insert(0, "Select from the list here")
selected_csv_file = st.selectbox("Select a CSV file", csv_files)

if selected_csv_file == "Upload your own file":
    selected_csv_file = uploaded_file

df = None

if selected_csv_file != "Select from the list here":
    df = pd.read_csv("data/" + selected_csv_file)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

if df is not None:
    # Display only the first 5 rows of the DataFrame
    st.write(df.head())

    # Extract the first line as a list of column names
    column_names = df.columns.tolist()

    # Show a text input to ask the user a question
    question = st.text_input("Ask a question about the data", "")

    # Translate the column names to a single table
    table = Table('table', column_names)

    tables = [table]

    # Make a call to OpenAI's API to get the answer to the question.
    # The answer is a string
    # Detect if the user has pressed enter on th text box.
    # If the user has pressed enter, then call the OpenAI API.
    # If the user has not pressed enter, then do not call the OpenAI API.
    if st.button("Get Answer"):
        answer = get_answer_from_openai(question, tables)
        st.write(answer)
