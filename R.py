import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

from pathlib import Path
#DATA_URL = Path(Training/Datascientist/Coursera).parents[1] / 'Motor_Vehicle_Collisions_-_Crashes.csv'

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  DATA_URL = pd.read_csv(uploaded_file).sample(n=30000)
    
st.title("Road Accident in France")
st.markdown("This application is a Streamlit dashboard that can be use to analyze road accident in France🗼🥐🇫🇷🥖🚗💥🚙")

from PIL import Image
image = Image.open('sunrise.jpg')
st.image("https://s3-us-west-2.amazonaws.com/uw-s3-cdn/wp-content/uploads/sites/6/2017/11/04133712/waterfall.jpg",
            width=400, # Manually Adjust the width of the image as per requirement
        )
#st.image(product_img[0]), width = 400, caption='Sunrise by the mountains')
#st.image(image, caption='Sunrise by the mountains')

#video_file = open('ADOIT.mp4', 'rb')
#video_bytes = video_file.read()
#st.video(video_bytes)

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL,nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data


data = load_data(100000)
original_data = data

st.header("Where are the most people injured in France?")
injured_people = st.slider("Number of person injured in road accident",0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude","longitude"]].dropna(how="any"))


st.header("How many road accident during a given time of the day?")
hour = st.slider("Hour to look at", 0, 23)
data = data[data['date/time'].dt.hour == hour]

st.markdown("road accident between %i:00 and %i:00" % (hour, (hour + 1) % 24))
midpoint = (np.average(data['latitude']), np.average(data['longitude']))

st.write(pdk.Deck(
     map_style="mapbox://styles/mapbox/light-v9",
     initial_view_state={
         "latitude": midpoint[0],
         "longitude": midpoint[1],
         "zoom": 11,
         "pitch": 50,
     },
     layers=[
         pdk.Layer(
         "HexagonLayer",
         data=data[['date/time','latitude','longitude']],
         get_position=['longitude','latitude'],
         radius=100,
         extruded=True,
         pickable=True,
         elevation_scale=4,
         elevation_range=[0,1000],
         ),
     ],
))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) %24))
filtered = data[
     (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour +1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))[0]
chart_data = pd.DataFrame({'minute':range(60), 'crashes':hist})
fig = px.bar(chart_data, x='minute',y='crashes', hover_data=['minute','crashes'], height=400)
st.write(fig)

st.header("Top 5 dangerous city by injury type")
select = st.selectbox('Injured people', ['Pedestrian','Cyclists','Motorists'])

if select == 'Pedestrian':
    st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name","injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how='any')[:5])

elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists >= 1") [["on_street_name","injured_cyclists"]].sort_values(by=['injured_cyclists'], ascending=False).dropna(how='any')[:5])

else:
    st.write(original_data.query("injured_motorists >= 1") [["on_street_name","injured_motorists"]].sort_values(by=['injured_motorists'], ascending=False).dropna(how='any')[:5])





if st.checkbox("Show Raw Data", False):
   st.subheader('Raw Data')
   st.write(data)
