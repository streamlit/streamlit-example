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
import matplotlib.gridspec as gridspec


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


def calc_rsi(df: pd.DataFrame, column: str, period: int) -> pd.Series:
    """Calculate the relative strength index (RSI) for a column in a Pandas DataFrame.
    
    Args:
        df: The Pandas DataFrame containing the data.
        column: The name of the column for which to calculate the RSI.
        period: The number of periods to use for the RSI calculation.
    
    Returns:
        A Pandas Series containing the RSI values.
    """
    # Calculate the difference between the current and previous values
    diff = df[column].diff()
    
    # Create two empty Pandas Series to store the gain and loss
    gain = pd.Series(index=diff.index)
    loss = pd.Series(index=diff.index)
    
    # Fill the gain and loss Series with the appropriate values
    gain[diff > 0] = diff[diff > 0]
    loss[diff < 0] = -diff[diff < 0]
    
    # Calculate the rolling average of the gain and loss
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    
    # Calculate the relative strength
    rs = avg_gain / avg_loss
    
    # Calculate the RSI
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def calc_macd(df: pd.DataFrame, column: str, fast_period: int, slow_period: int, signal_period: int) -> pd.DataFrame:
    """Calculate the moving average convergence divergence (MACD) for a column in a Pandas DataFrame.
    
    Args:
        df: The Pandas DataFrame containing the data.
        column: The name of the column for which to calculate the MACD.
        fast_period: The number of periods to use for the fast moving average.
        slow_period: The number of periods to use for the slow moving average.
        signal_period: The number of periods to use for the signal line.
    
    Returns:
        A Pandas DataFrame containing the MACD, MACD signal, and MACD histogram values.
    """
    # Calculate the fast and slow moving averages
    fast_ma = df[column].ewm(com=fast_period - 1, min_periods=fast_period).mean()
    slow_ma = df[column].ewm(com=slow_period - 1, min_periods=slow_period).mean()
    
    # Calculate the MACD
    macd = fast_ma - slow_ma
    
    # Calculate the MACD signal
    macd_signal = macd.ewm(com=signal_period - 1, min_periods=signal_period).mean()
    
    # Calculate the MACD histogram
    macd_hist = macd - macd_signal
    
    # Create a Pandas DataFrame to store the MACD, MACD signal, and MACD histogram values
    macd_df = pd.DataFrame({'MACD': macd, 'MACD signal': macd_signal, 'MACD histogram': macd_hist})
    
    return macd_df

# # Calculate the MACD values
# short_ema = data['Close'].ewm(span=12, adjust=False).mean()
# long_ema = data['Close'].ewm(span=26, adjust=False).mean()
# macd1 = short_ema - long_ema
# signal = macd1.ewm(span=9, adjust=False).mean()

fig = plt.figure(figsize=(12, 18))
gs = gridspec.GridSpec(nrows=4, ncols=1, height_ratios=[3, 1, 1, 1])

# Create the subplots using the grid specification
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax3 = fig.add_subplot(gs[2])
ax4 = fig.add_subplot(gs[3])

# Adjust the spacing between the subplots
fig.subplots_adjust(hspace=.5)

# Plot the results

ax1.fill_between(data.index, data['senkou_span_a'], data['senkou_span_b'], where=data['senkou_span_a'] >= data['senkou_span_b'], facecolor='green', alpha=0.25, interpolate=True)  # green fill for bullish trend 
ax1.fill_between(data.index, data['senkou_span_a'], data['senkou_span_b'], where=data['senkou_span_a'] < data['senkou_span_b'], facecolor='red', alpha=0.25, interpolate=True)  # red fill for bearish trend 
ax1.set_xlabel('Time')
ax1.set_ylabel('Price')
ax1.xaxis.set_major_locator(MinuteLocator (interval=30))
ax1.set_xlim(data.index.min(), data.index.max())

# Get the tick labels
tick_labels1 = ax1.get_xticklabels()

# Set the font size and style of the tick labels
for label in tick_labels1:
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
ax1.legend(fontsize=8, loc='upper left')


# Calculate the RSI of the 'Close' column of a Pandas DataFrame 'df'
rsi = calc_rsi(data, 'Close', 14)

# Plot the RSI on the first subplot
ax2.plot(data.index, rsi)
ax2.set_ylabel('RSI')

ax2.set_xlim(data.index.min(), data.index.max())

ax2.set_xlabel('Time')
ax2.xaxis.set_major_locator(MinuteLocator (interval=30))

#ax2.legend(fontsize=6)

# Get the tick labels
tick_labels2 = ax2.get_xticklabels()

# Set the font size and style of the tick labels
for label in tick_labels2:
    label.set_fontsize(12)
    label.set_fontstyle("italic")
    label.set_rotation(45)
    label.set_horizontalalignment('right')

# Calculate the MACD of the 'Close' column using a 12-period fast moving average, a 26-period slow moving average, and a 9-period signal line
macd_df = calc_macd(data, 'Close', 12, 26, 9)

# Create a new dataframe with the MACD and signal values
#macd_df1 = pd.DataFrame({'MACD': macd1, 'Signal': signal})

# Plot the MACD and MACD histogram values
ax3.plot(mac_df.index, macd_df['MACD'], label='MACD')
ax3.plot(macd_df['Signal'], label='MACD signal')
#ax3.bar(macd_df.index, macd_df['MACD histogram'], label='MACD histogram')

#ax3.plot(macd_df1)
ax3.fill_between(macd_df['MACD'], macd_df['Signal'], where=macd_df['MACD'] > macd_df['Signal'], facecolor='green', interpolate=True)
ax3.fill_between(macd_df['MACD'], macd_df['Signal'], where=macd_df['MACD'] < macd_df['Signal'], facecolor='red', interpolate=True)

ax3.set_xlabel('Time')
ax3.set_ylabel('MACD')
ax3.xaxis.set_major_locator(MinuteLocator (interval=30))

ax3.legend(fontsize=6, loc='upper left')

# Get the tick labels
tick_labels3 = ax3.get_xticklabels()

# Set the font size and style of the tick labels
for label in tick_labels3:
    label.set_fontsize(12)
    label.set_fontstyle("italic")
    label.set_rotation(45)
    label.set_horizontalalignment('right')
    
ax3.set_xlim(data.index.min(), data.index.max())
#ax3.xaxis.set_major_locator(MinuteLocator (interval=30))

# Plot the volume data on the new subplot
ax4.plot(data.index, data['Volume'], color='k', linestyle='-', linewidth=1)
ax4.set_ylabel('Volume of Option')

# Set the X axis limits to the minimum and maximum datetime values in the index
ax4.set_xlim(data.index.min(), data.index.max())

ax4.xaxis.set_major_locator(MinuteLocator (interval=30))

#ax4.legend(fontsize=6)

# Get the tick labels
tick_labels4 = ax4.get_xticklabels()

# Set the font size and style of the tick labels
for label in tick_labels4:
    label.set_fontsize(12)
    label.set_fontstyle("italic")
    label.set_rotation(45)
    label.set_horizontalalignment('right')


# Create a boolean mask that indicates where the 'volume' values are greater than 1500
mask = data['Volume'] > 1000

# Shade the region of the subplot where the mask is True
ax4.fill_between(data.index, data['Volume'], where=mask, alpha=0.25, color='purple')

#plt.show()

st.pyplot(fig)
st.write("Pricing Data from Option " + symbol)
data
st.write("RSI Data from Option " + symbol)
rsi
st.write("MACD Data from Option " + symbol)
macd_df1
