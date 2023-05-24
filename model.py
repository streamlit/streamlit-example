import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import streamlit as st

#df = pd.read_csv('train.csv')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)
  


df = df.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1)

X_cat = df[['Pclass', 'Sex',  'Embarked']]
X_quant = df[['Age', 'Fare', 'SibSp', 'Parch']]
y = df['Survived']

for col in X_cat.columns:
    X_cat[col] = X_cat[col].fillna(X_cat[col].mode()[0])

for col in X_quant.columns:
    X_quant[col] = X_quant[col].fillna(X_quant[col].mean())


X_cat_scaled = pd.get_dummies(X_cat, columns=X_cat.columns)

X = pd.concat([X_cat_scaled, X_quant], axis = 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.25)

scaler = StandardScaler()
X_train[X_quant.columns] = scaler.fit_transform(X_train[X_quant.columns])
X_test[X_quant.columns] = scaler.transform(X_test[X_quant.columns])

def prediction(classifier):
    if classifier == 'Random Forest':
        clf = RandomForestClassifier()
    elif classifier == 'SVC':
        clf = SVC()
    elif classifier == 'Logistic Regression':
        clf = LogisticRegression()
    clf.fit(X_train, y_train)
    return clf

def scores(clf, choice):
    if choice == 'Accuracy':
        return clf.score(X_test, y_test)
    elif choice == 'Confusion matrix':
        return confusion_matrix(y_test, clf.predict(X_test))
