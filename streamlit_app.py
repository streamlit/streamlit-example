import pandas as pd
import streamlit as st
from snowflake.snowpark import Session
import plotly.express as px
import datetime


@st.experimental_singleton # magic to cache db connection
def create_connection():
    connection_parameters = {
        "account": st.secrets["account"],
        "user": st.secrets["user"],
        "password": st.secrets["password"],
        "role": st.secrets["role"],
        "warehouse": st.secrets["warehouse"],
        "database": st.secrets["database"],
        "schema": st.secrets["schema"]
        }

    session = Session.builder.configs(connection_parameters).create()
    return session



@st.experimental_memo(ttl=300) # 5 minute object cache, or when query changes. Applies to all usage of this func.
def create_local_dataframe(_snowpark_dataframe):
    df = _snowpark_dataframe.to_pandas()
    return pd.DataFrame(df)

tab1, tab2 = st.tabs(["Leaderboard", "Trends"])
# tab1 = st.tabs(["Leaderboard"])

current_event = st.secrets['current_event']

session = create_connection()

# create Snowpark Dataframes
leaderboard_display_df = session.table('leaderboard_display_vw')




with tab1:
    leaderboard = create_local_dataframe(leaderboard_display_df)
    st.dataframe(leaderboard)

with tab2:
    st.write("Under Construction")