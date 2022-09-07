from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import snowflake.connector


@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])


conn = init_connection()


@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


rows = run_query("SELECT PHONE_NUMBER, CUSTOMER_UUID from DWH_DEV.LIAN_TEST.PHONE_NUMBERCUSTOMERUUIDMAP limit 10;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")