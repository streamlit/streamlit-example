from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

import pandas as pd
import io



"""
# Data overview
"""

customers = pd.read_csv('./customers.csv')
articles = pd.read_csv('./articles.csv')
transactions = pd.read_csv('./transactions_train.csv', parse_dates = ['t_dat'])
transactions = transactions.sort_values("t_dat")

"""
The data used to make recommendations for H&M products includes **three datasets: customers information, articles informations and transactions history**.
"""

"""
## Customers
"""

buffer = io.StringIO()
customers.info(buf=buffer)
s = buffer.getvalue()

# st.text(s)

st.write("The number of customers is", len(customers))

"An overview of the customers dataset can be found below: "
st.write(customers.head(10))

"""
## Articles
"""

buffer2 = io.StringIO()
articles.info(buf=buffer2)
s2 = buffer2.getvalue()

# st.text(s2)

st.write("The number of articles is", len(articles))
"An overview of the articles dataset can be found below: "
st.write(articles.head(10))

"""
## Transactions
"""

buffer3 = io.StringIO()
transactions.info(buf=buffer3)
s3 = buffer3.getvalue()

# st.text(s3)

st.write("The number of transactions registered is", len(transactions))
"An overview of the transactions dataset can be found below: "
st.write(transactions.head(10))

st.write("The transactions registered go from", transactions['t_dat'][0], "to", transactions['t_dat'][31788323])
st.write("One of the limitations found by the team was how big the datasets were. Therefore, we have worked with the most recent transactions, considering only one month worth of data.")

st.write("Additionally, only those transactions that involve the top 5,000 customers and the top 5,000 articles will be considered for the models.")
         
# transactions_red = transactions[31060590:31788323]

st.write("The transactions considered go from", transactions['t_dat'][31018179], "to", transactions['t_dat'][31788323])
         
#counts_df = transactions_red.groupby(['t_dat', 'customer_id', 'article_id', 'price', 'sales_channel_id']).size()
#counts_df = counts_df.to_frame()
#counts_df.reset_index(inplace=True)
#small_counts = counts_df.rename(columns={0: 'count'})
#small_counts = small_counts.sort_values('customer_id')
         
#no_transactions = len(small_counts)
#no_articles = len(pd.unique(small_counts['article_id']))
#no_customers = len(pd.unique(small_counts['customer_id']))
no_customers = 189510
no_articles = 26252
no_transactions = 727334


st.write("The dataset considered for recommendation includes a total of", no_customers, "customers, ", no_articles, "articles and ", no_transactions, "transactions.")

st.write("Even after reducing the dataset, it is representative enough of the traits and habits of the customers and, hence, will be used to generate the recommendations of articles for the customers of H&M database.")

