from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import streamlit as st
import pandas as pd
import joblib
import sklearn
import gzip


def results(model):
    st.markdown('## Accuracy')
    st.write(model.score(X_test, y_test))
    st.markdown('## Confusion Matrix')
    st.dataframe(confusion_matrix(y_test, model.predict(X_test)))
    st.markdown('## Classification Report')
    st.text(classification_report(y_test, model.predict(X_test)))

def splitDataset(df):
   y_test =df['grav']
   X_test = df.drop(['grav','gravMerged'], axis = 1)
   return y_test,X_test
   


st.markdown('# Machine learning models')
st.write("""Generally speaking we can consider that accuracy scores:
                          - Over 90% - Very Good
                    - Between 70% and 90% - Good
                    - Between 60% and 70% - OK""")

choices = ['XGBOOST','XGBOOST improved','Gradient Boosting','Gradient Boosting improved']
#choices = ['Gradient Boosting']
option = st.selectbox(
         'Which model do you want to try ?',
         choices)

st.write('You selected :', option)

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df



df = load_data('test_sample_15_06_2023.csv')

if df is not None:
    y_test =df['severity']
    X_test = df.drop(['severity','Unnamed: 0'], axis = 1)

 

if option=='Gradient Boosting':
   st.write('Gradient Boosting score train 73.127')
   GBC = GradientBoostingClassifier()
   GBC = GBC.load('Models/GBC_model.joblib')
   results(GBC)

if option=='Gradient Boosting improved':
   st.write('Gradient Boosting score train 78.535')
   GBCi = GradientBoostingClassifier()
   GBCi = GBCi.load('MModels/GBC_improved_model.joblib')
   results(GBCi)
   

if option=='XGBOOST':
   st.write('XGBOOST score train 78.733')
   xgb = xgb.XGBClassifier()
   xgb = xgb.load('Models/xgb_model.joblib')
   results(xgb)

if option=='XGBOOST improved':
   st.write('XGBOOST score train 78.733')
   xgbi = xgb.XGBClassifier()
   xgbi = xgbi.load('Models/xgboost_improved.joblib')
   results(xgbi)



  
