import streamlit as st
from snowflake.snowpark import Session
from global_functions import get_session

session = get_session()

st.write('## 🏆 The Race For The 80 Yard Bombs Cup')

with st.spinner('Checking the trophy room!'):
    cup_standings_df = session.table('cup_standings')
    st.dataframe(cup_standings_df)

    st.write("## 🥇 Winner's Circle")
    winners_circle_df = session.table('winners_circle_vw')
    st.dataframe(winners_circle_df)
