import pandas as pd
import streamlit as st
from snowflake.snowpark import Session
import plotly.express as px
from global_functions import create_connection, cache_local_dataframe


current_event = st.secrets['current_event']

if "snowpark_session" not in st.session_state:
  session = create_connection()
  st.session_state['snowpark_session'] = session
else:
  session = st.session_state['snowpark_session']

session = create_connection()

# create Snowpark Dataframes
leaderboard_display_df = session.table('leaderboard_display_vw')


leaderboard = cache_local_dataframe(leaderboard_display_df.to_pandas())
st.dataframe(leaderboard)
st.write("__Scoreboard reflects the projected cut of E__")
