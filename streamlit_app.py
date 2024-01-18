import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

"""
# Infinite Number Calculator

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

num_points = st.text_input("First Number", placeholder="Enter a number")
num_points2 = st.text_input("Second Number", placeholder="Enter a number")

