from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import random as rand


st.set_page_config("Demo app", ":heart:")


def get_stock(returns, std, start_price, n):
    prices = [start_price]
    for i in range(n):
        prices.append(prices[-1] * (1 + returns + std * (rand.random() - 0.5) * 2))
    return prices


def get_temp():
    if "old_temp" not in st.session_state:
        st.session_state["temp"] = round(30 + (rand.random() - 0.5) * 10)
        st.metric("Ithaca Temperature (ºF)", st.session_state["temp"])
        st.session_state["old_temp"] = st.session_state["temp"]
    else:
        st.session_state["temp"] = round(30 + (rand.random() - 0.5) * 10)
        st.metric(
            "Ithaca Temperature (ºF)",
            st.session_state["temp"],
            st.session_state["temp"] - st.session_state["old_temp"],
        )
        st.session_state["old_temp"] = st.session_state["temp"]


"""
# This is the first demo

We will use it to showcase some of streamlit functionalities
"""

st.header("Let's start with some math")
st.latex("e^{\pi i}+1=0")

st.header("What about today's weather?")
"Just joking, it is only a random number generator between 25 and 35..."
temp_button = st.button("Get temperature", on_click=get_temp())


st.header("Now let's do some finance stuff")
returns = 10
std = 0.5
initial_price = 1000
n = 50
with st.expander("Set the parameters"):
    returns = st.slider("Annual returns (%)", -30, 30, 0)
    std = st.slider("Standard deviation (%)", 0, 50, 0)
    initial_price = st.number_input("Initial price", step=1, value=1000)
    n = int(st.number_input("Number of periods", step=1, value=30))
    returns /= 100
    std /= 100
    prices = get_stock(returns, std, initial_price, n)
    st.subheader("Stock price evolution")
    st.line_chart(prices)
