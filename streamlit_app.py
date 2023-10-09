from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st


from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

from google.colab import files
import io

st.title("Ini punya kelompok FRIK")

df = pd.read_csv("queryresult(2).csv")
df = df.rename(columns={'sale_order_id': 'OrderID', 'product_default_code': 'Product'})
df.head()