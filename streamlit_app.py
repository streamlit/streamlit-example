from collections import namedtuple
import altair as alt
import math
import numpy as np
import pandas as pd
import streamlit as st
import time
import streamlit.components.v1 as components
st.set_page_config(
    page_title="Cool App",
    page_icon=":shark:",
    layout="wide"
    )
# 1st way of setting title style   
st.markdown("<h1 style='text-align: center; \
                        color: red;'>Some title\
            </h1>", unsafe_allow_html=True)

# 2nd way of setting title style
title_alignment= \
"""
<style>
#the-title {
  text-align: center
}
</style>
"""
st.markdown(title_alignment, unsafe_allow_html=True)
st.title("The title")
"""
# Welcome to Streamlit! """
@st.cache
def read_csv():
    df = pd.read_csv('test_1.csv')
    return df
df = read_csv()
# sidebar
sidebar_1 = st.sidebar
sidebar_1.header('hello')

column = sidebar_1.multiselect(
    "Column",
    options=df.columns
)
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
#   return df.boxplot(column = list(df.select_dtypes(include=numerics).columns.values),figsize=(fig_w,fig_h))
row = sidebar_1.multiselect(
    "Row",
    options=df.columns
)
value_col = sidebar_1.multiselect(
    "Value",
    options=df.select_dtypes(include=numerics).columns
)
value = sidebar_1.selectbox(
    "Operation",
    ("Sum", "Count", "Distinct","Mean")
)
if value == 'Sum':
    arg_ = np.sum
elif value == 'Count':
    arg_ = 'count'
elif value == 'Distinct':
    arg_ =  pd.Series.nunique
elif value == 'Mean':
    arg_ =  np.mean

df_query = table = pd.pivot_table(df, values=value_col, index=column,
                    columns=row, aggfunc=arg_)

    
# container
container_1 = st.container()

with container_1:
    st.dataframe(df)
    st.title("Pivot table")
    if column and value_col:
        st.dataframe(df_query)
    else:
        e = RuntimeError('Must select - Column, value in sidebar')
        st.exception(e)
    col1, col2, col3 = st.columns(3,gap="medium")
    total_points = col1.slider("Number of points in spiral", 1, 5000, 2000,help='hii')
    num_turns = col2.slider("Number of turns in spiral", 1, 100, 9)

    st.info('This is a purely informational message', icon="ℹ️")
    st.success('This is a success message!', icon="✅")
    e = RuntimeError('This is an exception of type RuntimeError')
    st.exception(e)

    with col3.form("my_form"):
        slider_val = st.slider("Form slider")
        checkbox_val = st.checkbox("Form checkbox")
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("slider", slider_val, "checkbox", checkbox_val)
