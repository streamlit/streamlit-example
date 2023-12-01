import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

import streamlit as st

# Function to create the sidebar
def create_sidebar():
    st.sidebar.image("path_to_your_logo.png", use_column_width=True)
    st.sidebar.write("## Navigation")
    st.sidebar.button("Usage")
    st.sidebar.button("Users")

# Function to create the top menu bar
def create_top_menu():
    st.button("Sign In/Sign Out")

# Main page layout
def main():
    create_top_menu()
    create_sidebar()

    st.title("Backoffice Homepage")
    st.write("Welcome to the Backoffice Dashboard.")

if __name__ == "__main__":
    main()
