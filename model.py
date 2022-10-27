import pandas as pd
from prophet import Prophet
import pmdarima as pmd
import pandas as pd 
import numpy as np
from scipy.stats import zscore
import statsmodels.api as sm
 
############################################## 
date = "01-01-2019	01-02-2019	01-03-2019	01-04-2019	01-05-2019	01-06-2019	01-07-2019	01-08-2019	01-09-2019	01-10-2019	01-11-2019	01-12-2019	01-01-2020	01-02-2020	01-03-2020	01-04-2020	01-05-2020	01-06-2020	01-07-2020	01-08-2020	01-09-2020	01-10-2020	01-11-2020	01-12-2020	01-01-2021	01-02-2021	01-03-2021	01-04-2021	01-05-2021	01-06-2021	01-07-2021	01-08-2021	01-09-2021	01-10-2021	01-11-2021	01-12-2021	01-01-2022	01-02-2022	01-03-2022	01-04-2022	01-05-2022	01-06-2022	01-07-2022	01-08-2022	01-09-2022	01-10-2022	01-11-2022	01-12-2022	01-01-2023	01-02-2023	01-03-2023	01-04-2023	01-05-2023	01-06-2023	01-07-2023	01-08-2023	01-09-2023	01-10-2023	01-11-2023	01-12-2023"
date = date.split("\t")

workday = "29	18	31	28	30	30	31	31	29	31	30	31	21	29	31	26	30	30	31	31	28	31	30	31	30	19	31	26	30	24	18	16	21	31	30	31	27	22	31	27	30	30	31	31	27	31	30	31	20	28	31	28	30	30	31	31	27	31	30	30"
workday = workday.split("\t")

data = {'Date': date,
        'WD': workday}  

# exogenous variable
WD = pd.DataFrame(data)
############################################## 

def clean_outlier(df):
    df = df.fillna(df.median())
    df = df[(np.abs(df.apply(zscore))<2.3)]
    df = df.fillna(df.median())
   
############################################## 
#exog for fitting
#exog_fit = df.merge(wd[['WD']],left_index=True,right_index=True,how='inner')
#exog_fit = exog_fit.drop(exog_fit.columns.difference(['WD']),axis=1) #drop other column
#exog for forecast
#exog_fc = wd.merge(df,left_index=True,right_index=True,how='outer',indicator=True).query('_merge == "left_only"') #anti left join
#exog_fc = exog_fc.drop(exog_fc.columns.difference(['WD']),axis=1).head(fcperiod)

#create list of forecast date

df_P = pd.DataFrame()

df_UCM = pd.DataFrame()
df_SARIMA = pd.DataFrame()
############################################## 


def HoltWinter(df: pd.DataFrame):
 fcperiod = 12
 df_HW = pd.DataFrame()
 future_index = []
 future_index.append(df.tail(12).index.shift(12,freq="MS"))

 
 
 for sku in df.columns:
        fitHW = sm.tsa.ExponentialSmoothing(np.asarray(df[sku]), initialization_method="heuristic",seasonal_periods=12,trend='add', seasonal='add',damped_trend=True).fit(optimized=True)
        arr_forecast = fitHW.forecast(fcperiod)
        df_HW['fc_'+sku] = arr_forecast
        df_HW.set_index(future_index,inplace=True)
    
 return pd.DataFrame(df_HW)
    
    
    
    
    
