import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark import Session, functions as F
from global_functions import get_session, check_password
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

def get_pre_tourney_odds() -> requests.Response:
    url = f"https://feeds.datagolf.com/preds/pre-tournament?tour=pga&odds_format=percent&key={st.secrets['api_key']}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response

if not check_password():
    st.write('☠️ Not Authorized ☠️')
else:
    session = get_session()

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
        if st.button('Truncate Pool Staging',):
            with st.spinner('Clearing table!'):
                session.sql('DELETE FROM GOLF_NEW.RAW.POOL_STAGING').collect()
        
    with st.expander('Entry Manager'):
        member_reference_df = session.table('GOLF_NEW.ANALYTICS.MEMBERS_VW').to_pandas()
        unconfirmed_entries_df = session.table('GOLF_NEW.RAW.POOL_STAGING').to_pandas()
        unconfirmed_entries_df.insert(loc=1,column='MEMBER_ID',value=pd.Series(dtype='int'))

        # The code below is for the title and logo.
        # st.info("💡 Hold the `Shift` (⇧) key to select multiple rows at once.")
        st.caption("")
        gd = GridOptionsBuilder.from_dataframe(unconfirmed_entries_df)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(editable=True, groupable=True)
        gd.configure_selection(selection_mode="multiple", use_checkbox=True)
        gridoptions = gd.build()
        grid_table = AgGrid(
            unconfirmed_entries_df,
            gridOptions=gridoptions,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            theme="streamlit",
        )

        st.dataframe(member_reference_df)
        sel_row = grid_table["selected_rows"]

        st.write("")

        try:
            df_sel_row = pd.DataFrame(sel_row)
            validated_df = df_sel_row[['ENTRY_NAME','MEMBER_ID','GOLFER_1','GOLFER_2','GOLFER_3','GOLFER_4','GOLFER_5','TOURNAMENT']]
            st.dataframe(validated_df)

            if st.button('Insert Validated Pool Entries'):
                with st.spinner('Adding entries to Pool'):
                    session.write_pandas(validated_df,'POOL',schema='RAW',database='GOLF_NEW',overwrite=False)

        except KeyError:
            st.write('No Selections Made')