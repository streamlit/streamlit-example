import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark import Session, functions as F
from global_functions import create_connection, check_password

def get_pre_tourney_odds():
    url = f"https://feeds.datagolf.com/preds/pre-tournament?tour=pga&odds_format=percent&key={st.secrets['api_key']}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response

if not check_password():
    st.write('☠️ Not Authorized ☠️')
else:
    if "snowpark_session" not in st.session_state:
        session = create_connection()
        st.session_state['snowpark_session'] = session
    else:
        session = st.session_state['snowpark_session']

    with st.expander('Pre-Tourney Checklist'):
        st.checkbox('Copy Event Name into the Secrets config')
        st.checkbox('Generate Player Pick List')
        st.checkbox('Generate Tournament Record')
        st.checkbox('Truncate POOL_STAGING table')
        st.checkbox('Set the Entry Boolean to True')


    with st.expander('Tourney Setup'):


        # Get the top_5 odds list from DataGolf
        response = get_pre_tourney_odds()

        # Extract the tournament name
        tournament_name = response.json()["event_name"]

        # produce a ranked dataframe of players for picking
        pre_tourney_golfers = response.json()["baseline_history_fit"]
        pre_tourney_df = pd.DataFrame.from_dict(pre_tourney_golfers)[["player_name","top_5"]]
        pre_tourney_df.sort_values(by=['top_5'],inplace=True,ascending=False)
        pre_tourney_df["rank"] = pre_tourney_df["top_5"].rank(ascending=False).convert_dtypes()


        st.title(tournament_name)

        st.write(pre_tourney_df[0:16])

        if st.button('Generate Pick List'):
            with st.spinner('Inserting records...'):
                create_pick_list = session.write_pandas(pre_tourney_df[["player_name","rank"]],'PICK_OPTIONS',database='GOLF_NEW',schema='RAW',auto_create_table=True,overwrite=True)
                st.write(f"Created table: {create_pick_list.table_name}")


        par = int(st.radio('Select Par',[72,71,70])) # type: ignore
        
        tournament_record = pd.DataFrame.from_dict({
            "TOURNAMENT": [tournament_name],
            "PAR": [int(par)],
            "CUT": [pd.NA]
        })

        st.write(tournament_record)

        if st.button('Create Tournament Data'):
            with st.spinner('Inserting records...'):
                check = session.table('GOLF_NEW.RAW.TOURNAMENTS').filter(F.col('TOURNAMENT') == tournament_name).count()
                if check == 0:
                    session.create_dataframe(tournament_record).write.mode("append").save_as_table('GOLF_NEW.RAW.TOURNAMENTS')
                    st.write(tournament_name,' created')
                else:
                    st.write('Error: Tournament already exists.')

    with st.expander('Entry Tool'):
        if st.button('Truncate Pool Staging',):
            with st.spinner('Clearing table!'):
                session.sql('DELETE FROM GOLF_NEW.RAW.POOL_STAGING').collect()