import streamlit as st
st.set_page_config(page_icon = ":rocket:", layout = "wide")

import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from matplotlib.dates import MinuteLocator, ConciseDateFormatter

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

# Convert the index to a column and keep only the hour and minute
data['time'] = pd.to_datetime(data.index, format='%H:%M')

# Set the 'time' column as the new index
data.set_index('time', inplace=True)

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

data = data.drop(columns=['Dividends', 'Stock Splits'])

# Create a new figure with the desired size
fig = plt.figure(figsize=(10, 8))

# Add subplots to the figure
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

# Create a subplot that takes up 25% of the figure height
#ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=1, fig=fig, height_ratios=[1, 3, 1])

# Create a subplot that takes up 50% of the figure height
#ax2 = plt.subplot2grid((3, 1), (1, 0), rowspan=1, fig=fig, height_ratios=[1, 3, 1])

# Create a subplot that takes up 25% of the figure height
#ax3 = plt.subplot2grid((3, 1), (2, 0), rowspan=1, fig=fig, height_ratios=[1, 3, 1])

# Plot the results

ax1.fill_between(data.index, data['senkou_span_a'], data['senkou_span_b'], where=data['senkou_span_a'] >= data['senkou_span_b'], facecolor='green', alpha=0.25, interpolate=True)  # green fill for bullish trend 
ax1.fill_between(data.index, data['senkou_span_a'], data['senkou_span_b'], where=data['senkou_span_a'] < data['senkou_span_b'], facecolor='red', alpha=0.25, interpolate=True)  # red fill for bearish trend 
ax1.set_xlabel('Time')
ax1.set_ylabel('Price')
ax1.xaxis.set_major_locator(MinuteLocator (interval=15))

#ax.xaxis.set_major_formatter(ConciseDateFormatter(ax.xaxis.get_major_locator())

# Get the tick labels
tick_labels = ax1.get_xticklabels()

# Set the font size and style of the tick labels
for label in tick_labels:
    label.set_fontsize(12)
    label.set_fontstyle("italic")
    label.set_rotation(45)
    label.set_horizontalalignment('right')

ax1.plot(data.index, data["Close"], label="Close", color='dimgrey', linewidth=1)
ax1.plot(data["tenkan_sen"], label="tenkan_sen" , color='blue', linewidth=0.75)
ax1.plot(data["kijun_sen"], label="kijun_sen" , color='saddlebrown', linewidth=0.75)
ax1.plot(data["senkou_span_a"], label="senkou_span_a" , color='limegreen', linewidth=0.75)
ax1.plot(data["senkou_span_b"], label="senkou_span_b" , color='red', linewidth=0.75)
ax1.plot(data["chikou_span"], label="chikou_span" , color='magenta', linewidth=0.75)
ax1.scatter(long_positions, data.loc[long_positions]["Close"], label="Buy", color='green')
ax1.scatter(short_positions, data.loc[short_positions]["Close"], label="Sell" , color='red')
plt.legend(fontsize=6)

# Plot the volume data on the new subplot
ax2.plot(data.index, data['Volume'], color='k', linestyle='-', linewidth=1)

# Set the X axis limits to the minimum and maximum datetime values in the index
#ax2.set_xlim(data.index.min(), data.index.max())

# Set the major tick intervals to 1 hour
ax2.xaxis.set_major_locator(mdates.HourLocator(interval=.25))

# Localize the time to EST
data.index = data.index.tz_localize('EST')

# Set the tick label format to display the time in EST
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=mdates.timezone('EST')))

# Set the tick label format to display the hour and minute
#ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

# Filter the data to only include volume above 1500
data_filtered = data[data['Volume'] > 1500]

# Plot the filtered data in green
ax2.plot(data_filtered.index, data_filtered['Volume'], linestyle='-', linewidth=1, color='green')

# Adjust the spacing between the subplots
fig.subplots_adjust(hspace=.5)

plt.show()

st.pyplot()
data
