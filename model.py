import pandas as pd
from prophet import Prophet
import pmdarima as pmd
import pandas as pd 
import numpy as np
from scipy.stats import zscore
import statsmodels.api as sm
 
############################################## 
def working_day():
    date = "01-01-2019	01-02-2019	01-03-2019	01-04-2019	01-05-2019	01-06-2019	01-07-2019	01-08-2019	01-09-2019	01-10-2019	01-11-2019	01-12-2019	01-01-2020	01-02-2020	01-03-2020	01-04-2020	01-05-2020	01-06-2020	01-07-2020	01-08-2020	01-09-2020	01-10-2020	01-11-2020	01-12-2020	01-01-2021	01-02-2021	01-03-2021	01-04-2021	01-05-2021	01-06-2021	01-07-2021	01-08-2021	01-09-2021	01-10-2021	01-11-2021	01-12-2021	01-01-2022	01-02-2022	01-03-2022	01-04-2022	01-05-2022	01-06-2022	01-07-2022	01-08-2022	01-09-2022	01-10-2022	01-11-2022	01-12-2022	01-01-2023	01-02-2023	01-03-2023	01-04-2023	01-05-2023	01-06-2023	01-07-2023	01-08-2023	01-09-2023	01-10-2023	01-11-2023	01-12-2023"
    date = date.split("\t")

    workday = "29	18	31	28	30	30	31	31	29	31	30	31	21	29	31	26	30	30	31	31	28	31	30	31	30	19	31	26	30	24	18	16	21	31	30	31	27	22	31	27	30	30	31	31	27	31	30	31	20	28	31	28	30	30	31	31	27	31	30	30"
    workday = workday.split("\t")

    data = {'Date': date,
            'WD': workday}  

    # working day
    WD = pd.DataFrame(data)
    return WD
############################################## 

#forecast length
def fc_length(n=12):
    fcperiod = n
    return fcperiod

#clean outlier
def clean_outlier(df: pd.DataFrame):
    df = df.fillna(df.median())
    df = df[(np.abs(df.apply(zscore))<2.3)]
    df = df.fillna(df.median())
    return df
   
############################################## 
#EXOGENOUS VARABILE
def exog_var(df: pd.DataFrame):
    WD = working_day()
    fcperiod = fc_length()
    exog_fit = df.merge(WD[['WD']],left_index=True,right_index=True,how='inner')
    exog_fit = exog_fit.drop(exog_fit.columns.difference(['WD']),axis=1) #drop other column
    exog_fc = WD.merge(df,left_index=True,right_index=True,how='outer',indicator=True).query('_merge == "left_only"') #anti left join
    exog_fc = exog_fc.drop(exog_fc.columns.difference(['WD']),axis=1).head(fcperiod)

#create list of forecast date

df_P = pd.DataFrame()



############################################## 
def HoltWinter(df: pd.DataFrame):
 df = clean_outlier(df)
 fcperiod = fc_length()
 df_HW = pd.DataFrame()
 future_index = []
 future_index.append(df.tail(12).index.shift(12,freq="MS"))

 for sku in df.columns:
        fitHW = sm.tsa.ExponentialSmoothing(np.asarray(df[sku]), initialization_method="heuristic",seasonal_periods=12,trend='add', seasonal='add',damped_trend=True).fit(optimized=True)
        arr_forecast = fitHW.forecast(fcperiod)
        df_HW['HW_'+sku] = arr_forecast
        df_HW.set_index(future_index,inplace=True)
    
 return df_HW
 ############################################## 
def SARIMAX(df: pd.DataFrame):
    df = clean_outlier(df)
    fcperiod = fc_length()
    df_SARIMAX = pd.DataFrame()
    future_index = []
    future_index.append(df.tail(12).index.shift(12,freq="MS"))
    
    for sku in df.columns:
        ap_autoarimamodel = pmd.arima.auto_arima(np.asarray(df[sku]), 
                                         start_p=0, max_p=12,
                                         d=1, max_d=2,
                                         start_q=0, max_q=12,
                                         start_P=0, max_P=12,
                                         start_Q=0, max_Q=12,
                                         D=1,max_D=2,
                                         m=12,seasonal=True,
                                         error_action='warn',trace=True,supress_warnings=True,stepwise=True,random_state=20,n_fits=50)
        try:
            arr_forecast = ap_autoarimamodel.predict(n_periods=fcperiod,return_conf_int = False)
            df_SARIMAX['SARIMAX_'+sku] = arr_forecast
            df_SARIMAX.set_index(future_index,inplace=True)
        except:
            pass
    return df_SARIMAX
############################################## 
def UCM(df: pd.DataFrame):
      df = clean_outlier(df)
      fcperiod = fc_length()
      df_UCM = pd.DataFrame()
      future_index = []
      future_index.append(df.tail(12).index.shift(12,freq="MS"))
      
      for sku in df.columns:
          fitUCM = sm.tsa.UnobservedComponents(
                   np.asarray(df[sku]),
                   exog = exog_fit,
                   level=True, trend=False,cycle=True,irregular=True,damped_cycle=True,
                   stochastic_level=False,stochastic_trend=True,
                   autoregressive= pUCM,
                   freq_seasonal=[{'period':12,'harmonics':12}]).fit()
            arr_forecast = fitUCM.forecast(fcperiod,exog = exog_fc)
            df_UCM['UCM_'+sku] = arr_forecast
            df_UCM.set_index(future_index,inplace=True)
    
    
    
    
    
