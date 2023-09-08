from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Stress Intensity Factor Calculator (Proof of Concept)

"""


# with st.echo(code_location='below'):
iframe_src_3d_url = "https://3dwarehouse.sketchup.com/embed/9658ccab-6ac3-4b89-a23f-635206942357"
image_html_block = "<div class=\"col-lg-6 card my-2 px-3\" style=\"width: max-content;\"> <img src=\"https://hint1412.github.io/XLiu.github.io/SIF/images/Notched_cantilever_sketch.png\" class=\"img-fluid\" alt=\"Stress Intensity Factor Calculator\" /></div>"

test_iframe = st.components.v1.iframe(iframe_src_3d_url, width=800, height = 600, scrolling=False)

test_image = st.components.v1.html(image_html_block, width=800, height=600, scrolling=False)

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
