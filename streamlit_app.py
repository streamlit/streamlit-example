#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
#!pip install ta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas_datareader as web
import datetime as d
import yfinance as yf # https://pypi.org/project/yfinance/
from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.momentum import RSIIndicator
import plotly.graph_objs as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from datetime import date


# In[2]:


# sidebar #
###########
st.set_page_config(layout="wide")
crypto = st.sidebar.selectbox('Select one currency', ( "ADA","ATOM","AVAX","AXS","BTC","ETH","LINK","LUNA1","MATIC","SOL"))
import datetime
today = datetime.date.today()
before = today - datetime.timedelta(days=700)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)
if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')


# In[3]:


# Crypto data #
##############

# Download data
df = web.DataReader(f'{crypto}-USD', 'yahoo', start_date, end_date)

# Moving Average Convergence Divergence
macd = MACD(df['Close']).macd()

# Resistence Strength Indicator
rsi = RSIIndicator(df['Close']).rsi()


# In[4]:


###################
# Set up dashboard #
###################
#"https://www.hp.com/us-en/shop/app/assets/images/uploads/prod/cryptocurrency-trends_-is-bitcoin-mining-profitable-in-2021162075307076393.jpg"
st.image("https://www.hp.com/us-en/shop/app/assets/images/uploads/prod/cryptocurrency-trends_-is-bitcoin-mining-profitable-in-2021162075307076393.jpg", width=800)
st.title('Crypto Dashboard Group EA')
#Closing price over the time
st.header("1. Overview")
st.subheader('Crypto price over time')
st.line_chart(df['Adj Close'])


##Candle Plot
st.subheader('Candlestick Plot-Price')

def plot_candle_data():
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'], name = 'market data'))
    fig.update_layout(width=900)
    #title='Crypto price evolution',)
    st.plotly_chart(fig)

plot_candle_data()


#Volume traded over the time 
st.subheader('Crypto Volume traded over time')
st.line_chart(df['Volume'])

st.header("2. Technical Indicators")
# Plot MACD
st.subheader('Crypto Moving Average Convergence Divergence (MACD)')
st.area_chart(macd)

# Plot RSI
st.subheader('Crypto RSI ')
st.line_chart(rsi)

#Prediction 
st.subheader("3. Prediction")
# Data of recent days
#st.write('Recent data ')
#st.dataframe(df.tail(10))


# In[5]:


# preparing the data for Facebook-Prophet.
df.reset_index(inplace=True)
month = st.slider('Month of prediction:',1,12)
period = month * 30
data_pred = df[['Date','Close']]
data_pred=data_pred.rename(columns={"Date": "ds", "Close": "y"})

# code for facebook prophet prediction
m = Prophet(daily_seasonality = False, yearly_seasonality =False,weekly_seasonality =False,changepoint_prior_scale=0.5, interval_width=0.9)
#m = Prophet() 
m.fit(data_pred)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

#plot forecast
fig1 = plot_plotly(m, forecast)
if st.checkbox('Show forecast data'):
    st.subheader('forecast data')
    st.write(forecast)
st.plotly_chart(fig1)

#plot component wise forecast
st.write("Component wise forecast")
fig2 = m.plot_components(forecast)
st.write(fig2)


# In[6]:


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="download.xlsx">Download excel file</a>' # decode b'abc' => abc

st.markdown(get_table_download_link(df), unsafe_allow_html=True)
st.subheader('Authors')
st.write('**Adriana Gamboa** :sunglasses:' )
st.write('**Andreas Schneeweiss** :wink:')
st.write('**Debora Carreira** :stuck_out_tongue:')
st.write('**Mario Negas** :laughing:')
