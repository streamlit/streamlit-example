from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pickle
import numpy as np
import plotly.express as px

# Load the model into memory
with open('new_model.pkl', 'rb') as model_pkl:
    lr = pd.read_pickle(model_pkl)

# Create a text input for the user to enter the value for the unseen variable
#unseen = st.text_input('Введите количество безработных (тыс. человек):', 0)

unseen = st.slider("Количество безработных (в тыс. человек)", min_value = 0.0, max_value = 200.0, step = 0.1)


# Convert the input to a float and create a test observation
X_test_sm = [[float(1.0)], [float(unseen)]]
X_test_sm = np.squeeze(X_test_sm)

# Make a prediction using the model
result = lr.predict(X_test_sm)[0]

st.write(f'Количество алкоголиков: {result} (в тыс. человек)')

source = pd.DataFrame({
    'a': ['Алкаши', 'Наркоши'],
    'b': [result, 32]
})

st.altair_chart(alt.Chart(pd.DataFrame(source), height = 500, width = 500)


# Display the result
#if result < 0:
#    st.write(f'При количестве безработных в {float(unseen)} тыс. человек, алкоголиков не будет')
#else:
#    st.write(f'При количестве безработных в {float(unseen)} тыс. человек, количество алкоголиков будет составлять {result} тыс. человек')

#with st.echo(code_location='below'):
#    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
#    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)
#
#    Point = namedtuple('Point', 'x y')
#    data = []
#
#    points_per_turn = total_points / num_turns
#
#    for curr_point_num in range(total_points):
#        curr_turn, i = divmod(curr_point_num, points_per_turn)
#        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#        radius = curr_point_num / total_points
#        x = radius * math.cos(angle)
#        y = radius * math.sin(angle)
#        data.append(Point(x, y))
#
#    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#        .mark_circle(color='#0068c9', opacity=0.5)
#        .encode(x='x:Q', y='y:Q'))
