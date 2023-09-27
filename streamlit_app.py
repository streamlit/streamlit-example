from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from io import StringIO
# import tensorflow as tf
import numpy as np

# """
# # Stress Intensity Factor Calculator (Proof of Concept)

# """


# Global variables and settings
model = None
record_num = 0
iframe_src_3d_url = "https://3dwarehouse.sketchup.com/embed/9658ccab-6ac3-4b89-a23f-635206942357"

st.set_page_config(layout="wide")


def load_model():
    global model
    model = tf.keras.models.load_model('models/NN_4_64_64_1/model.h5')
    a = np.array([[1, 1, 1, 1]])
    pred = model.predict(a)
    st.write('a shape:', a.shape)
    st.write('pred:', pred)


def KP(a, b, w, l0, l1, P):
    inputs = np.array([[a / b, w / b, l0 / b, l1 / b]])
    outputs = model.predict(inputs)
    kop = (outputs * l1 * (a ** 0.5) / b / w / w)
    return kop if np.isfinite(kop) else 0.0


def emp(a, b, w, L, P):
    F = 1.85 - 3.38 * (a / b) + 13.24 * (a / b) ** 2 - 23.26 * (a / b) ** 3 + 16.8 * (a / b) ** 4
    y = (b * b * w / 2 + w * w / 4 * (b + w / 6)) / (b * w + w * w / 4)
    I = w * b ** 3 / 12 + (y - b / 2) ** 2 * b * w + w ** 4 / 288 + (w / 6 + b - y) ** 2 * w * w / 4
    sigma = P * L * y / I
    return sigma * np.sqrt(np.pi * a) * F

def runUiSetUp():
    st.image("./public/web_title.png")
    st.markdown("""
    <style>
            .block-container {
                margin-top: -2rem;
                
            }
    </style>
    """, unsafe_allow_html=True)


# add sideBar
with st.sidebar:
    runUiSetUp()


    # st.write("**Stress Intensity Factor Calculator (PoC)**")

    a = st.number_input("a (μm)", help="a; unit: μm", key="a")
    b = st.number_input("b (μm)", help="b; unit: μm", key="b")
    w = st.number_input("w (μm)", help="w; unit: μm", key="w")
    LZero = st.number_input("L0 (μm)", help="L0; unit: μm", key="l_zero")
    LOne = st.number_input("L1 (μm)", help="L1; unit: μm", key="l_one")
    P = st.number_input("P (mN)", help="P; unit: mN", key="p")

    uploaded_file = st.file_uploader("Upload your model here", key="user_custom_model", type = "json")
    if uploaded_file is not None:
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        st.write(string_data)

        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_json(uploaded_file)
        st.write(dataframe.to_json())

        # TODO: Check parsing json and apply model equation



st.write("(PoC) Assuming model equation is: a + b + w + LZero + LOne + P. Result is: " )
st.write(str(a + b + w + LZero + LOne + P))


col1, col2 = st.columns(2, gap="medium")
with col1:
   st.image("https://hint1412.github.io/XLiu.github.io/SIF/images/Notched_cantilever_sketch.png")

with col2:
   with st.container():
    st.components.v1.iframe(iframe_src_3d_url, scrolling=False)


# st.components.v1.iframe(iframe_src_3d_url, width=800, height = 600, scrolling=False)
# st.components.v1.html(image_html_block, width=800, height=600, scrolling=False)


