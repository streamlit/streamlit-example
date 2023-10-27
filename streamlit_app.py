#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 11:57:49 2023

@author: jak
"""


import streamlit as st
from streamlit import components
from streamlit.components import v1 as components
import yfinance as yf
import os


# Sidebar navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home", "Equity Screener", "Crypto Screener", "Comparative Screener and Picker","Option Screener","Index/Fund Screener","Quantitative Modelling", "Portfolio Tracker"])



def fetch_graph_data_USIRYY(symbol, interval="D"):
    # Basic TradingView widget template
    tradingview_embed_template = """
    <<!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
    <div id="tradingview_ee9d3"></div>
    <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget(
        {{
            "width": 1200,
            "height": 600,
            "symbol": "ECONOMICS:USIRYY",
            "interval": "D",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "enable_publishing": false,
            "allow_symbol_change": true,
            "container_id": "tradingview_ee9d3"
            }}
        );
    </script>
    </div>
    <!-- TradingView Widget END -->
    """

    # Generate a unique container ID for each symbol to prevent conflicts
    container_id = symbol.lower() + "_" + interval.lower()

    # Format the embed template with the given symbol and interval
    tradingview_embed_code = tradingview_embed_template.format(
        symbol_name=symbol,
        graph_interval=interval,
        container_id=container_id
    )

    # Embed the widget in Streamlit
    st.components.v1.html(tradingview_embed_code, height=600, scrolling=True)

import matplotlib.pyplot as plt
import requests
import pandas as pd
from datetime import datetime


from bs4 import BeautifulSoup

def scrape_tradingview(ticker):
    url = f"https://www.tradingview.com/symbols/{ticker}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return f"Failed to fetch data for {ticker}. HTTP Status Code: {response.status_code}"
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Just as a starting point, let's try to find the price data in the soup. 
    # This might not work immediately and might need more refined searching.
    price_tag = soup.find("div", class_="tv-symbol-header__price-value")
    price = price_tag.text if price_tag else "Price not found"
    
    return price


# 1. Fetch Prices:
def fetch_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="1d")["Close"].iloc[0]





if selection == "Home":
    st.title('Investment Analysis Dashboard')
    st.write("Choose an option from the sidebar to begin.")
    
    
     
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Construct the URL dynamically
    URL = f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month={current_year}{current_month:02}"

    response2 = requests.get(URL)
    soup = BeautifulSoup(response2.content, 'html.parser')

    # 2. Extract table data
    table = soup.find_all('table')[-1] # Assuming the desired table is the last one on the page
    dfs = pd.read_html(str(table))
    df = dfs[0]
    
    columns_to_keep = ["Date", "1 Mo", "2 Mo", "3 Mo", "4 Mo", "6 Mo", "1 Yr", "2 Yr", "3 Yr", "5 Yr", "7 Yr", "10 Yr", "20 Yr", "30 Yr"]

    # Filter the dataframe
    df_filtered = df[columns_to_keep]

    # 3. Display table data in Streamlit
    st.table(df_filtered)

    

    maturities = ['1 Mo', '2 Mo', '3 Mo', '4 Mo', '6 Mo', '1 Yr', '2 Yr', '3 Yr', '5 Yr', '7 Yr', '10 Yr', '20 Yr', '30 Yr']
    most_recent_date = df_filtered['Date'].max()

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#0E1117')  # Set figure background color
    ax.set_facecolor('#0E1117')  # Set plot background color

    # Plot each yield curve
    for index, row in df_filtered.iterrows():
        alpha_value = 0.2 if row['Date'] != most_recent_date else 1
        color_value = 'white' if row['Date'] == most_recent_date else 'lightgray'
        ax.plot(maturities, row[maturities].values, label=row['Date'], alpha=alpha_value, color=color_value)

    # Adjust y-axis
    max_yield = df_filtered[maturities].values.max()
    ax.set_ylim(0, max_yield + 0.5)  # Added a little buffer for clarity

    # Add title, labels, and legend
    ax.set_title('US Treasury Yield Curve', color='white')
    ax.set_xlabel('Maturity', color='white')
    ax.set_ylabel('Yield (%)', color='white')
    ax.tick_params(colors='white')
    ax.legend()
    
    # Display the plot in Streamlit
    st.pyplot(fig)
    
    
    
    
    
    SPY_price = fetch_price("SPY")
    QQQ_price = fetch_price("QQQ")
    TMF_price = fetch_price("TMF")



    # 2. Display Prices:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader(f"SPY Price: ${SPY_price:.2f}")
    with col2:
        st.subheader(f"QQQ Price: ${QQQ_price:.2f}")
    with col3:
        st.subheader(f"TMF Price: ${TMF_price:.2f}")


    # 3. Fetch Graph Data:
    def fetch_graph_data(ticker, period="1d"):
        stock = yf.Ticker(ticker)
        return stock.history(period=period)



    SPY_daily = fetch_graph_data("SPY")
    QQQ_daily = fetch_graph_data("QQQ")
    TMF_daily = fetch_graph_data("TMF")


    SPY_yearly = fetch_graph_data("SPY", "1y")
    QQQ_yearly = fetch_graph_data("QQQ", "1y")
    TMF_yearly = fetch_graph_data("TMF", "1y")


    # 4. Display Graphs:
    col1, col2, col3 = st.columns(3)  # Added a fourth column for USIRYY
    with col1:
        st.line_chart(SPY_daily["Close"],use_container_width=True)
        st.line_chart(SPY_yearly["Close"],use_container_width=True)
    with col2:
        st.line_chart(QQQ_daily["Close"],use_container_width=True)
        st.line_chart(QQQ_yearly["Close"],use_container_width=True)
    with col3:
        st.line_chart(TMF_daily["Close"],use_container_width=True)
        st.line_chart(TMF_yearly["Close"],use_container_width=True)


    USIRYY_daily = fetch_graph_data_USIRYY("ECONOMICS:USIRYY")


   

    







import numpy as np


import datetime
@st.cache_data
def fetch_equity_data(ticker: str, start_date: str = '2000-01-01', end_date: str = None) -> 'pd.DataFrame':
    if end_date is None:
        end_date = datetime.date.today().strftime('%Y-%m-%d')

    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            st.warning(f"No data found for {ticker} between {start_date} and {end_date}")
            return None
        return data

    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None




import cryptocompare
import pandas as pd

@st.cache_data
def fetch_risk_free_rate():
    # Fetch the data for the 10-year Treasury rate
    ten_year_treasury = yf.Ticker("^TNX")
    
    # Get the historical data (we'll just use the last data point)
    history = ten_year_treasury.history(period="1d")

    if not history.empty:
        return history["Close"].iloc[0]
    else:
        # If the current day's data is missing, fetch the latest available data
        history = ten_year_treasury.history(period="7d")  # fetch data for the past week
        if not history.empty:
            return history["Close"].iloc[-1]  # return the most recent available data
        else:
            print("Failed to fetch risk-free rate for the past week. Using default value.")
            return 0.045  # Return a default risk-free rate if all attempts fail

risk_free = fetch_risk_free_rate()
st.write(f"The 10-year U.S. Treasury rate (risk-free rate) is: {risk_free:.2f}%.")
risk_free = risk_free / 100









@st.cache_data
def fetch_crypto_data(crypto_symbol, currency="USD", limit=2000):
    """
    Fetch crypto data using the cryptocompare API.
    
    Parameters:
    - crypto_symbol (str): The symbol for the cryptocurrency (e.g., 'BTC' for Bitcoin).
    - currency (str): The fiat currency to compare against (default is 'USD').
    - limit (int): Number of days of historical data to retrieve.
    
    Returns:
    - DataFrame: A pandas DataFrame containing historical data.
    """
    data = cryptocompare.get_historical_price_day(
        crypto_symbol, 
        currency=currency, 
        limit=limit, 
        toTs=pd.Timestamp.now()
    )
    
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    
    return df[['close', 'high', 'low', 'open', 'volumeto', 'volumefrom']]


def fetch_equity_data_safe(ticker, start_date=None, end_date=None):
    # If start_date and end_date are not provided, fetch all available data
    # Otherwise, fetch data for the given date range
    if not isinstance(ticker, str):
        st.error(f"Ticker is not a string. Received type: {type(ticker)}")
    return None

    ticker = str(ticker)

    try:
        if start_date and end_date:
            data = yf.download(ticker, start=start_date, end=end_date)
        else:
            data = yf.download(ticker)  # This fetches all available data
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None


def fetch_crypto_data_safe(ticker):
    try:
        data = fetch_crypto_data(ticker)
        return data
    except Exception as e:
        st.error(f"An error occurred when fetching data for {ticker}. Error: {e}")
        return None



    # Technical Indicators:

def moving_average(data, window):
    """Calculate Moving Average"""
    return data.rolling(window=window).mean()
    
def rsi(data, window=14):
    """Calculate Relative Strength Index (RSI)"""
    delta = data.diff()
    up = delta.where(delta > 0, 0)
    down = -delta.where(delta < 0, 0)
    avg_gain = up.rolling(window=window, min_periods=1).mean()
    avg_loss = down.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def macd(data, short_window=12, long_window=26, signal_window=9):
    """Calculate Moving Average Convergence Divergence (MACD) and Signal line"""
    short_ema = data.ewm(span=short_window, adjust=False).mean()
    long_ema = data.ewm(span=long_window, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
    return macd_line, signal_line

# Quantitative Metrics:
    

def fetch_beta(ticker):
    equity = yf.Ticker(ticker)
    try:
        return equity.info['beta']
    except KeyError:
        return None

    
from scipy.stats import skew, kurtosis


def mean_price(data):
    """Calculate the mean price."""
    return float(data['Close'].mean())

def median_price(data):
    """Calculate the median price."""
    return float(data['Close'].median())

def standard_deviation(data):
    """Calculate the standard deviation."""
    return float(data['Close'].std())

def variance(data):
    """Calculate the variance."""
    return float(data['Close'].var())

def price_skewness(data):
    """Calculate the skewness."""
    return float(skew(data['Close']))

def price_kurtosis(data):
    """Calculate the kurtosis."""
    return float(kurtosis(data['Close']))


def calculate_annualized_return(data):
    returns = data['Close'].pct_change().dropna()
    annualized_return = (1 + returns.mean())**252 - 1
    return annualized_return

def calculate_annualized_volatility(data):
    returns = data['Close'].pct_change().dropna()
    annualized_volatility = returns.std() * np.sqrt(252)
    return annualized_volatility

def sharpe_ratio(data, risk_free):  # assuming a default risk-free rate of 1%
    return_ratio = calculate_annualized_return(data) - risk_free
    sharpe_ratio_calc = return_ratio / calculate_annualized_volatility(data)
    return sharpe_ratio_calc


# Key Ratios:
    
@st.cache_data
def financial_metrics(ticker):
    equity = yf.Ticker(ticker)


    try:
        recommendationKey = equity.info['recommendationKey']
    except:
        recommendationKey = None
        
    # Debt-to-Equity Ratio
    try:
        debt_to_equity = equity.info['debtToEquity']
    except:
        debt_to_equity = None

    # Current Ratio
    try:
        current_ratio = equity.info['currentRatio']
    except:
        current_ratio = None


    # Earnings Per Share
    try:
        trailingEps = equity.info['trailingEps']
    except:
        trailingEps = None
    try:
        forwardEps = equity.info['forwardEps']
    except:
        forwardEps = None

    return {
        'Recommendation': recommendationKey,
        'Debt-to-Equity Ratio': debt_to_equity,
        'Current Ratio': current_ratio,
        'Trailing EPS': trailingEps,
        'Forward EPS': forwardEps
    }


if 'total_constituents' not in st.session_state:
    st.session_state.total_constituents = 0
    st.session_state.processed_constituents = 0


import re
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

@st.cache_data
def get_constituents(etf_ticker):
    url = f"https://www.zacks.com/funds/etf/{etf_ticker}/holding"
    response = requests.get(url, headers=HEADERS)  # set a 10-second timeout
    if response.status_code == 200:
        return extract_etf_holdings(response.text)
    else:
        return None, 0

    
    
def extract_etf_holdings(html_content, _progress_callback=None):
    pattern = re.compile(r'etf_holdings.formatted_data = (\[.*?\]);', re.DOTALL)
    match = pattern.search(html_content)
    
    if not match:
        return None

    holdings_data = json.loads(match.group(1))
    constituents = []
    
    
    
    for index, item in enumerate(holdings_data):
       
        symbol_match = re.search(r'rel="(\w+)"', item[1])
        if not symbol_match:
            continue
        symbol = symbol_match.group(1)
        
        
        if not isinstance(symbol, str):  # Ensure that symbol is a string
            print(f"Unexpected symbol format for {symbol}. Skipping...")
            continue
        
        # Try fetching additional data from Yahoo Finance
        try:
            currentPrice = constituentPrice(symbol)
            pe_ratio = get_pe_ratio(symbol)
            recommendation = sentiment(symbol)
            targetMeanPrice = targetPrice(symbol)

            # Fetch financial data and calculate DCF valuation
            financial_data = fetch_financial_data(symbol)
            wacc = get_wacc(symbol)
            fcfs = get_free_cash_flow(symbol)
            dcf_valuation, growth_rate = calculate_dcf(fcfs, symbol, wacc)
        
            # Fetch additional data to convert DCF valuation to stock price target
            stock = yf.Ticker(symbol)
            total_debt = stock.info.get('totalDebt', 0)
            cash_and_equivalents = stock.balance_sheet.loc['Cash And Cash Equivalents'].iloc[0]
            total_shares = stock.info.get('sharesOutstanding', 1)  # default to 1 to prevent division by zero
            

            # Convert DCF valuation to stock price target
            stock_price_target = dcf_to_stock_price_target(dcf_valuation, total_debt, cash_and_equivalents, total_shares)
       
            # Calculate the percentage difference
            if currentPrice and targetMeanPrice:
                percentage_difference = ((targetMeanPrice - currentPrice) / currentPrice) * 100
            else:
                percentage_difference = None
                
                # Calculate DCF-based percentage difference
            if currentPrice and stock_price_target != 'NA':
                dcf_percentage_difference = ((stock_price_target - currentPrice) / currentPrice) * 100
            else:
                dcf_percentage_difference = None

            data = {
                "Symbol": symbol,
                "Shares": item[2],
                "Weight(%)": item[3],
                "52 Wk Change(%)": item[4],
                "P/E Ratio": pe_ratio,
                "Recommendation": recommendation,
                "Current Price": currentPrice,
                "Analyst Target": targetMeanPrice,
                "Target % Difference": percentage_difference,
                "DCF Stock Price": stock_price_target,
                "DCF % Difference": dcf_percentage_difference
            }
            constituents.append(data)
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data for {symbol} due to {e}. Skipping...")
            continue  # skip to the next ticker
            
        
    return constituents




def get_fund_details(etf_ticker):
    # Fetch data using yfinance
    ticker = yf.Ticker(etf_ticker)
    history = ticker.history(period="1d")

    # Extract fund name
    fund_name = ticker.info.get("shortName", "N/A")

    # Extract daily return
    if not history.empty:
        today_close = history.iloc[0]['Close']
        prev_close = ticker.info.get("previousClose", today_close)
        daily_return = ((today_close - prev_close) / prev_close) * 100  # in percentage
    else:
        daily_return = "N/A"

    
    # Extract 52-week (1 year) return
    history_last_year = ticker.history(period="1y")
    if not history_last_year.empty:
        close_one_year_ago = history_last_year.iloc[0]['Close']
        fifty_two_week_return = ((today_close - close_one_year_ago) / close_one_year_ago) * 100  # in percentage
    else:
        fifty_two_week_return = "N/A"

    return fund_name, daily_return, fifty_two_week_return


def get_pe_ratio(ticker):
    stock = yf.Ticker(ticker)
    pe_ratio = stock.info.get('trailingPE', None)
    return pe_ratio


def sentiment(ticker):
    equity = yf.Ticker(ticker)
    try:
        recommendationKey = equity.info['recommendationKey']
    except:
        recommendationKey = None
    return recommendationKey


def constituentPrice(ticker):
    equity = yf.Ticker(ticker)
    try:
        return equity.info['currentPrice']
    except KeyError:
        try:
            return equity.info['regularMarketPrice']
        except KeyError:
            try:
                return equity.history(period="1d")["Close"].iloc[0]
            except:
                st.warning("NA")
                return None
    

def targetPrice(ticker):
    equity = yf.Ticker(ticker)
    targetMeanPrice = equity.info.get('targetMeanPrice')
    return targetMeanPrice


perpetual_growth_rate = 0.03  # 3% growth rate

def fetch_financial_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.financials.transpose()

def calculate_cagr(end_value, start_value, periods):
    return (end_value/start_value)**(1/periods)-1

def mean_growth_rate(values):
    if len(values) < 2:
        return None
    
    growth_rates = [(values[i] - values[i-1]) / values[i-1] for i in range(1, len(values))]
    return sum(growth_rates) / len(growth_rates)




def get_wacc(ticker):
    stock = yf.Ticker(ticker)

    if 'Interest Expense' in stock.financials.index:
        interest_expense = stock.financials.loc['Interest Expense'].iloc[0]  # get the most recent year's value
    else:
        interest_expense = 0

    total_debt = stock.info.get('totalDebt', 1)

    beta = stock.info.get('beta', 1)

    market_cap = stock.info.get('marketCap', 1)

    rf = risk_free

    rm = 0.08  # Market return

    re = rf.real + beta.real * (rm.real - rf.real)

    rd = interest_expense / total_debt if abs(total_debt) > 1e-9 else 0

    wacc = (market_cap / (market_cap + total_debt)) * re + (total_debt / (market_cap + total_debt)) * rd.real

    return wacc

@st.cache_data
def get_free_cash_flow(ticker_symbol):
    if not isinstance(ticker_symbol, str):
        print(f"Expected ticker symbol as string but got {type(ticker_symbol)} instead.")
        return None

    ticker = yf.Ticker(ticker_symbol)
    cash_flow_df = ticker.cashflow

    if cash_flow_df is None:
        print(f"Failed to fetch cash flow data for {ticker_symbol}")
        return None

    if "Free Cash Flow" in cash_flow_df.index:
        free_cash_flow = cash_flow_df.loc["Free Cash Flow"].tolist()  # Convert Series to list
        return free_cash_flow
    else:
        print(f"'Free Cash Flow' not found in the cash flow data for {ticker_symbol}")
        return None


@st.cache_data
def calculate_dcf(fcfs, ticker, wacc, n_years=5):
    dcf_valuation = 0
    growth_rate = 0

    # Check that the FCFs are a list and have enough data
    if not fcfs or len(fcfs) < 2:
        print(f"Insufficient FCF data for {ticker}.")
        return dcf_valuation, growth_rate

    fcf_latest = fcfs[0]
    fcf_earliest = fcfs[-1]

    if fcf_earliest > 0:
        growth_rate = calculate_cagr(fcf_latest, fcf_earliest, 4)
    elif fcf_earliest < 0 and fcf_latest < 0:
        growth_rate = (fcf_earliest - fcf_latest) / fcf_earliest
    else:
        growth_rate = mean_growth_rate(fcfs)



    # Project FCF for n_years using the calculated growth rate
    projected_fcfs = [fcf_latest * (1 + growth_rate.real)**i for i in range(1, n_years)]
    
    # Calculate Terminal Value at the end of the forecast period
    terminal_value = (projected_fcfs[-1] * (1 + perpetual_growth_rate.real)) / (wacc.real - perpetual_growth_rate.real)
    
    # Discount projected FCFs and Terminal Value
    discounted_fcfs = [fcf / (1 + wacc.real)**i for i, fcf in enumerate(projected_fcfs, start=1)]
    discounted_terminal_value = terminal_value / (1 + wacc.real)**n_years
    
    # Calculate the intrinsic value
    intrinsic_value = sum(discounted_fcfs) + discounted_terminal_value
    
    return intrinsic_value, growth_rate




def dcf_to_stock_price_target(dcf_valuation, total_debt, cash_and_equivalents, total_shares):
    equity_value = dcf_valuation - total_debt + cash_and_equivalents
    stock_price_target = equity_value / total_shares

    # Check if stock_price_target is negative and return 'NA' if it is
    if stock_price_target < 0:
        return 'NA'
    else:
        return stock_price_target

@st.cache_data
def fetch_dcf_parameters_for_ticker(ticker):
    try:
        # Assuming you have already imported yfinance and fetched the stock data:
        # stock = yf.Ticker(ticker)
        stock = yf.Ticker(ticker)
        
        # Fetch Interest Expense
        if 'Interest Expense' in stock.financials.index:
            interest_expense = stock.financials.loc['Interest Expense'].iloc[0]  # get the most recent year's value
        else:
            interest_expense = 0

        # Fetch Total Debt
        total_debt = stock.info.get('totalDebt', 1)

        # Fetch Beta
        beta = stock.info.get('beta', 1)

        # Fetch Market Cap (Market Value of Equity)
        market_value_of_equity = stock.info.get('marketCap', 1)

        # Set the Risk Free rate and Market Return
        market_return = 0.08  # Market return

        # Calculate Cost of Equity (re)
        cost_of_equity = risk_free + beta * (market_return - risk_free)

        # Calculate Cost of Debt (rd)
        cost_of_debt = interest_expense / total_debt if abs(total_debt) > 1e-9 else 0

        # Fetching WACC and FCF
        wacc = get_wacc(ticker)
        fcfs = get_free_cash_flow(ticker)

        # Calculating DCF
        dcf_valuation, growth_rate = calculate_dcf(fcfs, ticker, wacc)

        # Projecting Free Cash Flows for next 5 years
        projected_fcfs = [fcfs[0] * (1 + growth_rate.real)**i for i in range(1, 6)]

        # Calculating Terminal Value at the end of the forecast period
        terminal_value = (projected_fcfs[-1] * (1 + perpetual_growth_rate.real)) / (wacc.real - perpetual_growth_rate.real)

        # Discount projected FCFs and Terminal Value
        discounted_fcfs = [fcf / (1 + wacc.real)**i for i, fcf in enumerate(projected_fcfs, start=1)]
        discounted_terminal_value = terminal_value / (1 + wacc.real)**5

        # Calculating the intrinsic value
        intrinsic_value = sum(discounted_fcfs) + discounted_terminal_value
        
        
        cash_and_equivalents = stock.balance_sheet.loc['Cash And Cash Equivalents'].iloc[0]
        total_shares = stock.info.get('sharesOutstanding', 1)
        equity_value = dcf_valuation - total_debt + cash_and_equivalents
        stock_price_target = equity_value / total_shares

        # Calculate Weight of Debt and Weight of Equity
        weight_of_debt = total_debt / (total_debt + market_value_of_equity)
        weight_of_equity = 1 - weight_of_debt

        return {
            "Risk Free": risk_free,
            "Market Return": market_return,
            "Beta": beta,
            "Interest Expense": interest_expense,
            "Total Debt": total_debt,
            "Cost of Debt": cost_of_debt,
            "Market Value of Equity": market_value_of_equity,
            "Cost of Equity": cost_of_equity,
            "Weight of Debt": weight_of_debt,
            "Weight of Equity": weight_of_equity,
            "Growth Rate": growth_rate,
            "Projected Free Cash Flows": projected_fcfs,
            "Terminal Value": terminal_value,
            "Discounted Free Cash Flows": discounted_fcfs,
            "Discounted Terminal Value": discounted_terminal_value,
            "Intrinsic Value": intrinsic_value,
            "Equity Value": equity_value,
            "WACC": wacc,
            "Cash and Cash Equivalents": cash_and_equivalents,
            "Shares Outstanding": total_shares,
            "DCF Stock Price": stock_price_target
            
        }

    except Exception as e:
        print(f"Failed to fetch DCF parameters for {ticker} due to {e}.")
        return None



def get_dcf_details_for_ticker(selected_ticker):
    # Fetch the necessary DCF parameters
    dcf_parameters = fetch_dcf_parameters_for_ticker(selected_ticker)  
    return dcf_parameters




def dcf_to_markdown_table(dcf_parameters,fcfs):
    # Create a markdown string for the table
    markdown_string = ""

    # Add title
    markdown_string += "### Discounted Cash Flow Analysis\n\n"


    def table_row(label, value):
        return f"| {label:30} | {value:20} |\n"

    # Add the fetched FCF section
    markdown_string += "| Year             | Fetched FCF       |\n"
    markdown_string += "|------------------|-------------------|\n"
    for i in range(4):  # Assuming you have 4 years of data
        fetched_index = -(i + 1)
        fetched = fcfs[fetched_index] if abs(fetched_index) <= len(fcfs) else '-'
        markdown_string += f"| Year {i+1}         | ${fetched:,.2f}           |\n"
    
    markdown_string += "\n"

    # Add the first section (Risk Free, Market Return, Beta)
    markdown_string += table_row("Growth Rate", f"{dcf_parameters['Growth Rate']:.2%}")
    markdown_string += table_row("Risk Free", f"{dcf_parameters['Risk Free']:.2%}")
    markdown_string += table_row("Market Return", f"{dcf_parameters['Market Return']:.2%}")
    markdown_string += table_row("Beta", f"{dcf_parameters['Beta']:.2f}")
    
    markdown_string += "\n"

    # Add the Interest section (Interest Expense, Total Debt, Cost of Debt)
    markdown_string += table_row("Interest Expense", f"${dcf_parameters['Interest Expense']:,.2f}")
    markdown_string += table_row("Total Debt", f"${dcf_parameters['Total Debt']:,.2f}")
    markdown_string += table_row("Cost of Debt", f"{dcf_parameters['Cost of Debt']:.2%}")
    
    markdown_string += "\n"

    # Add the Equity section (Market Value of Equity, Cost of Equity)
    markdown_string += table_row("Market Value of Equity", f"${dcf_parameters['Market Value of Equity']:,.2f}")
    markdown_string += table_row("Cost of Equity", f"{dcf_parameters['Cost of Equity']:.2%}")
    
    markdown_string += "\n"

    # Add the Weights section (Weight of Debt, Weight of Equity)
    markdown_string += table_row("Weight of Debt", f"{dcf_parameters['Weight of Debt']:.2%}")
    markdown_string += table_row("Weight of Equity", f"{dcf_parameters['Weight of Equity']:.2%}")
    markdown_string += table_row("WACC", f"{dcf_parameters['wacc']:.2%}")
    
    markdown_string += "\n"
    
    # Add the projected FCF section
    markdown_string += "| Year             | Projected FCF       | Discounted FCF      |\n"
    markdown_string += "|------------------|---------------------|---------------------|\n"
    for i, (projected, discounted) in enumerate(zip(dcf_parameters['Projected Free Cash Flows'], dcf_parameters['Discounted Free Cash Flows']), start=1):
        markdown_string += f"| Year {i:2}         | ${projected:,.2f}           | ${discounted:,.2f}          |\n"
    
    markdown_string += "\n"

    # Add the Terminal Value section
    markdown_string += table_row("Terminal Value", f"${dcf_parameters['Terminal Value']:,.2f}")
    markdown_string += table_row("Discounted Terminal Value", f"${dcf_parameters['Discounted Terminal Value']:,.2f}")

    # Add the Intrinsic Value, Cash and Cash Equivalents, Equity Value sections
    markdown_string += table_row("Intrinsic Value", f"${dcf_parameters['Intrinsic Value']:,.2f}")
    markdown_string += table_row("Cash and Cash Equivalents", f"${dcf_parameters['Cash and Cash Equivalents']:,.2f}")
    markdown_string += table_row("Equity Value", f"${dcf_parameters['Equity Value']:,.2f}")
    
    markdown_string += "\n"

    # Add the Shares Outstanding and DCF Stock Price sections
    markdown_string += table_row("Shares Outstanding", f"{dcf_parameters['Shares Outstanding']:,.2f}")
    markdown_string += table_row("DCF Stock Price", f"${dcf_parameters['DCF Stock Price']:,.2f}")

    return markdown_string




#Monte Carlo Simulations
def monte_carlo_forecast(ticker, num_simulations=1000, num_days=252, data=None):
    if data is None:
        data = fetch_equity_data(ticker)
        
    if isinstance(data, pd.DataFrame):
        prices = data['Close']
        last_price = prices[-1]
    else:
        return None 

    log_returns = np.log(1 + prices.pct_change())
    u = log_returns.mean()
    var = log_returns.var()
    drift = u - (0.5 * var)
    stdev = log_returns.std()

    daily_returns = np.exp(drift + stdev * np.random.normal(0, 1, (num_days, num_simulations)))

    price_paths = np.zeros_like(daily_returns)
    price_paths[0] = prices.iloc[-1]

    for t in range(1, num_days):
        price_paths[t] = price_paths[t-1] * daily_returns[t]

    # Calculate results
    simulations = pd.DataFrame(price_paths)
    probability_positive_return = (price_paths[-1] > last_price).sum() / num_simulations
    mean_return = price_paths[-1].mean() - last_price
    expected_return = ((price_paths[-1].mean() / last_price) - 1) * 100
    expected_dollar_return = price_paths[-1].mean() - last_price


    results = {
        "Probability Positive Return": probability_positive_return,
        "Mean Return": mean_return,
        "Expected Return %": expected_return,
        "Expected Dollar Return with the purchase of 1 share": expected_dollar_return,
        "Simulations": simulations
    }
    
    return results



import plotly.graph_objs as go

def plot_monte_carlo(ticker):
    results = monte_carlo_forecast(ticker)
    simulations = results["Simulations"]
    
    # Calculate the percentiles
    percentiles_to_plot = [10, 25, 50, 75, 90]
    percentile_paths = {}
    for percentile in percentiles_to_plot:
        percentile_paths[percentile] = np.percentile(simulations, percentile, axis=1)

    # Plotting
    fig = go.Figure()

    colors = {
        10: '#1f77b4',
        25: '#ff7f0e',
        50: '#2ca02c',
        75: '#d62728',
        90: '#9467bd'
    }

    for percentile, path in percentile_paths.items():
        fig.add_trace(go.Scatter(y=path, mode='lines', line=dict(width=2, color=colors[percentile]), name=f'{percentile}th Percentile'))

    fig.update_layout(title=f"Monte Carlo Simulation Percentile Paths for {ticker}",
                      xaxis_title="Days",
                      yaxis_title="Price",
                      template="plotly_dark")
    return fig






#LSTM Model

from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

def get_data(ticker):
    df = yf.download(ticker, period="20y")
    return df['Close'].values.reshape(-1, 1)

def create_dataset(data, timestep):
    X, y = [], []
    for i in range(len(data) - timestep):
        X.append(data[i:i + timestep])
        y.append(data[i + timestep])
    return np.array(X), np.array(y)

def predict_next_t_days(model, data, t, timestep, scaler):
    last_sequence = data[-timestep:]
    predictions = []
    for _ in range(t):
        prediction = model.predict(last_sequence.reshape(1, timestep, 1))
        predictions.append(prediction[0][0])
        last_sequence = np.append(last_sequence[1:], prediction, axis=0)
    return scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

def train_model_with_progress(model, X_train, y_train, epochs=100, batch_size=32):
    progress_bar = st.progress(0)
    for epoch in range(epochs):
        model.fit(X_train, y_train, epochs=1, batch_size=batch_size, verbose=0)
        progress = (epoch + 1) / epochs
        progress_bar.progress(progress)
    progress_bar.empty()

def create_model(timestep):
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(units=50, return_sequences=True, input_shape=(timestep, 1)),
        tf.keras.layers.LSTM(units=50),
        tf.keras.layers.Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model






import pickle

# File to save the serialized portfolio
PORTFOLIO_FILE = 'portfolio.pkl'

def save_portfolio(portfolio):
    """Serialize and save the portfolio to a file."""
    with open(PORTFOLIO_FILE, 'wb') as file:
        pickle.dump(portfolio, file)

def load_portfolio():
    """Load and deserialize the portfolio from a file."""
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, 'rb') as file:
            return pickle.load(file)
    return []


def remove_transaction(ticker, transaction_index):
 """Remove a transaction from the portfolio based on ticker and transaction index."""
 for holding in st.session_state.portfolio:
     if holding['ticker'] == ticker:
         del holding['transactions'][transaction_index]
         if not holding['transactions']:  # If no more transactions for the ticker
             st.session_state.portfolio.remove(holding)
             break

def display_remove_table():
    """Display a table of transactions with removal options."""
    
    # Loop through each holding and its transactions
    for holding in st.session_state.portfolio:
        ticker = holding['ticker']
        st.write(f"Transactions for {ticker}")
        
        # Display transactions for the current ticker
        for index, transaction in enumerate(holding['transactions']):
            details = f"Date: {transaction['purchase_date']} | Quantity: {transaction['quantity']} | Price: {transaction['purchase_price']}"
            remove_button_key = f"remove_{ticker}_{index}"
            
            # Display each transaction and its remove button
            col1, col2 = st.columns(2)
            with col1:
                st.write(details)
            with col2:
                if st.button("Remove", key=remove_button_key):
                    remove_transaction(ticker, index)
                    st.experimental_rerun()  # Refresh the app after removal
                
   



# Main area placeholders



if selection == "Equity Screener":
    st.title("Equity Screener")

    import altair as alt

    ticker = st.text_input("Enter ticker for analysis:").upper()
    
    

    def get_live_price(ticker):
        equity = yf.Ticker(ticker)
        try:
            return equity.info['currentPrice']
        except KeyError:
            try:
                return equity.info['regularMarketPrice']
            except KeyError:
                try:
                    return equity.history(period="1d")["Close"].iloc[0]
                except:
                    st.warning(f"Unable to fetch live price for {ticker}. Please try another ticker or check the ticker's validity.")
                    return None



    def get_returns(ticker):
        today = datetime.date.today()
        equity = yf.Ticker(ticker)
        prices = equity.history(period="1y")["Close"]

        one_day_return = ((prices[-1] - prices[-2]) / prices[-2]) * 100
        five_day_return = ((prices[-1] - prices[-5]) / prices[-5]) * 100
        one_month_return = ((prices[-1] - prices[-30]) / prices[-30]) * 100
        three_month_return = ((prices[-1] - prices[-90]) / prices[-90]) * 100
        six_month_return = ((prices[-1] - prices[-180]) / prices[-180]) * 100
        one_year_return = ((prices[-1] - prices[0]) / prices[0]) * 100
        ytd_start_price = prices[today.replace(month=1, day=1):].iloc[0]
        ytd_return = ((prices[-1] - ytd_start_price) / ytd_start_price) * 100

        returns = {
         "1 Day": f"{one_day_return:.2f}%",
         "5 Days": f"{five_day_return:.2f}%",
         "1 Month": f"{one_month_return:.2f}%",
         "3 Months": f"{three_month_return:.2f}%",
         "6 Months": f"{six_month_return:.2f}%",
         "1 Year": f"{one_year_return:.2f}%",
         "YTD": f"{ytd_return:.2f}%"
    }

        # Fetch additional information
        equity_info = equity.info
        fifty_two_week_high = equity_info.get('fiftyTwoWeekHigh', 'N/A')
        fifty_two_week_low = equity_info.get('fiftyTwoWeekLow', 'N/A')
        all_time_high = equity_info.get('dayHigh', 'N/A')  # Assuming this represents the all-time high

        returns["52-Week High"] = fifty_two_week_high
        returns["52-Week Low"] = fifty_two_week_low
        returns["All-Time High"] = all_time_high


        return returns

  
    if ticker:
        live_price = get_live_price(ticker)
        st.header(f"{ticker} Live Price: ${live_price:.2f}")

        returns = get_returns(ticker)
        

        # Display returns in a horizontal layout
        st.write(pd.DataFrame(list(returns.items()), columns=["Metric", "Value"]))

 

    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

        
    if ticker and ticker not in st.session_state.stored_data:
        st.session_state.stored_data[ticker] = {}  # Initialize a dictionary for this ticker
    
    if 'stored_data' not in st.session_state:
        st.session_state.stored_data = {}

    data_choice = st.radio("Select data for calculations and simulations:", 
                           ["Use input dates", "Use all available data"])

    if st.button("Calculate Metrics"):
        try:
            if data_choice == "Use input dates":
                data = fetch_equity_data(ticker, start_date, end_date)
            else:
                data = fetch_equity_data(ticker)
             
            if data is not None:
                # Metrics calculation
                metrics = {}
                ticker_beta = fetch_beta(ticker)
                metrics['Beta'] = ticker_beta
                metrics['Mean Price'] = mean_price(data)
                metrics['Median Price'] = median_price(data)
                metrics['Standard Deviation'] = standard_deviation(data)
                metrics['Variance'] = variance(data)
                metrics['Skewness'] = price_skewness(data)
                metrics['Kurtosis'] = price_kurtosis(data)
                metrics['Annualized Return'] = calculate_annualized_return(data)
                metrics['Annualized Volatility'] = calculate_annualized_volatility(data)
                metrics['Sharpe Ratio'] = sharpe_ratio(data, risk_free)

                # Assuming you have defined these functions
                metrics['Moving Average (50 days)'] = moving_average(data['Adj Close'], 50).iloc[-1]
                metrics['RSI (14 days)'] = rsi(data['Adj Close']).iloc[-1]
                macd_line, signal_line = macd(data['Adj Close'])
                metrics['MACD'] = macd_line.iloc[-1]
                metrics['MACD Signal Line'] = signal_line.iloc[-1]

                metrics_df = pd.DataFrame.from_dict(metrics, orient='index', columns=['Value'])
                st.table(metrics_df)

             # Store in session state
                if 'stored_data' not in st.session_state:
                    st.session_state.stored_data = {}
                st.session_state.stored_data[ticker] = {'metrics': metrics}

        except Exception as e:
            st.error(f"Error occurred: {e}")


    num_days = st.number_input("Number of Forecast Days", min_value=1, max_value=252*10, value=252)
    num_simulations = st.number_input("Number of Simulations", min_value=1, max_value=10000, value=1000)

    
    def extract_percentile_values_MC(simulations, percentiles=[10, 25, 50, 75, 90]):
        starting_price = simulations.iloc[0].mean()
        end_values = simulations.iloc[-1]
        # Calculate percentage returns relative to the beginning value
        return {p: ((end_values.quantile(p/100.0) - starting_price) / starting_price) * 100 for p in percentiles}


    def calculate_positive_return_probabilities(simulations, percentiles):
        starting_value = simulations.iloc[0]
        probabilities = {}
    
        for p in percentiles:
            percentile_value = simulations.quantile(p/100.0)  # Divide by 100 to get the correct range
            probabilities[p] = (percentile_value > starting_value).mean()
        
        return probabilities


    def present_results(simulations, timeframes=[21, 63, 126, 251]):  
        percentiles = [10, 25, 50, 75, 90]
        data = []

        for timeframe in timeframes:
            end_values = simulations.iloc[timeframe]
            percentile_values = extract_percentile_values_MC(simulations.iloc[:timeframe], percentiles)
            positive_return_probabilities = calculate_positive_return_probabilities(end_values, simulations.iloc[:timeframe])

            # For Probability of Return
            data.append({
                "Percentile": f"{timeframe} days Probability of Positive Return",
                "10th": positive_return_probabilities[10],
                "25th": positive_return_probabilities[25],
                "50th": positive_return_probabilities[50],
                "75th": positive_return_probabilities[75],
                "90th": positive_return_probabilities[90]
                })
            
            # For Expected Return
            data.append({
                "Percentile": f"{timeframe} days Return",
                "10th": percentile_values[10],
                "25th": percentile_values[25],
                "50th": percentile_values[50],
                "75th": percentile_values[75],
                "90th": percentile_values[90]
                })
                
        MCresultsDF = pd.DataFrame(data)
        return MCresultsDF

    if st.button("Run Monte Carlo Simulation"):
        try:
            if data_choice == "Use input dates":
                data = fetch_equity_data(ticker, start_date, end_date)
            else:
                data = fetch_equity_data(ticker)

            results = monte_carlo_forecast(ticker, num_simulations, num_days, data=data)
        
            if results is not None:
                st.subheader(f"Results for {ticker} Simulations")
                df_results = pd.DataFrame({
                    "Metric": ["Probability of Positive Return", "Expected Return %"],
                    "Value": [results["Probability Positive Return"],
                              results["Expected Return %"]]
                    })
                
                # Convert the 'Value' column to string for display purposes
                df_results['Value'] = df_results['Value'].astype(str)
                st.table(df_results)
                st.subheader("Monte Carlo Simulations")
                fig = plot_monte_carlo(ticker)
                st.plotly_chart(fig)

                if ticker not in st.session_state.stored_data:
                    st.session_state.stored_data[ticker] = {}

                st.session_state.stored_data[ticker]['results'] = results
                
                MCresultsDF = present_results(results["Simulations"])
                st.table(MCresultsDF)


            else:
                st.error("Unable to perform Monte Carlo simulation due to invalid data.")

        except Exception as e:
            st.error(f"Error occurred: {e}")
            
            
    timestep = st.number_input("Select timestep:", min_value=10, max_value=252*10, value=60, step=1)
    T = st.number_input("Predict for the next T days:", min_value=10, max_value=252, value=10, step=1)
    
            
    if st.button("Start LSTM Prediction"):
        # Check if the ticker is valid and has data
       
        data = get_data(ticker)
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data)
        X, y = create_dataset(scaled_data, timestep)

        train_size = int(len(X) * 0.67)
        X_train, X_test = X[0:train_size], X[train_size:]
        y_train, y_test = y[0:train_size], y[train_size:]

        model = create_model(timestep)
        train_model_with_progress(model, X_train, y_train)

        predicted_prices = predict_next_t_days(model, scaled_data, t=T, timestep=timestep, scaler=scaler)

        # Get the last 'timestep' days of the original data for visualization
        last_data_points = data[-timestep:].flatten()

        # Create a DataFrame for visualization
        df_visualization = pd.DataFrame({
            'days': list(range(-timestep, 0)) + list(range(1, T + 1)),
            'price': np.concatenate((last_data_points, predicted_prices.flatten())),
            'type': ['historical'] * timestep + ['predicted'] * T
            })
        
        # Use Altair to plot
        chart = alt.Chart(df_visualization).mark_line().encode(
            x='days',
            y='price',
            color=alt.Color('type', scale=alt.Scale(domain=['historical', 'predicted'], range=['blue', 'red']))
            )
        
        st.altair_chart(chart, use_container_width=True)
            

    

 
                    
                    

elif selection == "Crypto Screener":
    # Will populate this in the next step
    st.title("Crypto Screener")

    ticker = st.text_input("Enter ticker for analysis:").upper()
    
    def get_live_price(ticker):
        equity = yf.Ticker(ticker)
        try:
            return equity.info['currentPrice']
        except KeyError:
            try:
                return equity.info['regularMarketPrice']
            except KeyError:
                try:
                    return equity.history(period="1d")["Close"].iloc[0]
                except:
                    st.warning(f"Unable to fetch live price for {ticker}. Please try another ticker or check the ticker's validity.")
                    return None



    def get_returns(ticker):
        today = datetime.date.today()
        equity = yf.Ticker(ticker)
        prices = equity.history(period="1y")["Close"]

        one_day_return = ((prices[-1] - prices[-2]) / prices[-2]) * 100
        five_day_return = ((prices[-1] - prices[-5]) / prices[-5]) * 100
        one_month_return = ((prices[-1] - prices[-30]) / prices[-30]) * 100
        three_month_return = ((prices[-1] - prices[-90]) / prices[-90]) * 100
        six_month_return = ((prices[-1] - prices[-180]) / prices[-180]) * 100
        one_year_return = ((prices[-1] - prices[0]) / prices[0]) * 100
        ytd_start_price = prices[today.replace(month=1, day=1):].iloc[0]
        ytd_return = ((prices[-1] - ytd_start_price) / ytd_start_price) * 100

        returns = {
         "1 Day": f"{one_day_return:.2f}%",
         "5 Days": f"{five_day_return:.2f}%",
         "1 Month": f"{one_month_return:.2f}%",
         "3 Months": f"{three_month_return:.2f}%",
         "6 Months": f"{six_month_return:.2f}%",
         "1 Year": f"{one_year_return:.2f}%",
         "YTD": f"{ytd_return:.2f}%"
    }

        # Fetch additional information
        equity_info = equity.info
        fifty_two_week_high = equity_info.get('fiftyTwoWeekHigh', 'N/A')
        fifty_two_week_low = equity_info.get('fiftyTwoWeekLow', 'N/A')
        all_time_high = equity_info.get('dayHigh', 'N/A')  # Assuming this represents the all-time high

        returns["52-Week High"] = fifty_two_week_high
        returns["52-Week Low"] = fifty_two_week_low
        returns["All-Time High"] = all_time_high


        return returns

  
    if ticker:
        live_price = get_live_price(ticker)
        st.header(f"{ticker} Live Price: ${live_price:.2f}")

        returns = get_returns(ticker)
        

        # Display returns in a horizontal layout
        st.write(pd.DataFrame(list(returns.items()), columns=["Metric", "Value"]))

 

    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if 'show_monte_carlo_input' not in st.session_state:
        st.session_state.show_monte_carlo_input = False
        
    if ticker and ticker not in st.session_state.stored_data:
        st.session_state.stored_data[ticker] = {}  # Initialize a dictionary for this ticker
    
    if 'stored_data' not in st.session_state:
        st.session_state.stored_data = {}

    if st.button("Calculate Metrics"):
        if ticker:
            data = fetch_equity_data_safe(ticker, start_date, end_date)

            if data is not None:
                metrics = {}
                metrics['Beta'] = fetch_beta(ticker)
                metrics['Mean Price'] = mean_price(ticker)
                metrics['Median Price'] = median_price(ticker)
                metrics['Standard Deviation'] = standard_deviation(ticker)
                metrics['Variance'] = variance(ticker)
                metrics['Skewness'] = price_skewness(ticker)
                metrics['Kurtosis'] = price_kurtosis(ticker)
                metrics['Annualized Return'] = calculate_annualized_return(data)
                metrics['Annualized Volatility'] = calculate_annualized_volatility(data)
                metrics['Sharpe Ratio'] = sharpe_ratio(data, risk_free)

                metrics['Moving Average (50 days)'] = moving_average(data['Adj Close'], 50).iloc[-1]
                metrics['RSI (14 days)'] = rsi(data['Adj Close']).iloc[-1]
                macd_line, signal_line = macd(data['Adj Close'])
                metrics['MACD'] = macd_line.iloc[-1]
                metrics['MACD Signal Line'] = signal_line.iloc[-1]

                metrics_df = pd.DataFrame.from_dict(metrics, orient='index', columns=['Value'])
                st.table(metrics_df)

                st.session_state.show_monte_carlo_input = True
                
                
                if ticker not in st.session_state.stored_data:
                    st.session_state.stored_data[ticker] = {}
                
                st.session_state.stored_data[ticker]['metrics'] = metrics
                
                st.write(data.dtypes)



    if st.session_state.show_monte_carlo_input:
        num_days = st.number_input("Number of Forecast Days", min_value=1, max_value=252*10, value=252)
        num_simulations = st.number_input("Number of Simulations", min_value=1, max_value=10000, value=1000)

        if st.button("Run Monte Carlo Simulation"):
            results = monte_carlo_forecast(ticker, num_simulations, num_days)

            st.subheader(f"Results for {ticker} Simulations")
            df_results = pd.DataFrame({
                "Metric": ["Probability of Positive Return", "Expected Return %"],
                "Value": [results["Probability Positive Return"],
                          results["Expected Return %"]]
            })
            st.table(df_results)
            st.subheader("Monte Carlo Simulations")
            st.line_chart(results["Simulations"])
        

            if ticker not in st.session_state.stored_data:
                st.session_state.stored_data[ticker] = {}
            
            st.session_state.stored_data[ticker]['results'] = results
            
            st.write(data.dtypes)
    
            
    if st.button("Start LSTM Prediction"):
        # Check if the ticker is valid and has data
        data = get_data(ticker)
        if data is not None:
            # Normalize data
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(data)

            # Create dataset with the selected timestep
            X, y = create_dataset(scaled_data, timestep=timestep)

            # Split dataset into training and testing sets
            train_size = int(len(X) * 0.67)
            X_train, X_test = X[0:train_size], X[train_size:len(X)]
            y_train, y_test = y[0:train_size], y[train_size:len(y)]

            model = create_model(timestep=timestep)
            train_model_with_progress(model, X_train, y_train, epochs=100, batch_size=32)


            predicted_prices = predict_next_t_days(model, scaled_data, t=T, timestep=timestep)

            # Visualize predictions
            st.line_chart(predicted_prices, use_container_width=True)
            

            

    
    
elif selection == "Comparative Screener and Picker":
    st.title("Comparative Screener and Picker")

    # Create a list of metrics and results for each ticker
    metric_data = []

    for ticker, data in st.session_state.stored_data.items():
        ticker_data = {}

        if 'metrics' in data:
            for metric, value in data['metrics'].items():
                if isinstance(value, float):
                    value = round(value, 2)
                ticker_data[metric] = value

        if 'results' in data:
            for metric, value in data['results'].items():
                if metric not in ["Simulations", "Mean Return", "Expected Dollar Return with purchase of 1 share"]:
                    if isinstance(value, float):
                        value = round(value, 2)
                    ticker_data[metric] = value

        ticker_data["Ticker"] = ticker  # Add the ticker as a row

        metric_data.append(ticker_data)

    # Create a DataFrame from the metric data
    df = pd.DataFrame(metric_data)

    # Move the "Ticker" column to the front
    df = df[['Ticker'] + [col for col in df.columns if col != 'Ticker']]

    # Transpose the DataFrame to have tickers in the first column
    df = df.T

    # Display the transposed DataFrame as a table
    st.table(df)




elif selection == "Option Screener":
    st.title("Option Screener")
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    from datetime import date
    ticker = st.text_input("Enter ticker for analysis:").upper()    
    

    def fetch_expiry_dates(ticker):
        stock = yf.Ticker(ticker)
        return stock.options

    
    def get_implied_volatility(ticker, expiry, strike, option_type):
        # Get option chain for the ticker
        option_chain = yf.Ticker(ticker).option_chain(date=expiry)
        
        # Fetch call or put data based on user selection
        if option_type == "Call":
            options_data = option_chain.calls
        elif option_type == "Put":
                options_data = option_chain.puts
        else:
            return None

    # Filter for the selected strike
        option_at_strike = options_data[options_data['strike'] == strike]

        # If there's no such option, return None
        if option_at_strike.empty:
            return None

        # Return the implied volatility, stripping the '%' and converting to a fraction
        return float(option_at_strike['impliedVolatility'].iloc[0]) / 100


    def fetch_options(ticker, expiry_date):
        stock = yf.Ticker(ticker)
        opt = stock.option_chain(expiry_date)
        return opt

    import math
    import scipy.stats as stats

    def black_scholes(S, K, T, r, sigma, option_type="Call"):
        d1 = (math.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
    
        if option_type == "Call":
            return S * stats.norm.cdf(d1) - K * math.exp(-r * T) * stats.norm.cdf(d2)
        elif option_type == "Put":
            return K * math.exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)





    try:
        expiry_dates = fetch_expiry_dates(ticker)
        selected_expiry_date = st.selectbox('Select Expiry Date', expiry_dates)
        options = fetch_options(ticker, selected_expiry_date)

        option_type = st.radio("Option Type", ["Call", "Put"])
        if option_type == "Call":
            options_list = options.calls
        else:
            options_list = options.puts

        strikes = options_list['strike'].tolist()
        selected_strike = st.selectbox('Select Strike', strikes)
        selected_option = options_list[options_list['strike'] == selected_strike].iloc[0]
        premium = selected_option['lastPrice']
        st.write(f"Last Close Premium: ${premium}")

        # Calculate contract value
        num_contracts = st.number_input('Number of contracts', 1)
        contract_value = premium * 100 * num_contracts
        st.write(f"Total value for {num_contracts} contracts: ${contract_value:.2f}")

        stock_price_start = st.number_input("Start Stock Price", min_value=0.01, max_value=selected_strike*2, value=0.5*selected_strike)
        stock_price_end = st.number_input("End Stock Price", min_value=stock_price_start+0.01, max_value=selected_strike*3, value=1.5*selected_strike)

        
        if st.button("Generate Profit Heatmap"):
            stock_prices = np.linspace(stock_price_start, stock_price_end, 100)
            days_to_expiry = np.linspace(0, (np.datetime64(selected_expiry_date) - np.datetime64(date.today())).astype(int), 100)

            sigma = get_implied_volatility(ticker, selected_expiry_date, selected_strike, option_type)
            if sigma is None:
                st.warning("Failed to fetch implied volatility from Yahoo Finance. Please provide manually.")
                sigma = st.slider("Volatility (σ)", 0.05, 0.5, 0.2)
            
            profit_matrix = np.array([[black_scholes(sp, selected_strike, day/365, risk_free, sigma, option_type) * num_contracts * 100 
                                       for sp in stock_prices] 
                                      for day in days_to_expiry])

        fig = go.Figure(data=go.Heatmap(
                       z=profit_matrix,
                       x=days_to_expiry,
                       y=stock_prices,
                       hoverongaps = False,
                       colorscale='Viridis'))
        fig.update_layout(title=f'Profit Heatmap for {ticker} {option_type} Option (Strike: {selected_strike}, Expiry: {selected_expiry_date})',
                          xaxis_title='Days to Expiry',
                          yaxis_title='Stock Price at Expiry')
        st.plotly_chart(fig)

    except Exception as e:
        st.write("Error fetching option data:", e)



elif selection == "Index/Fund Screener":
    st.title("Index/Fund Screener")
    etf_ticker = st.text_input("Enter ETF Ticker (e.g., QQQ): ")
    

    if etf_ticker:
        st.write(f"Fetching constituents for {etf_ticker}...")
        current_etf_price = constituentPrice(etf_ticker)

        st.markdown(f"## Current Price of {etf_ticker}: **${current_etf_price:.2f}**")
        fund_name, daily_return, fifty_two_week_return = get_fund_details(etf_ticker)
        st.write(f"Fund Name: {fund_name}")
        st.write(f"Daily Return: {daily_return:.2f}%")
        st.write(f"52-Week Return: {fifty_two_week_return:.2f}%")
        
        
        constituents = get_constituents(etf_ticker)
        
    


        expected_analyst_move = sum(
            float(row["Weight(%)"].replace('%','')) * row["Target % Difference"] / 100
            for row in constituents if row["Target % Difference"] is not None
        )

        # Display the table and the expected analyst move
        st.table(constituents)
        st.write(f"Expected Analyst Move for {etf_ticker}: **{expected_analyst_move:.2f}%**")
        
        # Let the user pick a constituent for a DCF deep dive
        tickers = [constituent['Symbol'] for constituent in constituents]
        
        if 'selected_ticker' not in st.session_state:
           st.session_state.selected_ticker = tickers[0]  # Default value

        selected_ticker = st.selectbox('Select a ticker for a deep dive:', tickers, index=tickers.index(st.session_state.selected_ticker))
        st.session_state.selected_ticker = selected_ticker
        
        fcfs = get_free_cash_flow(selected_ticker)
        
        # Fetch DCF details for the selected ticker
        dcf_details = get_dcf_details_for_ticker(selected_ticker)
        
        if dcf_details:
            markdown_str = dcf_to_markdown_table(dcf_details, fcfs)
            st.markdown(markdown_str)

            
            


elif selection == "Quantitative Modelling":
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression




elif selection == 'Portfolio Tracker':
    st.title('Portfolio Tracker')
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = []
    
    if st.button("Load Portfolio"):
        st.session_state.portfolio = load_portfolio()
        st.write("Portfolio loaded successfully!")


    def display_input():
        # Show input options
        ticker = st.text_input("Enter ticker for holding:").upper()
        quantity = st.number_input("Quantity", step=0.1)
        purchase_price = st.number_input("Purchase Price")
        purchase_date = st.date_input("Purchase Date")
        if st.button("Submit"):
            # Check if ticker already exists in portfolio
            for holding in st.session_state.portfolio:
                if holding['ticker'] == ticker:
                    holding['transactions'].append({
                        'quantity': quantity,
                        'purchase_price': purchase_price,
                        'purchase_date': purchase_date
                    })
                    break
            else:
                # If ticker not in portfolio, create a new entry
                st.session_state.portfolio.append({
                    'ticker': ticker,
                    'transactions': [{
                        'quantity': quantity,
                        'purchase_price': purchase_price,
                        'purchase_date': purchase_date
                    }]
                })
            st.session_state.add_purchase_clicked = False  # Reset flag
    
        # After adding the transaction, save the updated portfolio
        save_portfolio(st.session_state.portfolio)

    def display_portfolio():
        if st.session_state.portfolio:
            # DCA Visualization
            for holding in st.session_state.portfolio:
                data = fetch_equity_data(holding['ticker'])
                if not data.empty:
                    dates = [x['purchase_date'] for x in holding['transactions']]
                    prices = [x['purchase_price'] for x in holding['transactions']]
                    quantities = [x['quantity'] for x in holding['transactions']]
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Price'))
                    fig.add_trace(go.Scatter(x=dates, y=prices, mode='markers', name='Purchases'))
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)')   
                    st.plotly_chart(fig)

            # Display current holdings and update values
            portfolio_df = pd.DataFrame(st.session_state.portfolio)
            current_prices = [fetch_equity_data(row['ticker'])['Close'].iloc[-1] if fetch_equity_data(row['ticker']) is not None else None for _, row in portfolio_df.iterrows()]

            def weighted_avg_price(transactions):
                total_quantity = sum(transaction['quantity'] for transaction in transactions)
                total_cost = sum(transaction['purchase_price'] * transaction['quantity'] for transaction in transactions)
                return total_cost / total_quantity if total_quantity else 0

            portfolio_df['avg_purchase_price'] = [weighted_avg_price(row['transactions']) for _, row in portfolio_df.iterrows()]
            portfolio_df['total_quantity'] = [sum(transaction['quantity'] for transaction in row['transactions']) for _, row in portfolio_df.iterrows()]
            portfolio_df['current_price'] = current_prices
            portfolio_df['current_value'] = portfolio_df['total_quantity'] * portfolio_df['current_price']
            portfolio_df['gain/loss'] = (portfolio_df['current_price'] - portfolio_df['avg_purchase_price']) * portfolio_df['total_quantity']

            min_date = min(transaction['purchase_date'] for holding in st.session_state.portfolio for transaction in holding['transactions'])
            portfolio_dates = pd.date_range(min_date, pd.Timestamp.today(), freq='D')
            portfolio_values = []

            last_known_values = {}  # Dictionary to store the last known closing prices for each ticker
            last_valid_value = 0
            
            for date in portfolio_dates:
                daily_value = 0
                quantity_on_date = {}  # Keeps track of quantity of a ticker on the current date
        
                # Skip weekends
                if date.weekday() >= 5: 
                    continue

                for holding in st.session_state.portfolio:
                    ticker = holding['ticker']
                    # Update quantity_on_date for the current ticker
                    quantity_on_date[ticker] = sum(transaction['quantity'] for transaction in holding['transactions'] if transaction['purchase_date'] <= date)
        
                    daily_data = fetch_equity_data(ticker, start_date=date.strftime('%Y-%m-%d'), end_date=(date + pd.Timedelta(days=1)).strftime('%Y-%m-%d'))
                    # If there's valid data for the date, update the last known value
                    if daily_data is not None and not daily_data.empty:
                        last_known_values[ticker] = daily_data['Close'].iloc[0]
                        daily_value += last_known_values.get(ticker, 0) * quantity_on_date[ticker]

        
                if daily_value == 0:
                    daily_value = last_valid_value
                else:
                    last_valid_value = daily_value
                    
                portfolio_values.append(daily_value)



            fig = go.Figure()
            fig.add_trace(go.Scatter(x=portfolio_dates, y=portfolio_values, mode='lines', name='Portfolio Value'))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)')   
            st.plotly_chart(fig)
            st.write(portfolio_df)

    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = []
        
    if 'add_purchase_clicked' not in st.session_state:
        st.session_state.add_purchase_clicked = False

    if st.session_state.add_purchase_clicked or st.button("Add Purchase"):
        st.session_state.add_purchase_clicked = True
        display_input()
    else:
        display_portfolio()
    
    display_remove_table()
    

# Streamlit UI
# ... other code for other tabs ...













    








