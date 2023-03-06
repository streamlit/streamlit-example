import streamlit as st
from snowflake.snowpark import Session
from global_functions import get_session

session = get_session()

st.title('Trophy Room')

with st.spinner('Checking the trophy room!'):

    st.write('## 🏆 The Race For The 80 Yard Bombs Cup')
    cup_standings_df = session.table('cup_standings')
    st.dataframe(cup_standings_df.to_pandas().set_index('OVERALL_RANK'))

    st.write("## 🥇 Winner's Circle")
    winners_circle_df = session.table('winners_circle_vw').to_pandas()
    winners_circle_df['TOURNAMENT'].replace({'The Masters': 'The Masters 🏅',
                                             'PGA Championship': 'PGA Championship 🏅',
                                             'U.S. Open': 'U.S. Open 🏅',
                                             'The Open Championship': 'The Open Championship 🏅'}, inplace=True)
    st.dataframe(winners_circle_df)
