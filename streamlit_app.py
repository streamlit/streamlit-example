from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st


from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules



st.title("Cross Selling Recommendation")

st.text("Improving revenue by upselling shrimp input product")

st.header("Association Rule")
st.subheader("transaction behavior")
df = pd.read_csv("Data/query_result.csv")
df = df.rename(columns={'sale_order_id': 'OrderID', 'product_default_code': 'Product'})
st.write(df)