from collections import namedtuple
import altair as alt
import math

import pandas
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


with st.echo(code_location='below'):
    # SQ1 --> Heat Map
    df = pd.read_csv("dft-road-casualty-statistics-accident-2020.csv")
    map = pd.DataFrame()
    map['latitude'] = df['latitude'].dropna()
    map['longitude'] = df['longitude'].dropna()
    #print(max(map['longitude']), min(map['longitude']), max(map['latitude']), min(map['latitude']), map.dtypes)
    st.map(map)

    # SQ2 --> Pie Chart
    df = pd.read_csv("dft-road-casualty-statistics-accident-2020.csv")
    labels = 'Slight', 'Serious', 'Fatal'

    #fig1, ax = plt.subplots()
    #ax.pie(df[''].value_counts(), labels=labels)
    #st.pyplot(fig1)

    # SQ3 --> Bar Chart
    st.bar_chart(df['accident_severity'].value_counts())

    # SQ4 --> Line Chart
    guide = pd.read_csv("regions-labels.csv")
    #guide['id'] = guide['id'].astype(int)
    print(guide.dtypes)
    st.selectbox("Which region do you want to view?", df.local_authority_district.unique())

    # SQ5 --> Bar Chart
    st.bar_chart(df['day_of_week'].value_counts())
