from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from io import StringIO

# """
# # Stress Intensity Factor Calculator (Proof of Concept)

# """

# add sideBar
with st.sidebar:
    st.write("**Stress Intensity Factor Calculator (PoC)**")

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


iframe_src_3d_url = "https://3dwarehouse.sketchup.com/embed/9658ccab-6ac3-4b89-a23f-635206942357"
image_html_block = "<div class=\"col-lg-6 card my-2 px-3\" style=\"width: max-content;\"> <img src=\"https://hint1412.github.io/XLiu.github.io/SIF/images/Notched_cantilever_sketch.png\" class=\"img-fluid\" alt=\"Stress Intensity Factor Calculator\" /></div>"

st.components.v1.iframe(iframe_src_3d_url, width=800, height = 600, scrolling=False)
st.components.v1.html(image_html_block, width=800, height=600, scrolling=False)

total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

Point = namedtuple('Point', 'x y')
data = []

points_per_turn = total_points / num_turns

for curr_point_num in range(total_points):
    curr_turn, i = divmod(curr_point_num, points_per_turn)
    angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
    radius = curr_point_num / total_points
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    data.append(Point(x, y))

st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
    .mark_circle(color='#0068c9', opacity=0.5)
    .encode(x='x:Q', y='y:Q'))
