import pandas as pd
import streamlit as st
from snowflake.snowpark import Session
import plotly.express as px
from global_functions import create_connection, cache_local_dataframe
from snowflake.snowpark import functions as F

tournament = st.secrets['current_event']

if "snowpark_session" not in st.session_state:
  session = create_connection()
  st.session_state['snowpark_session'] = session
else:
  session = st.session_state['snowpark_session']

session = create_connection()

st.write(f"# {tournament}")

# create Snowpark Dataframes
try:
  leaderboard_display_df = session.table('leaderboard_display_vw').filter(F.col("TOURNAMENT") == tournament)
  tournament_cut_line = int(session.table('tournaments_vw').filter(F.col("TOURNAMENT") == tournament).collect()[0][2]) # type: ignore

  with st.spinner('Getting yardages...'):
      st.dataframe(leaderboard_display_df)
      st.write(f"#### Cut = {tournament_cut_line}")

      st.write(f"All golfers who miss the cut will reflect as __{tournament_cut_line + 1}__ for scoring")


except TypeError:
  st.write(f"Whoops...the players are still warming up! {tournament} hasn't started yet...come back later!")
  st.image('assets/tiger-woods-gif.gif')
  