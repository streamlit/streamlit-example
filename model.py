import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
import streamlit as st
import xgboost as xgb
from xgboost import XGBClassifier
import joblib

#df = pd.read_csv('https://drive.google.com/file/d/1dLzhkMdx58uzJIjhqyFSQBFPKAIiZXhT/view?usp=sharing')

#uploaded_file = st.file_uploader("Choose a file")
#if uploaded_file is not None:
#  df = pd.read_csv(uploaded_file)
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data('https://bol.mondial-assistance.gr/Files/modelling/modelling_shap_2012_2015.csv')
#df = df.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1)
#df = df.drop(['gravMerged'], axis=1, inplace=True)


y =df['grav']
X = df.drop(['grav','gravMerged'], axis = 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

#loaded_model = pickle.load(open(filename, 'rb'))
#result = loaded_model.score(X_test, Y_test)
#print(result)

def prediction(classifier):
    #if classifier == 'Random Forest':
    #    clf = RandomForestClassifier()
    #elif classifier == 'SVC':
    #    clf = SVC()
    #elif classifier == 'KNN':
    #    clf = KNeighborsClassifier()
    if classifier == 'XGBOOST':
        #clf = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        clf = joblib.load('https://github.com/IsiD11/streamlit-example/blob/314ba6c248287502ab2e61a70598c3b48310cf93/xgb_model.sav')
    elif classifier == 'Gradient Boosting':
        #clf = GradientBoostingClassifier()
        clf = joblib.load('https://github.com/IsiD11/streamlit-example/blob/314ba6c248287502ab2e61a70598c3b48310cf93/gbc_model.sav')
        
    #clf.fit(X_train, y_train)
    return clf
    
def scores(clf, choice):
        if choice == 'Accuracy':
             return clf.score(X_test, y_test)
        elif choice == 'Confusion matrix':
            return confusion_matrix(y_test, clf.predict(X_test))
        elif choice == 'Classification report':
            return classification_report(y_test, clf.predict(X_test))
