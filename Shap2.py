import shap
import streamlit as st
import streamlit.components.v1 as components
import xgboost

@st.cache
def load_data():
    return shap.datasets.boston()

def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)

st.title("SHAP in Streamlit")

# train XGBoost model
X,y = load_data()
model = xgboost.train({"learning_rate": 0.01}, xgboost.DMatrix(X, label=y), 100)

# explain the model's predictions using SHAP
# (same syntax works for LightGBM, CatBoost, scikit-learn and spark models)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# visualize the first prediction's explanation (use matplotlib=True to avoid Javascript)
st_shap(shap.force_plot(explainer.expected_value, shap_values[0,:], X.iloc[0,:]))

# visualize the training set predictions
st_shap(shap.force_plot(explainer.expected_value, shap_values, X), 400)
