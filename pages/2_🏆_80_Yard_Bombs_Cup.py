import streamlit as st
from snowflake.snowpark import Session
from global_functions import create_connection, cache_local_dataframe

if "snowpark_session" not in st.session_state:
  session = create_connection()
  st.session_state['snowpark_session'] = session
else:
  session = st.session_state['snowpark_session']

st.write('## 🏆 The Race For The 80 Yard Bombs Cup')

cup_standings_df = session.table('cup_standings')


st.dataframe(cup_standings_df)