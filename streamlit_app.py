import streamlit as st
import pandas as pd
# import dask.dataframe as dd
import matplotlib.pyplot as plt
import datetime
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

    #因為header缺失導致concat函式無法正常合併
# 讀取資料
@st.cache_data
def load_data():
    # 定義 CSV 檔案的數量
    num_files = 20 

    # 定義 CSV 檔案的網址前綴
    url_prefix = 'https://raw.githubusercontent.com/CrayonDing0909/streamlit-example/master/ETH_1min_'

    # 读取第一个CSV文件（保留头部）
    df = pd.read_csv(url_prefix + '00.csv')

 # 使用循环生成文件网址并读取合并 CSV 文件
    for i in range(num_files):
        file_url = url_prefix + '{:02d}.csv'.format(i)
        temp_df = pd.read_csv(file_url) 
        if i == 0:
            df = temp_df.copy()  # 第一个文件保留全部内容
        else:
            header = df.columns  # 获取第一个文件的 header 行
            temp_df.columns = header  # 设置当前文件的列名为第一个文件的列名
            df = pd.concat([df, temp_df])  # 后续文件添加到合适的位置       
 



    # 排序
    df = df.sort_values(by='Unix Timestamp')

    # 选择所需的列，降低 RAM 的需求
    df = df[['Date', 'Close']]

    # 将日期列进行自定义日期解析
    df['Date'] = df['Date'].apply(custom_date_parser)

    return df

# 將資料合併成小時級別，並排序按照 Date，並將 DATE 設置為 index
def to_hour(df):
    df = df.set_index('Date')
    df_hour = df.resample('1H').agg({'Close': 'last'})
    df_hour.index.freq = 'H'  # 設置頻率為小時級別
    df_hour['Close'] = df_hour['Close'].fillna(method='ffill')
    return df_hour




df = load_data()
df = to_hour(df)


def df_filter(message, df):
    start_date = st.date_input('Start Date', df.index.min())
    end_date = st.date_input('End Date', df.index.max())

    # 將時間轉換為 datetime.time 類型，並顯示預設值
    start_time = st.time_input('Start Time', datetime.time(0, 0))
    end_time = st.time_input('End Time', datetime.time(23, 45))

    start_datetime = pd.to_datetime(str(start_date) + ' ' + str(start_time.hour) + ':' + str(start_time.minute))
    end_datetime = pd.to_datetime(str(end_date) + ' ' + str(end_time.hour) + ':' + str(end_time.minute))

    start_date_str = start_datetime.strftime('%Y-%m-%d %I:%M%p')
    end_date_str = end_datetime.strftime('%Y-%m-%d %I:%M%p')

    st.info('Start: **%s** End: **%s**' % (start_date_str, end_date_str))

    filtered_df = df[(df.index >= start_datetime) & (df.index <= end_datetime)]

    return filtered_df





# Streamlit應用程式開始
st.title('Time Series Analysis and Prediction')
# st.subheader('Hourly Data')
st.subheader('Datetime Filter')
filtered_df = df_filter('Select a time range:', df)
# 顯示原始資料
# st.write('Original Data:')

# st.write(filtered_df)

# 繪製原始資料圖表
st.subheader('Original Data Plot + MA50 + MA200')
fig, ax = plt.subplots(figsize=(16, 10))
ax.plot(filtered_df.Close, c='navy', label='Close')
ax.plot(filtered_df.Close.rolling(window=50).mean(), c='red', label='MA50')
ax.plot(filtered_df.Close.rolling(window=200).mean(), c='orange', label='MA200')
ax.legend(loc='upper left')
st.pyplot(fig)

# 執行simple exponential smoothing
fit2 = SimpleExpSmoothing(filtered_df.Close).fit(smoothing_level=0.6, optimized=False)
filtered_df['SES'] = fit2.fittedvalues
# 繪製simple exponential smoothing結果圖表
st.subheader('simple exponential smoothing')
fig2, ax2 = plt.subplots(figsize=(16, 10))
ax2.plot(filtered_df.Close, c='navy', label='Close')
ax2.plot(filtered_df.SES, c='green', label='SES')
ax2.legend(loc='upper left')
st.pyplot(fig2)






# 季節性分析
st.subheader('Seasonailty Analystic')
to_be_examined = filtered_df['Close']
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
ax.plot(filtered_df.Close['2016-05-09 13:00:00':], label='orig')
ax.plot(filtered_df.Close['2016-05-09 13:00:00':].diff(lag_num), label='lag-1')
ax.plot(filtered_df.Close['2016-05-09 13:00:00':].diff(lag_num + 11), label='lag-12')
ax.plot(filtered_df.Close['2016-05-09 13:00:00':].diff(lag_num + 23).diff(1), label='double-diff(24, 1)')
ax.legend(shadow=True, fontsize=14)
st.pyplot(fig)
# t - (t-1)之後數值應該以0為中心上下震盪
# 會發現diff的效果變成shift了圖形一段(amt這個dataframe資料有規律？)
# diff函數相當好用，只用這個函數就能達到我們要的differencing的效果。


#double diff
edf = filtered_df.Close.diff(24).diff(1)[25:] #要注意做diff時 第一項會是na所以要從第一個開始取值
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

train_data = edf[:train_size] #0~70
val_data = edf[train_size:train_size+val_size]#
test_data = edf[train_size+val_size:]

st.subheader('ARIMA_Model using valData')
model = ARIMA(train_data, order=(7, 0, 1))
model = model.fit()
summary = model.summary()
st.write(summary)


y_pred_val = model.predict(start = train_size, end = train_size + val_size - 1)
y_pred = model.predict(end = test_size - 1)
#用train_data進行訓練
#以val_data（驗證資料集）做第一次predict然後找出最佳的超參數。

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
y_pred_test = model.predict(start = train_size + val_size, end = len(edf) - 1)#用test_data進行predict
mse = mean_squared_error(test_data, y_pred_test)
rmse = np.sqrt(mse)

fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(test_data, c='g', label='y_true')
ax.plot(test_data.index, y_pred, c='red', label='y_pred')
ax.legend(title='RMSE = %.3f\n' % rmse, shadow=True, fontsize=14)

st.pyplot(fig)
plt.close(fig)


