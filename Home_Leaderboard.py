import pandas as pd
import streamlit as st
from snowflake.snowpark import Session
import plotly.express as px
from global_functions import get_session
from snowflake.snowpark import functions as F

tournament = st.secrets['current_event']

session = get_session()


st.write(f"# {tournament}")

# create Snowpark Dataframes

leaderboard_display_df = session.table('leaderboard_display_vw').filter(F.col('TOURNAMENT') == tournament)

try:
  tournament_cut_line = int(session.table('tournaments_vw').filter(F.col("TOURNAMENT") == tournament).collect()[0][2]) # type: ignore
  cut_player_score = tournament_cut_line + 1
except TypeError:
  tournament_cut_line = 'TBD'
  cut_player_score = 'TBD'

if leaderboard_display_df.count() > 0:
  with st.spinner('Getting yardages...'):
      st.dataframe(leaderboard_display_df.drop(['TOURNAMENT']))
      st.write(f"#### Cut = {tournament_cut_line}")
      st.write(f"All golfers who miss the cut will reflect as __{cut_player_score}__ for scoring")


else:
  st.write(f"Whoops...the players are still warming up! {tournament} hasn't started yet...come back later!")
  st.image('assets/tiger-woods-gif.gif')
