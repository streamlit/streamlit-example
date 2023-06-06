import pandas as pd
import numpy as np 
from   matplotlib import style
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import altair as alt
import plotly.express as px

     
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
   df = pd.read_csv(uploaded_file,low_memory=False).sample(n=100000)
   
st.markdown("""4.1 Visualisation of Accident severity trends across different years.
        - we can see that death rate in accidents is slightly getting reduced over years
        - Number of accidents also show a reducing trend over years 
""")

# Extract data for visualisation
df1 = pd.DataFrame(df)     
          #df['AccidentId'] = df['AccidentId']
          #df['Year'] = df['Year'].astype(float)
df1['AccidentSeverity'] = df1['AccidentSeverity'].astype(str)
df1['AccidentSeverity'] = df1['AccidentSeverity']. replace(['1','2','3','4'], ['Not Injured','Died','Injured&Hospitalised','Slightly Injured'])

   # Visualise extracted data
road_accidents = pd.DataFrame({'AccidentSeverity','AccidentId','Year'})
 
bar_chart = alt.Chart(road_accidents).mark_bar().encode(
        x="year(Year):O",
        y="sum(AccidentId):Q",
        color="AccidentSeverity:N"
    )
st.altair_chart(bar_chart, use_container_width=True)

