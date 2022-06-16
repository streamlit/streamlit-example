# from collections import namedtuple
# from re import T
# from time import altzone
# from tkinter import Scrollbar
# from unicodedata import decimal
# import altair as alt
# import math
# from numpy import NaN, column_stack
import pandas as pd
import streamlit as st
import snowflake.connector
import plotly.express as px
import datetime
# import numpy as np
# import matplotlib.pyplot as plt

# hide_dataframe_row_index = """
#             <style>
#             .row_heading.level0 {display:none}
#             .blank {display:none}
#             </style>
#             """
            
# st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)


@st.experimental_singleton # magic to cache db connection
def create_connection():
    con = snowflake.connector.connect(
        user=st.secrets["user"],
        password=st.secrets["password"],
        account=st.secrets["account"],
        session_parameters={
            'QUERY_TAG': st.secrets["query_tag"],
            'ROLE':st.secrets["role"]
        }
    )   
    return con

con = create_connection()

@st.experimental_memo(ttl=300) # 5 minute object cache, or when query changes. Applies to all usage of this func.
def run_query(query):
    with con.cursor() as cur:
        cur.execute(query)
        return pd.DataFrame(cur.fetch_pandas_all())


# with st.sidebar:
#     page = st.radio('',
#         ("Pool Leaderboard","Golfer Leaderboard","Analysis")
#     )

page = 'U.S. Open Pool Leaderboard'

pool_df = run_query('select * from GOLF.PUBLIC.pools_vw')
# pool_leaderboard_df = run_query('select * from GOLF.PUBLIC.pool_leaderboard_vw')
# pool_analytics_df = run_query('select * from GOLF.PUBLIC.pools_columnar_vw')
# pool_leaderboard_analytics_df = run_query('select * from GOLF.PUBLIC.pool_leaderboard_analytics_vw;')
# pool_leaderboard_analytics_df = pool_leaderboard_analytics_df.convert_dtypes(infer_objects=True)
tourney_df = run_query("select * from GOLF.PUBLIC.scoreboard_master_vw;")
tourney_df = tourney_df.convert_dtypes(infer_objects=True)







f"""
# {page}
Last Updated - {(tourney_df['UPDATED'].max()+datetime.timedelta(hours=-4)).strftime('%I:%M %p EST | %m-%d-%Y ')}

"""



if page == 'U.S. Open Pool Leaderboard':
    
    st.write(pool_df[["NICKNAME","GOLFER_1","GOLFER_2","GOLFER_3","GOLFER_4","GOLFER_5"]])
    st.write()
        

    # temp_df = tourney_df[['PLAYER','SCORE','UPDATED']]
    # temp_df['PLAYER'] = temp_df['PLAYER'].astype('str')
    # temp_df['SCORE'] = temp_df['SCORE'].astype('int',)
    # # temp_df['PLAYER'] = temp_df['PLAYER'].astype('str')

    # fig2 = px.line(
    #     tourney_df[["PLAYER","SCORE","UPDATED","THRU"]].fillna(0),
    #     x="UPDATED",
    #     y="SCORE",
    #     color="PLAYER",
    #     markers=True,
    #     template='none',
    #     hover_data=["PLAYER","SCORE","UPDATED","THRU"]
    # )

    # fig2.update_layout(
    #     xaxis = dict(
    #         tickmode = 'linear'
    #     )
    # )
    # fig2.update_yaxes(autorange="reversed")
    # st.plotly_chart(fig2,use_container_width=True)

    # fig, ax = plt.subplots()
    # ax.scatter(x=pool_leaderboard_analytics_df['SCORE'],)

    # st.pyplot(fig)

# if page == 'Golfer Leaderboard':
#     tourney_df = run_query("select * from GOLF.PUBLIC.scoreboard_master_vw;")
#     tourney_df = tourney_df.convert_dtypes(infer_objects=True)
#     st.dataframe(tourney_df[['POS','PLAYER','SCORE','THRU','TODAY']],)

#     st.plotly_chart(
#         px.bar(tourney_df[tourney_df['SCORE'] != 'nan'],x='PLAYER',y='SCORE',),
#         use_container_width=True
#     )



# if page == "Analysis":
    
#     unique_df = pd.DataFrame(pool_leaderboard_analytics_df.groupby(['PLAYER'])['NICKNAME'].count().sort_values(ascending=False))
#     unique_df['PLAYER'] = unique_df.index
#     unique_df.rename(columns={"NICKNAME" : "Selections"},inplace=True)
#     st.write('#### Unique Selections')
#     st.write(unique_df[['PLAYER','Selections']])