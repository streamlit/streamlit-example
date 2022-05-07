from collections import namedtuple
import altair as alt
import math

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
    st.map(map)

    # Selection Box
    guide = pd.read_csv("regions-labels.csv")
    guide = pd.Series(guide.label.values, index=guide.id).to_dict()
    medium = df.local_authority_district.unique().tolist()
    medium.remove(-1)
    region_setup = []
    for item in medium:
        region_name = guide[item]
        region_setup.append(region_name)
    region_setup = sorted(region_setup)
    region = pd.Series(region_setup, index=medium).to_dict()
    region_rev = pd.Series(medium, index=region_setup).to_dict()
    option_setup = st.selectbox("Which region do you want to view?", sorted(region.values()))
    option = region_rev[option_setup]

    # SQ2 --> Pie Chart
    df_v = pd.read_csv("dft-road-casualty-statistics-vehicle-2020.csv", low_memory=False)

    #fig1, ax = plt.subplots()
    #ax.pie(df[''].value_counts(), labels=labels)
    #st.pyplot(fig1)


    # SQ3 --> Bar Chart
    labels = 'Slight', 'Serious', 'Fatal'
    df_3 = df.loc[df['local_authority_district'] == option]
    severity_count_setup = df_3['accident_severity'].value_counts().tolist()
    print(severity_count_setup)
    severity_count = pd.DataFrame(severity_count_setup, index=['Slightly', 'Serious', 'Fatal'])
    print(severity_count)
    st.bar_chart(severity_count)

    # SQ4 --> Line Chart


    # SQ5 --> Bar Chart
    df_5 = df.loc[df['local_authority_district'] == option]
    severity_count_setup = df_5['day_of_week'].value_counts().tolist()
    severity_count = pd.DataFrame(severity_count_setup, index=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    st.bar_chart(severity_count)
