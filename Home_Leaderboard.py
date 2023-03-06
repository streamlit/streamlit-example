import pandas as pd
import streamlit as st
from snowflake.snowpark import Session
import plotly.express as px
from global_functions import get_session
from snowflake.snowpark import functions as F
from datetime import datetime
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

tournament = st.secrets['current_event']

session = get_session()


st.write(f"# {tournament}")

# create Snowpark Dataframes

leaderboard_display_df = session.table('leaderboard_display_vw').filter(F.col('TOURNAMENT') == tournament).drop(['TOURNAMENT'])

picks_df = session.table('POOL_COLUMNAR_VW').filter(F.col('TOURNAMENT') == tournament)[["ENTRY_NAME","GOLFER"]]
selection_df = picks_df.group_by(F.col("GOLFER")).agg(F.count("ENTRY_NAME")).with_column_renamed(F.col("COUNT(ENTRY_NAME)"),"SELECTIONS")  # type: ignore
player_df = session.table('PLAYER_LEADERBOARD_VW').filter(F.col('EVENT_NAME') == tournament)
player_leaderboard_df = selection_df.join(player_df,F.col("FULL_NAME") == F.col("GOLFER"))
last_refresh = session.table('SCOREBOARD').filter(F.col('EVENT_NAME') == tournament).distinct().agg(F.max("LAST_UPDATED"))

# PROTOTYPE FOR SELECT AND HIGHLIGHT FUNCTIONALITY
# gd = GridOptionsBuilder.from_dataframe(leaderboard_display_df.to_pandas())
# gd.configure_pagination(enabled=True)
# gd.configure_default_column(editable=True, groupable=True)
# gd.configure_selection(selection_mode="single", use_checkbox=True)
# gridoptions = gd.build()
# grid_table = AgGrid(
#     leaderboard_display_df.to_pandas(),
#     gridOptions=gridoptions,
#     update_mode=GridUpdateMode.SELECTION_CHANGED,
#     theme="streamlit",
# )

try:
  tournament_cut_line = int(session.table('tournaments_vw').filter(F.col("TOURNAMENT") == tournament).collect()[0][2]) # type: ignore
  cut_player_score = tournament_cut_line + 1
except TypeError:
  tournament_cut_line = 'TBD'
  cut_player_score = 'TBD'

if leaderboard_display_df.count() > 0:
  with st.spinner('Getting yardages...'):
      st.write('#### Member Leaderboard')
      st.write(f"""```{last_refresh.collect()[0][0].strftime("%A %b %d %I:%M %p")}```""")
      leaderboard_display = leaderboard_display_df.to_pandas()
      leaderboard_display['SELECTIONS'] = leaderboard_display['SELECTIONS'].apply(lambda x: [sel.strip() for sel in x.split(",")])
      st.dataframe(leaderboard_display.set_index('RANK'))
      st.write(f"#### Cut = {tournament_cut_line}")
      st.write(f"All golfers who miss the cut will reflect as __{cut_player_score}__ for scoring")
      st.write("")
      st.write('#### Selected Player Leaderboard')
      st.dataframe(player_leaderboard_df[['POSITION','GOLFER','TOTAL','THRU','SELECTIONS']].to_pandas().set_index('POSITION'),height=825)


else:
  st.write(f"Whoops...the players are still warming up! {tournament} hasn't started yet...come back later!")
  st.image('assets/tiger-woods-gif.gif')