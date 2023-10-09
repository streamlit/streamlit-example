from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st


from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules



st.title("Ini punya kelompok FRIK")

df = pd.read_csv("Data/query_result.csv")
df = df.rename(columns={'sale_order_id': 'OrderID', 'product_default_code': 'Product'})
df.head()