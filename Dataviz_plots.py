import pandas as pd
import numpy as np 
from   matplotlib import style
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import plotly.express as px


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file,low_memory=False).sample(n=200000)
      
st.markdown("""4.1 Visualisation of Accident severity trends across different years.
        - we can see that death rate in accidents is slightly getting reduced over years
        - Number of accidents also show a reducing trend over years 
""")

st.write(df)

st.dataframe(df)

# Extract data for visualisation
df = pd.DataFrame(columns=['AccidentId', 'AccidentSeverity', 'Year'])
df['AccidentId'] = df['AccidentId']
df['Year'] = df['Year'].astype(float)
df['AccidentSeverity'] = df['AccidentSeverity'].astype(str)
df['AccidentSeverity'] = df['AccidentSeverity']. replace(['1','2','3','4'], ['Not Injured','Died','Injured&Hospitalised','Slightly Injured'])

st.write(df)

st.dataframe(df)
# Visualise extracted data

df1 = pd.melt(df, 
              value_vars=['Widgets','Wodgets','Wudgets'], 
              id_vars=['Years'],
              var_name='Name'
              )

c = px.bar(df1, x="Year", y="AccidentId",
             color='AccidentSeverity', barmode='stack',
             height=400)

c.update_layout(paper_bgcolor="white", 
                plot_bgcolor="white", 
                yaxis_gridcolor= "black",
                yaxis_linecolor= "black",
                xaxis_linecolor= "black")

st.plotly_chart(c)


