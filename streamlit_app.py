from collections import namedtuple
import altair as alt
import math
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st


CLIENT_ID = st.secrets["CLIENT_ID"]

"""
# Welcome to Spike Demo App!

"""


def load_steps_data():
    return pd.read_json('data_samples/steps_2022-03-01_2022-07-31.json')


def load_sleep_data():
    return pd.read_json('data_samples/sleep_2022-03-01_2022-07-31.json')


def load_summaries_data():
    return pd.read_json('data_samples/activities_summary_2022-03-01_2022-07-31.json')


def load_heart_data():
    return pd.read_json('data_samples/heart_2022-03-01_2022-07-31.json')


start_time = st.sidebar.slider(
    "When do you start?",
    value=datetime(2022, 3, 1, 0, 0),
    min_value=datetime(2022, 3, 1, 0, 0),
    max_value=datetime(2022, 7, 31, 0, 0),
    format="YYYY/MM/DD")
end_time = st.sidebar.slider(
    "When do you end?",
    value=datetime(2022, 7, 31, 0, 0),
    min_value=datetime(2022, 3, 1, 0, 0),
    max_value=datetime(2022, 7, 31, 0, 0),
    format="YYYY/MM/DD")
st.write("Start time:", start_time, "End time:", end_time)

st.sidebar.markdown('<style>.btn {font-family: "Poppins", Sans-serif;font-size: 12px;font-weight: 500;border-radius: 50px 50px 50px 50px;box-shadow: 0px 4px 10px -1px rgb(0 0 0 / 27%);padding: 14px 35px 14px 35px;width: 300px;border: unset;color: #f2f5f8;background-color: #1b2836;}</style>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    f"""
        <a href="https://spikeapi.com/app" target='_self'>Connect device</a>
    """,
    unsafe_allow_html=True,
)
# link = '[Connect device](https://spikeapi.com/app)'
# st.sidebar.markdown(link, unsafe_allow_html=True)

with st.echo(code_location='below'):

    steps_data = load_steps_data()
    steps_data.rename(columns={'value': 'steps'}, inplace=True)
    steps_data = steps_data[(steps_data['date'] >= start_time) & (steps_data['date'] <= end_time)]

    sleep_data = load_sleep_data()
    sleep_data = sleep_data[(sleep_data['date'] >= start_time) & (sleep_data['date'] <= end_time)]
    sleep_data["total_sleep_h"] = sleep_data.apply(lambda row: int(row.total_sleep / 3600), axis=1)

    summaries_data = load_summaries_data()
    summaries_data = summaries_data[(summaries_data['date'] >= start_time) & (summaries_data['date'] <= end_time)]
    summaries_data['cal_norm'] = summaries_data['calories_total'] / summaries_data['calories_total'].max()
    summaries_data['stress_norm'] = summaries_data['stress_duration'] / summaries_data['stress_duration'].max()

    heart_data = load_heart_data()
    heart_data = heart_data[(heart_data['date'] >= start_time) & (heart_data['date'] <= end_time)]

    df_merged = steps_data.reset_index().merge(sleep_data.reset_index(), how='left', on='date')
    df_merged['weekday'] = df_merged['date'].apply(lambda x: x.day_name())

    df_week_sleep = df_merged.groupby(['weekday'])['total_sleep_h'].mean()\
        .reset_index().sort_values('total_sleep_h', ascending=False)

    tab1, tab2, tab3 = st.tabs(["Sleep", "Activities", "Heart"])

    ########
    with tab1:
        base = alt.Chart(df_week_sleep).mark_bar(
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3
        ).encode(
            x=alt.X('total_sleep_h'),
            y=alt.Y('weekday', sort='-x')
        )
        st.altair_chart(base, use_container_width=True)
    ############
        interval = alt.selection_interval()
        base = alt.Chart(df_merged).mark_point().encode(
            x='total_sleep_h',
            y='steps',
            color=alt.condition(interval, 'weekday', alt.value('lightgray'))
        ).properties(
            selection=interval
        )
        st.altair_chart(base, use_container_width=True)

    with tab2:
        st.line_chart(steps_data, x='date', y='steps')

    with tab3:
        st.vega_lite_chart(heart_data, {
            'mark': {'type': 'circle', 'tooltip': True},
            'encoding': {
                'x': {'field': 'date', 'type': 'temporal'},
                # 'x': {'field': 'max_hr', 'type': 'quantitative', "scale": {"domain": [80, 150]}},
                'y': {'field': 'avg_hr', 'type': 'quantitative', "scale": {"domain": [60, 90]}},
                'size': {'field': 'resting_hr', 'type': 'quantitative', "scale": {"domain": [40, 70]}},
                'color': {'field': 'resting_hr', 'type': 'quantitative'},
            },
        }, use_container_width=True)

        b = alt.Chart(summaries_data).mark_line(opacity=1).encode(
            x='date', y='stress_norm')
        st.altair_chart(b, use_container_width=True)
