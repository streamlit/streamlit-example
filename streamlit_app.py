# Originaly forked from the streamlit example app

from collections import namedtuple
import time
import altair as alt
import math
import pandas as pd
import numpy as np
import streamlit as st
import random as rand
import matplotlib.pyplot as plt


# COMPONENTS USED
# Write and magic
#  st.write()
#  magic
# Text elements
#  st.header()
#  st.subheader()
#  st.latex()
# Data display elements
#  st.metric()
#  st.dataframe()
# Chart elements
#  st.line_chart()
#  st.pyplot()
# Input widgets
#  st.button()
#  st.slider()
#  st.number_input()
# Media elements
#  st.image()
#  st.audio()
# Layouts and containers
#  st.expander()
#  st.container()
#  st.empty()
# Status elements
#  st.spinner()
#  st.balloons()

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
temp_button = st.button("Get temperature", on_click=get_temp())
"Just joking, it is only a random number generator between 25 and 35..."

st.header("Now let's do some finance stuff")
st.write("How will our portfolio perform over time?")
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


st.header("Don't mind these random numbers...")
df = pd.DataFrame(np.random.randint(0, 100, size=(30, 4)), columns=list("ABCD"))
# obtained from https://stackoverflow.com/questions/32752292/how-to-create-a-dataframe-of-random-integers-with-pandas
c1, c2 = st.columns(2)
c1.dataframe(df)
fig, ax = plt.subplots()
ax.plot(df)
c2.pyplot(fig)


cat_supercontainer = st.empty()
if cat_supercontainer.button(
    "Congratulations on getting this far", help="Do you want a cat?"
):
    with st.spinner("Thank you for your patience..."):
        time.sleep(1.5)
        cat_container = cat_supercontainer.container()
        cat_container.image("./media/cat.png")
        cat_container.audio(
            f"https://assets.mixkit.co/sfx/preview/mixkit-sweet-kitty-meow-93.mp3"
        )
        cat_container.balloons()
