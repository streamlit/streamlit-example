import pandas as pd
import streamlit as st
import snowflake.connector
import plotly.express as px
import datetime


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


with st.sidebar:
    page = st.radio('',
        ("Leaderboard","Analysis")
    )

current_event = st.secrets['current_event']

pool_df = run_query(f"select * from GOLF.PUBLIC.pools_vw where tournament='{current_event}'")
pool_leaderboard_df = run_query(f"select * from GOLF.PUBLIC.pool_leaderboard_vw where tournament='{current_event}'")
pool_analytics_df = run_query(f"select * from GOLF.PUBLIC.pools_columnar_vw where tournament='{current_event}'")
pool_leaderboard_analytics_df = run_query(f"select * from GOLF.PUBLIC.pool_leaderboard_analytics_vw where tournament='{current_event}'")
pool_leaderboard_analytics_df = pool_leaderboard_analytics_df.convert_dtypes(infer_objects=True)
pool_trend_df = run_query(f"select * from GOLF.PUBLIC.POOL_LEADERBOARD_TREND_VW where tournament='{current_event}';")
tourney_df = run_query(f"select * from GOLF.PUBLIC.SCOREBOARD_MASTER_FILTERED_VW where tournament='{current_event}';")
tourney_df = tourney_df.convert_dtypes(infer_objects=True)
tourney_latest_df = tourney_df.loc[tourney_df['UPDATED'] == tourney_df["UPDATED"].max()]

selection_dict = tourney_latest_df[['PLAYER','NICKNAME']].drop_duplicates().to_dict()

# create selection lookup dictionary for styling
def create_lookup():
    res = []
    [res.append(x) for x in list(selection_dict['NICKNAME'].values()) if x not in res]
    selection_lookup_dict = {}
    for i in res:
        selection_lookup_dict[i] = []
    for p in selection_dict['PLAYER']:
        selection_lookup_dict[selection_dict['NICKNAME'][p]].append(selection_dict['PLAYER'][p])
    return selection_lookup_dict    

selection_lookup_dict = create_lookup()

def highlight_cells_pool(val):
    if val == selected_nickname:
        color = 'green'
    else:
        color = ''
    return 'background-color: {}'.format(color)

def highlight_cells_golf(val):
    if val in selection_lookup_dict[selected_nickname]:
        color = 'green'
    else:
        color = ''
    return 'background-color: {}'.format(color)

st.write(
f"""
# {page}
 Last Updated - {(tourney_df['UPDATED'].max()+datetime.timedelta(hours=-4)).strftime('%I:%M %p EST | %m-%d-%Y ')}

"""
)

if page == 'Leaderboard':
    selected_nickname = st.selectbox('Select Nickname',options=pool_leaderboard_df["NICKNAME"].to_list())
    st.write('#### Pool Standings')
    st.dataframe(pool_leaderboard_df[['RANK','NICKNAME','SCORE']].style.applymap(highlight_cells_pool))

    unique_df = pd.DataFrame(pool_leaderboard_analytics_df.groupby(['PLAYER'])['NICKNAME'].count().sort_values(ascending=False))
    unique_df['PLAYER'] = unique_df.index
    unique_df = unique_df.join(tourney_latest_df[['PLAYER','SCORE','THRU']].drop_duplicates().set_index('PLAYER'),how='right')
    unique_df.rename(columns={"NICKNAME" : "SELECTIONS"},inplace=True)
    unique_df = unique_df[['SCORE','THRU','SELECTIONS']].reset_index()
    st.write('#### Golfer Standings')
    st.dataframe(unique_df[['PLAYER','SCORE','THRU','SELECTIONS']].sort_values(by='SCORE').style.applymap(highlight_cells_golf),height=800)

if page == "Analysis":

    player_trend_df = tourney_df[["PLAYER","SCORE","UPDATED","THRU"]].fillna(0).sort_values(by=['PLAYER','UPDATED'], ascending= [0,0])

    st.write('### Pool Trend')
    fig1 = px.line(
        pool_trend_df,
        x="UPDATED",
        y="SCORE",
        color="NICKNAME",
        markers=False,
        template='none',
        hover_data=["NICKNAME","SCORE","UPDATED"]       
    )

    fig1.update_layout(
        xaxis = dict(
            tickmode = 'linear'
        )
    )
    fig1.update_yaxes(autorange="reversed")
    st.plotly_chart(fig1,use_container_width=True)

    st.write('### Tournament Trend')

    fig2 = px.line(
        player_trend_df,
        x="UPDATED",
        y="SCORE",
        color="PLAYER",
        markers=False,
        template='none',
        hover_data=["PLAYER","SCORE","UPDATED","THRU"]
    )

    fig2.update_layout(
        xaxis = dict(
            tickmode = 'linear'
        )
    )
    fig2.update_yaxes(autorange="reversed")
    st.plotly_chart(fig2,use_container_width=True)