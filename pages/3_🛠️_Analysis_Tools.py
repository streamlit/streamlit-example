import streamlit as st
from global_functions import get_session
import pandas as pd
from snowflake.snowpark import Session, functions as F
import logging

@st.cache(ttl=300)
def get_pick_options() -> pd.DataFrame:
  df = session.table('GOLF_NEW.RAW.PICK_OPTIONS').to_pandas()
  return pd.DataFrame(df)

def convert_to_int(x):
  try:
    return int(x)
  except:
    return 18

session = get_session()
tournament = st.secrets["current_event"]

st.title('🛠️ Analysis Tools')

tab1,tab2,tab3 = st.tabs(["Matchup Analysis", "Golfer History","Member Performance"])

with tab1:
  st.write(f'### {tournament}')
  picks_df = session.table('TOURNEY_PICK_DETAIL_VW').to_pandas().set_index('POSITION')

  entries = picks_df['ENTRY_NAME'].drop_duplicates().to_list()
  col1, col2 = st.columns(2)
  
  compare = st.multiselect('Compare 2 Entries:',entries,max_selections=2)
    
  if len(compare) == 2:

    compare_df = picks_df[picks_df['ENTRY_NAME'].isin(compare)]

    # group by pick and count the number of unique entry names for each pick
    counts = compare_df.groupby('GOLFER')['ENTRY_NAME'].nunique().reset_index(name='count')

    # filter picks with count equal to 2 (i.e., picks that appear in both entries)
    picks_to_exclude = counts[counts['count'] == 2]['GOLFER'].tolist()

    # filter the original dataframe to exclude the picks that appear in both entries
    result_df = compare_df[~compare_df['GOLFER'].isin(picks_to_exclude)]
  
    col1, col2 = st.columns(2)

    with col1:
      st.write(f"#### {compare[0]}")
      member_1_df = result_df[result_df['ENTRY_NAME'] == compare[0]]
      st.write(f"##### {member_1_df['TOTAL'].sum()}")
      holes_played = member_1_df[member_1_df['THRU'] != 'CUT']['THRU'].to_list()
      holes_played = [convert_to_int(x) for x in holes_played]
      st.dataframe(member_1_df[['GOLFER','THRU','TOTAL']])
      st.write(f"Holes left today: {(18*len(member_1_df[member_1_df['THRU'] != 'CUT'])) - sum(holes_played)}")

    with col2:
      st.write(f"#### {compare[1]}")
      member_2_df = result_df[result_df['ENTRY_NAME'] == compare[1]]
      st.write(f"##### {member_2_df['TOTAL'].sum()}")
      holes_played = member_2_df[member_2_df['THRU'] != 'CUT']['THRU'].to_list()
      holes_played = [convert_to_int(x) for x in holes_played]
      st.dataframe(member_2_df[['GOLFER','THRU','TOTAL']])
      st.write(f"Holes left today: {(18*len(member_2_df[member_2_df['THRU'] != 'CUT'])) - sum(holes_played)}")

with tab2:
  st.write('Under Construction')

with tab3:
  st.write('Under Construction')