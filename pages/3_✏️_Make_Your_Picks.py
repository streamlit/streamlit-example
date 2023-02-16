import streamlit as st
from global_functions import get_session
import pandas as pd
from snowflake.snowpark import Session, functions as F
import logging

@st.cache(ttl=300)
def get_pick_options() -> pd.DataFrame:
  df = session.table('GOLF_NEW.RAW.PICK_OPTIONS').to_pandas()
  return pd.DataFrame(df)

session = get_session()

if st.secrets['entry_boolean'] == 'False':
    st.write('## 🔒 Entries are currently locked')


else:
    # create dataframe and convert players to list, clean names up
    pick_options_df = get_pick_options()
    pick_list = pick_options_df["player_name"].to_list()
    pick_list = [x.split(', ')[1]+' '+x.split(', ')[0] for x in pick_list]

    # create slicers to separate out the pick lists
    first = pick_list[0:5]
    second = pick_list[5:16]
    third = pick_list[16:]

    tournament = st.secrets['current_event']

    # 
    st.title(f"Picks for {tournament}")
    with st.form(key='pick_form'):

      entry_name = st.text_input('Entry Name')

      golfer_1 = st.radio('Top 5 pick',first)
      golfer_2_and_3 = st.multiselect('Two 6 - 16 picks', second)
      golfer_4_and_5 = st.multiselect('Two 17+ picks',third)

      if st.form_submit_button('Submit Picks'):
        if len(golfer_2_and_3) == 2 and len(golfer_4_and_5) == 2 and len(entry_name) > 0:
          with st.spinner("Informing golfers they've been selected..."):
            golfer_2 = golfer_2_and_3[0]
            golfer_3 = golfer_2_and_3[1]
            golfer_4 = golfer_4_and_5[0]
            golfer_5 = golfer_4_and_5[1]

            try:
              session.write_pandas(
                pd.DataFrame.from_dict(
                  {
                    "ENTRY_NAME": [entry_name],
                    "GOLFER_1": [golfer_1],
                    "GOLFER_2": [golfer_2],
                    "GOLFER_3": [golfer_3],
                    "GOLFER_4": [golfer_4],
                    "GOLFER_5": [golfer_5],
                    "TOURNAMENT": [tournament] 
                  }
                )
                ,'POOL_STAGING',database='GOLF_NEW',schema='RAW',overwrite=False)

              st.write("✅ Submit Successful!")
              st.write("Hit the copy button below to transfer your picks to a note")
              st.code(entry_name+f' - {tournament}\n--------------\n'+golfer_1+'\n'+golfer_2+'\n'+golfer_3+'\n'+golfer_4+'\n'+golfer_5,language='markdown') # type: ignore

            except BaseException as error:
              st.write('Weird bug caught! Hit the copy button on the below output and send to the admin!')
              st.code('An exception occurred: {}'.format(error))

        else:
          st.write('⚠️ Validation Check Failed - please make sure you have 5 golfers selected and a valid entry name. ⚠️')

      