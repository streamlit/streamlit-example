import shap
import streamlit as st
import streamlit.components.v1 as components
import xgboost
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)
  
df = df.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1)

def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)
    
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


st.title("SHAP Interpretation")

# train XGBoost model
model = xgboost.train({"learning_rate": 0.01}, xgboost.DMatrix(X, label=y), 100)

# explain the model's predictions using SHAP
# (same syntax works for LightGBM, CatBoost, scikit-learn and spark models)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

st.write('<p style="font-size:130%">visualize the first prediction explanation </p>', unsafe_allow_html=True)
#  (use matplotlib=True to avoid Javascript)
st_shap(shap.force_plot(explainer.expected_value, shap_values[0,:], X.iloc[0,:]))

st.write('<p style="font-size:130%">visualize the training set predictions </p>', unsafe_allow_html=True)
st_shap(shap.force_plot(explainer.expected_value, shap_values, X), 400)



