from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import streamlit as st
import pandas as pd
import joblib
import sklearn


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

df = pd.read_csv('C:\\python\\roadAccidentInFrance\\dataset\\test_sample_15_06_2023.csv')

if df is not None:
    y_test =df['severity']
    X_test = df.drop(['severity','Unnamed: 0'], axis = 1)

 

if option=='Gradient Boosting':
   st.write('Gradient Boosting score train 73.127 rmse train 0.518')
   GBC=joblib.load('C:\\python\\roadAccidentInFrance\\models\\GBC_model.joblib')
   results(GBC)

if option=='Gradient Boosting improved':
   st.write('Gradient Boosting score train 78.535 rmse train 0.463')
   GBCi=joblib.load('C:\\python\\roadAccidentInFrance\\models\\GBC_improved_model.joblib')
   results(GBCi)


if option=='XGBOOST':
   st.write('XGBOOST score train 78.733 rmse train 0.461')
   xgb = joblib.load('C:\\python\\roadAccidentInFrance\\models\\xgb_model.joblib')
   results(xgb)


if option=='XGBOOST improved':
   st.write('XGBOOST score train 78.733 rmse train 0.461')
   xgbi = joblib.load('C:\\python\\roadAccidentInFrance\\models\\xgb_model.joblib')
   results(xgbi)

# if option=='Random Forest':
#    st.write('Random Forest score train 99.998 rmse train 0.004')
#    RFC = RandomForestClassifier()
#     #    RFC=joblib.load('C:\\python\\roadAccidentInFrance\\models\\RFC_model.joblib')
#    results(RFC)

# if option=='SVC':
#    st.write('SVC score train 74.286 rmse train 0.507')
#    SVC=joblib.load('C:\\python\\roadAccidentInFrance\\models\\SVC_model.joblib')
#    results(SVC)

# uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file).sample(n=10000)
        
#     @st.cache_data
#     def load_data(url):
#         df = pd.read_csv(url)
#         return df

  
