import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import datetime as dt

st.header('Data Visualization')

st.image("https://www.simplilearn.com/ice9/free_resources_article_thumb/Data_Visualization_Tools.jpg", width=700)
#@st.cache_data

#uploaded_file = st.file_uploader("Choose a file")
#if uploaded_file is not None:
#    df = pd.read_csv(uploaded_file).sample(n=100000)

            
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

  
df = load_data('Dataviz_12_06_2023.csv')
    
df.dropna(subset=['LATITUDE', 'LONGITUDE','CRASH_DATE','CRASH_TIME'], inplace=True)


df['date/time'] = pd.to_datetime(df['CRASH_DATE'] + ' ' + df['CRASH_TIME'])
data = df

#1. Visualization
st.header("Where are the most people injured in France?")
injured_people = st.slider("Number of person injured in road accident",0, 100)
st.map(data.query("INJURED_PERSONS >= @injured_people")[['LATITUDE', 'LONGITUDE']].dropna(how="any"))

#2. Visualization ######################
st.header("How many road accident during a given time of the day?")
hour = st.slider("Hour to look at", 0, 23)
severity = st.radio("Severity",('Not Severe', 'Severe', 'All'))
if severity=='Not Severe':
     severity=0
if severity=='Severe':
     severity=1

st.markdown("road accident between %i:00 and %i:00" % (hour, (hour + 1) % 24))

chart_data = df[['LATITUDE','LONGITUDE','date/time','severity']].dropna(how="any")
chart_data=chart_data.rename(columns={"LATITUDE": "lat", "LONGITUDE": "lon"})
if severity!='All':
     severity=chart_data=chart_data[chart_data['severity'] == severity]
vis_data=chart_data[chart_data['date/time'].dt.hour == hour]

def pychart(dataframe):
     st.pydeck_chart(pdk.Deck(
          map_style=None,
            initial_view_state=pdk.ViewState(
                 latitude=48.85,
                 longitude=2.35,
                 zoom=6,
                 pitch=50,
            ),
            layers=[pdk.Layer(
                 'HexagonLayer',
                 data=dataframe,
                 get_position='[lon, lat]',
                 radius=50,
                 elevation_scale=10,
                 elevation_range=[20, 500],
                 pickable=True,
                 extruded=True,),],
       ))

pychart(vis_data)
    #######################

#4. Visualization
st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) %24))
# filtered = data[
#  (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour +1))
# ]
hist = np.histogram(data['date/time'].dt.minute, bins=60, range=(0,60))[0]
chart_data = pd.DataFrame({'minute':range(60), 'crashes':hist})
fig = px.bar(chart_data, x='minute',y='crashes', hover_data=['minute','crashes'], height=400)
st.write(fig)

#5. Visualization
st.header("Top 8 dangerous area by zone")
#select = st.selectbox('Injured people', ['Pedestrian','Cyclists','Motorists'])
select = st.selectbox('Injured people', ['Department','Commune','Street'])

if select == 'Department':
     st.write(data.query("INJURED_PERSONS >= 1")[["dep","INJURED_PERSONS"]].sort_values(by=['INJURED_PERSONS'], ascending=False).dropna(how='any')[:8])
elif select == 'Commune':
       st.write(data.query("INJURED_PERSONS >= 1")[["com","INJURED_PERSONS"]].sort_values(by=['INJURED_PERSONS'], ascending=False).dropna(how='any')[:8])
else:
       st.write(data.query("INJURED_PERSONS >= 1")[["ON_STREET_NAME","INJURED_PERSONS"]].sort_values(by=['INJURED_PERSONS'], ascending=False).dropna(how='any')[:8])


if st.checkbox("Show Raw Data", False):
   st.subheader('Raw Data')
   st.write(data)

