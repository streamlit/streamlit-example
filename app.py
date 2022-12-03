from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
### Upload your file and ask a question on the file.


"""
import streamlit as st

# Upload the file using the file_uploader function
uploaded_file = st.file_uploader("Upload your a csv file", type="csv")

# Check if a file was uploaded
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # Parse the CSV file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)
    st.write(df)

    # Extract the first line as a list of column names
    column_names = df.columns.tolist()
    st.write(column_names)






