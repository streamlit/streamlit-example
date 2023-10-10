import math
import pandas as pd
import streamlit as st
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
st.title("Cross Selling Recommendation")

st.text("Improving revenue by upselling shrimp input product")

st.header("Association Rule")
st.subheader("Transaction behavior")
df = pd.read_csv("Data/raw_data_v2.csv")
df.product_default_code = df.product_subcategory + ': ' + df.product_default_code
df = df.rename(columns={'sale_order_id': 'OrderID', 'product_default_code': 'Product'})

st.write(df)

# Convert the data into a one-hot encoded format
oht = df.groupby(['OrderID', 'Product'])['Product'].count().unstack().fillna(0)
oht = (oht > 0).astype(int)
# print(oht)
# # Run Apriori algorithm to find frequent item sets
# frequent_itemsets = apriori(oht, min_support=0.5, use_colnames=True)
frequent_itemsets = apriori(oht,
                            min_support = 0.001,
                            max_len = 2,
                            use_colnames = True)
frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].map(lambda x:set(x)) 
print(frequent_itemsets)
# # Generate association rules
rules = association_rules(frequent_itemsets, metric='lift', min_threshold=1.0)
rules = rules.sort_values(by=['confidence'],ascending=False)

# Display the frequent item sets and association rules
st.write("Frequent Item Sets:")
st.write(frequent_itemsets)


st.write("\nAssociation Rules:")
# rules["antecedents"] = rules["antecedents"].map(lambda x:set(x))
product_name = rules['antecedents'].unique()
dropdown = st.selectbox('Select product to check', product_name)
rules_selected = rules["consequents"].loc[rules["antecedents"] == dropdown]
st.write(rules_selected.map(lambda x:set(x)) )
