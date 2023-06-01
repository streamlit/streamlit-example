import shap
import streamlit as st
import streamlit.components.v1 as components
import xgboost
import pandas as pd


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)

st.title("SHAP Interpretation")

# train XGBoost model
X,y = df
model = xgboost.train({"learning_rate": 0.01}, xgboost.DMatrix(X, label=y), 100)

# explain the model's predictions using SHAP
# (same syntax works for LightGBM, CatBoost, scikit-learn and spark models)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# visualize the first prediction's explanation (use matplotlib=True to avoid Javascript)
st_shap(shap.force_plot(explainer.expected_value, shap_values[0,:], X.iloc[0,:]))

# visualize the training set predictions
st_shap(shap.force_plot(explainer.expected_value, shap_values, X), 400)
