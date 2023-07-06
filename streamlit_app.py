import streamlit as st
import pandas as pd
import dask.dataframe as dd
import matplotlib.pyplot as plt
from datetime import datetime
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from pmdarima.arima import auto_arima
import numpy as np
from statsmodels.tsa.stattools import acf, pacf
from pandas.plotting import autocorrelation_plot, lag_plot
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_squared_error




def custom_date_parser(x):
    return pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S')

# 讀取資料
@st.cache_data
def load_data():
    # 創建一個包含所有文件的列表
    filenames = ['ETH_1min_{:02d}.csv'.format(i) for i in range(20)]
    
    # 讀取所有文件並合併成一個Dask DataFrame
    dfs = [dd.read_csv(filename) for filename in filenames]
    df = dd.concat(dfs)
    
    # 排序
    df = df.sort_values(by='Unix Timestamp')
    
    # 選擇所需的列
    df = df[['Date', 'Close']]
    
    # 將日期列進行自定義日期解析
    df['Date'] = df['Date'].apply(custom_date_parser, meta=('Date', 'datetime64[ns]'))
    
    return df

# 將資料合併成小時級別，並排序按照Date，並將DATE設置為index
def to_hour(df):
    df = df.set_index('Date')
    df_hour = df.resample('1H').agg({'Close': 'last'})
    df_hour.index.freq = 'H'  # 显式设置频率为小时级别
    df_hour['Close'] = df_hour['Close'].fillna(method='ffill')
    return df_hour


df = load_data()
df = df.compute()
df = to_hour(df)


# def custom_date_parser(x):
#     return pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S')
    
# # 讀取資料
# def load_data():
#     df = dd.read_csv('ETH_1min.csv')
#     df = df.sort_values(by='Unix Timestamp')
#     df = df[['Date', 'Close']]
#     df['Date'] = df['Date'].apply(custom_date_parser, meta=('Date', 'datetime64[ns]'))
#     return df

# # 將資料合併成小時級別，並排序按照Date，並將DATE設置為index
# def to_hour(df):
#     df = df.set_index('Date')
#     df_hour = df.resample('1H').agg({'Close': 'last'})
#     df_hour['Close'] = df_hour['Close'].fillna(method='ffill')
#     return df_hour

# df = load_data()
# df = df.compute()
# df = to_hour(df)



# Streamlit應用程式開始
st.title('Time Series Analysis and Prediction')
st.subheader('Hourly Data')

# 顯示原始資料
st.write('Original Data:')
st.write(df)

# 繪製原始資料圖表
st.subheader('Original Data Plot + MA50 + MA200')
fig, ax = plt.subplots(figsize=(16, 10))
ax.plot(df.Close, c='navy', label='Close')
ax.plot(df.Close.rolling(window=50).mean(), c='red', label='MA50')
ax.plot(df.Close.rolling(window=200).mean(), c='orange', label='MA200')
ax.legend(loc='upper left')
st.pyplot(fig)

# 執行simple exponential smoothing
fit2 = SimpleExpSmoothing(df.Close).fit(smoothing_level=0.6, optimized=False)
df['SES'] = fit2.fittedvalues
# 繪製simple exponential smoothing結果圖表
st.subheader('simple exponential smoothing')
fig2, ax2 = plt.subplots(figsize=(16, 10))
ax2.plot(df.Close, c='navy', label='Close')
ax2.plot(df.SES, c='green', label='SES')
ax2.legend(loc='upper left')
st.pyplot(fig2)

# 季節性分析
st.subheader('Seasonailty Analystic')
to_be_examined = df['Close']
result = seasonal_decompose(to_be_examined, model='multiplicative')
# 圖表
fig, ax = plt.subplots(4, 1, figsize=(12, 8), sharex=True)
# 原始數據
to_be_examined.plot(ax=ax[0])
ax[0].set_title('Original Data')
# 趨勢
result.trend.plot(ax=ax[1])
ax[1].set_title('Trend')
# 季節性
result.seasonal.plot(ax=ax[2])
ax[2].set_title('Seasonality')
# 白噪音
result.resid.plot(ax=ax[3])
ax[3].set_title('Residuals')
# 共享 x 軸和圖例位置
plt.tight_layout()
plt.xlabel('Time')
plt.legend()
# 在 Streamlit 中顯示圖表
st.pyplot(fig)




st.subheader('differencing by different lags')
lag_num = 1
fig, ax = plt.subplots(figsize=(15, 10), dpi=120)
ax.plot(df.Close['2016-05-09 13:00:00':], label='orig')
ax.plot(df.Close['2016-05-09 13:00:00':].diff(lag_num), label='lag-1')
ax.plot(df.Close['2016-05-09 13:00:00':].diff(lag_num + 11), label='lag-12')
ax.plot(df.Close['2016-05-09 13:00:00':].diff(lag_num + 23).diff(1), label='double-diff(24, 1)')
ax.legend(shadow=True, fontsize=14)
st.pyplot(fig)
# t - (t-1)之後數值應該以0為中心上下震盪
# 會發現diff的效果變成shift了圖形一段(amt這個dataframe資料有規律？)
# diff函數相當好用，只用這個函數就能達到我們要的differencing的效果。



edf = df.Close.diff(24).diff(1)[25:] #要注意做diff時 第一項會是na所以要從第一個開始取值
st.subheader('Autocorrelation Plot')
fig1, ax1 = plt.subplots(figsize=(12, 5))
plot_acf(edf, lags=30, ax=ax1)
st.pyplot(fig1)
plt.close(fig1)

st.subheader('Partial Autocorrelation Plot')
fig2, ax2 = plt.subplots(figsize=(12, 5))
plot_pacf(edf, lags=30, method='ywm', ax=ax2)
st.pyplot(fig2)
plt.close(fig2)


# 切分資料集
train_size = int(len(edf) * 0.7)  # 訓練資料佔 70%
val_size = int(len(edf) * 0.2)    # 驗證資料佔 20%
test_size = len(edf) - train_size - val_size   # 測試資料佔剩下的部分

train_data = edf[:train_size]
val_data = edf[train_size:train_size+val_size]
test_data = edf[train_size+val_size:]

st.subheader('ARIMA_Model using valData')
model = ARIMA(train_data, order=(7, 0, 1))
model = model.fit()
summary = model.summary()
st.write(summary)


y_pred_val = model.predict(start = train_size, end = train_size + val_size - 1)
y_pred = model.predict(end = test_size - 1)

mse = mean_squared_error(val_data, y_pred_val)
rmse = np.sqrt(mse)

fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(test_data, c='g', label='y_true')
ax.plot(test_data.index, y_pred, c='red', label='y_pred')
ax.legend(title='RMSE = %.3f\n' % rmse, shadow=True, fontsize=14)

st.pyplot(fig)
plt.close(fig)


st.subheader('ARIMA_Model using testData')
model = ARIMA(train_data, order=(7, 0, 1))
model = model.fit()
summary = model.summary()
st.write(summary)
y_pred_test = model.predict(start = train_size + val_size, end = len(edf) - 1)
mse = mean_squared_error(test_data, y_pred_test)
rmse = np.sqrt(mse)

fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(test_data, c='g', label='y_true')
ax.plot(test_data.index, y_pred, c='red', label='y_pred')
ax.legend(title='RMSE = %.3f\n' % rmse, shadow=True, fontsize=14)

st.pyplot(fig)
plt.close(fig)


