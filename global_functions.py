import streamlit as st
from snowflake.snowpark import Session
import pandas as pd

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
def cache_local_dataframe(local_dataframe):
    return pd.DataFrame(local_dataframe)