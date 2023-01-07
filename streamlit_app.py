import streamlit as st
st.set_page_config(page_icon = ":rocket:", layout = "wide")

import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.ticker as ticker
from matplotlib.dates import MinuteLocator, ConciseDateFormatter

# Set the interval to 1 minute and the symbol to SPY
#interval = "1m"
#period = '1d'
#symbol = "SPY221223C00380000"

# Create a sidebar for user input
st.sidebar.header("Inputs")

# Add a text input for the interval
interval = st.sidebar.text_input("Interval", "1m")

# Add a text input for the period
period = st.sidebar.text_input("Period", "1d")

# Add a text input for the symbol
symbol = st.sidebar.text_input("Symbol", "SPY230106C00386000")

st.title('Ichimoku Cloud Indicator')
st.markdown("Interval: **{}**, Period: **{}**, Symbol: **{}**".format(interval, period, symbol))

# Connect to the TradeStation API and retrieve the price data for the specified symbol and interval
ticker = yf.Ticker(symbol)
data = ticker.history(period=period, interval=interval)

# Calculate the Ichimoku Cloud indicator using the data
data["tenkan_sen"] = data["High"].rolling(window=9).mean()
data["kijun_sen"] = data["Low"].rolling(window=26).mean()
data["senkou_span_a"] = (data["tenkan_sen"] + data["kijun_sen"]) / 2
data["senkou_span_b"] = data["Low"].rolling(window=52).mean()
data["chikou_span"] = data["Close"].shift(-26)

# Initialize empty lists to store the long and short positions
long_positions = []
short_positions = []

# Iterate through the data and determine the trading criteria for go long and go short positions
for index, row in data.iterrows():
    # Go long if the market is above the open and the chikou span is above the current price
    if row["Close"] > row["Open"] and row["chikou_span"] > row["Close"]:
        long_positions.append(index)
    # Go short if the market is below the open and the chikou span is below the current price
    elif row["Close"] < row["Open"] and row["chikou_span"] < row["Close"]:
        short_positions.append(index)

#data.insert(loc=1, column='TIME', value=pd.to_datetime(data.index,format='%H:%M')
data['TIME'] = pd.to_datetime(data.index)
data['TIME'] = data['TIME'].dt.strftime('%H:%M')
#time_data = data['TIME'] 
data = data.drop(columns=['Dividends', 'Stock Splits'])
# Plot the results
fig, ax = plt.subplots()
#ax.set_xlim(data.index)
ax.fill_between(data.index, data['senkou_span_a'], data['senkou_span_b'], where=data['senkou_span_a'] >= data['senkou_span_b'], facecolor='green', alpha=0.25, interpolate=True)  # green fill for bullish trend 
ax.fill_between(data.index, data['senkou_span_a'], data['senkou_span_b'], where=data['senkou_span_a'] < data['senkou_span_b'], facecolor='red', alpha=0.25, interpolate=True)  # red fill for bearish trend 
ax.set_xlabel('Time')
ax.set_ylabel('Price')
#ax.xaxis.set_major_locator(MinuteLocator (interval=15))
ax.xaxis.set_major_locator(ticker.MultipleLocator(15))
#ax.xaxis.set_major_formatter(ConciseDateFormatter(ax.xaxis.get_major_locator())

# Get the tick labels
tick_labels = ax.get_xticklabels()

# Set the font size and style of the tick labels
for label in tick_labels:
    label.set_fontsize(14)
    label.set_fontstyle("italic")
#for label in ax.get_xticklabels():
        #label.set_rotation(45)
        #label.set_horizontalalignment('right')
#ax.set_xticks(time_data.values)
#ax.set_xticklabels(labels = time_data.values, rotation=45, fontstyle='italic', color='black')
ax.plot(data["Close"], label="Close", color='dimgrey', linewidth=1)
ax.plot(data["tenkan_sen"], label="tenkan_sen" , color='blue', linewidth=0.75)
ax.plot(data["kijun_sen"], label="kijun_sen" , color='saddlebrown', linewidth=0.75)
ax.plot(data["senkou_span_a"], label="senkou_span_a" , color='limegreen', linewidth=0.75)
ax.plot(data["senkou_span_b"], label="senkou_span_b" , color='red', linewidth=0.75)
ax.plot(data["chikou_span"], label="chikou_span" , color='magenta', linewidth=0.75)
ax.scatter(long_positions, data.loc[long_positions]["Close"], label="Buy", color='green')
ax.scatter(short_positions, data.loc[short_positions]["Close"], label="Sell" , color='red')
plt.legend(fontsize=6)
plt.show()

st.pyplot()
data
