# libraries
import streamlit as st
import pandas as pd
from datetime import datetime

# read data
df = pd.read_csv('./data/final_simulated_schedule.csv')

# page title
st.title("Schedule")

# select / filter routes
all_routes = df['route'].unique()
routes = st.sidebar.multiselect("Select Route", default = all_routes, options = all_routes)

# select / filter dates
min_date = df['date'].min()
min_date = datetime.strptime(min_date, '%Y-%m-%d') 
max_date = df['date'].max()
max_date = datetime.strptime(max_date, '%Y-%m-%d')

all_dates = df['date'].unique()
dates = st.sidebar.date_input('Select Date', datetime.today(), min_date, max_date)

# result set
df['date']= pd.to_datetime(df['date']).dt.date
output = df[df['date'] == dates]

output = output[output['route'].isin(routes)]

st.table(output)