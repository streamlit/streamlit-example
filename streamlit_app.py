from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

age_param = st.number_input("Please enter your age", min_value=1, max_value=None)
st.text(age_param)
