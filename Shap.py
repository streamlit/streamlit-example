import shap
import streamlit as st
import streamlit.components.v1 as components
import xgboost
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
st.markdown(f'# {list(page_names_to_funcs.keys())[5]}')
    
#uploaded_file = st.file_uploader("Choose a file")
#if uploaded_file is not None:
#  df = pd.read_csv(uploaded_file)

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data('modelling_shap_2012_2015.csv')
df = df.sample(n=1000)
def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)

             
y =df['grav']
X = df.drop(['grav','gravMerged'], axis = 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

st.write('XGBoost model')
model = xgboost.train({"learning_rate": 0.01}, xgboost.DMatrix(X, label=y), 100)

st.markdown('''explain the model's predictions using SHAP''')
    
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

st.write('<p style="font-size:130%"> #Visualize the first prediction explanation </p>', unsafe_allow_html=True)
st_shap(shap.force_plot(explainer.expected_value, shap_values[0,:], X.iloc[0,:]))

st.write('<p style="font-size:130%"> #Visualize the training set predictions </p>', unsafe_allow_html=True)
st_shap(shap.force_plot(explainer.expected_value, shap_values, X), 400)
