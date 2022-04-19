from collections import namedtuple
import altair as alt
import math
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
from PIL import Image
import pickle

import pandas as pd
import io



"""
# Data overview
"""
st.set_page_config(
    page_title="H&M Personalized Fashion Recommendations",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.subheader('H&M Personalized Fashion Recommendations')

# Put image on top
image = Image.open('data/hm-store-728.jpeg')
st.image(image)

# Read csv files
transaction_aggr = pd.read_csv("data/transaction_aggr.csv",parse_dates = ['t_dat']) 
articles_transaction_color_aggr = pd.read_csv("data/articles_transaction_color_aggr.csv")
transactions_season = pd.read_csv("data/transactions_season.csv")     
customers_age = pd.read_csv("data/customers_age.csv")       
colors_season = pd.read_csv("data/colors_season.csv")                           

st.header('Data visualization')

# Number of articles, number of customers and total volume change over the time
st.subheader('Change over time')

all_variables = ['nr_customer','nr_article','total_volume']
variables = st.multiselect(
    "Select desired variables", options=all_variables, default=all_variables
)

fig = go.Figure()

for v in variables:
    fig.add_trace(go.Scatter(mode="lines", x=transaction_aggr["t_dat"], y=transaction_aggr[v], name=v))
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

fig.update_layout(
    title_text='Change over the time' # title of plot
)
if len(variables)==1:
    fig.update_layout(
    yaxis_title=variables[0]
)
st.plotly_chart(fig)

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
#Test



# Colors
st.subheader('Colors')
X_best = st.slider('Best colors sold?', 0, 30, 10)
best_colours=articles_transaction_color_aggr.groupby('colour_group_name')['article_id'].sum().sort_values(ascending=False)
best_colours=best_colours[:X_best]
best_colours=best_colours.index.values.tolist()

articles_transaction_color_aggr=articles_transaction_color_aggr[articles_transaction_color_aggr["colour_group_name"].isin(best_colours)]
articles_transaction_color_aggr=articles_transaction_color_aggr.groupby(['month_year','colour_group_name'])['article_id'].sum().reset_index()

fig = px.bar(articles_transaction_color_aggr,x="month_year", y="article_id",color="colour_group_name",
            labels={
                     "month_year": "Month",
                     "article_id": "Number of articles sold",
                     "colour_group_name": "Colour"
                 },
            category_orders={"colour_group_name": best_colours},
            title="Number of articles sold per colour along the time")
st.plotly_chart(fig)

# Seasons
st.subheader('Seasons')
season_chosen = st.selectbox(
     'Pick a season',
     ('Spring', 'Summer', 'Autumn', 'Winter'))

# LAYING OUT THE NEXT SECTION OF THE APP
row1_1, row1_2 = st.columns((1, 1))

fig = px.pie(transactions_season.loc[transactions_season.season == season_chosen].sort_values(by = 'quantity', ascending = False).head(10),
             values='quantity', 
             names='product_type_name',
             title='<b>Top 10 Product<b>',
             color_discrete_sequence=px.colors.sequential.RdBu,
             hover_data=['product_type_name'],
             labels={'product_type_name':'Product Type Name'},
            height=450)

with row1_1:
    st.plotly_chart(fig)

fig = px.bar(transactions_season.loc[transactions_season.season == season_chosen].sort_values(by = 'quantity', ascending = False),
             y='quantity',
             x='product_type_name',
             title='<b>Sale in Descending Order<b>',
             color_discrete_sequence=px.colors.sequential.RdBu,
             hover_data=['product_type_name'],
             labels={'product_type_name':'Product Type Name'},
            height=450)

with row1_2:
    st.plotly_chart(fig)

fig = px.pie(customers_age.loc[customers_age.season == season_chosen].sort_values(by = 'quantity', ascending = False).head(10),
             values='quantity', 
             title='<b>Top Buyers<b>',
             names='age_cat',
             color_discrete_sequence=px.colors.sequential.RdBu,
             hover_data=['age_cat'],
             labels={'age_cat':'Category'},
            height=450)

row2_1, row2_2 = st.columns((1, 1))
with row2_1:
    st.plotly_chart(fig)

fig = px.bar(colors_season.loc[colors_season.season == season_chosen].sort_values(by = 'quantity', ascending = False),
             y='quantity', 
             title='<b>Most Favourite Colors in Ascending Order<b>',
             x='perceived_colour_master_name',
             color_discrete_sequence=px.colors.sequential.RdBu,
             hover_data=['perceived_colour_master_name'],
             labels={'perceived_colour_master_name':'Colour'},
            height=450)

with row2_2:
    st.plotly_chart(fig)


# Product recommendation
st.header('Product recommendation')

customer_id_input = st.text_input('Give us your Customer id', '00aba6a94a52e7f0759dca976d3dc11040e5dcbf0b54a34b0854600683693846')

# 51 : 8e0e166ba96a7d4e2fa83ebe7fed15d07c87011085831e4f221b5c2ce14faf93
# 29 : 1bfde6cd02ea3321284a057dd05c9e6460ea855b217080b94c52cdceb32687ae

N = st.slider('Number of items you want to be recommended', 0, 12, 12)


# Items bought by the customer
st.subheader('Items bought')
transactions_agg_customer = pd.read_csv("data/transactions_agg_customer.csv")  
items_bought=transactions_agg_customer[transactions_agg_customer['customer_id'] == customer_id_input]['articles'].reset_index(drop=True)[0]
items_bought = items_bought.replace("[","").replace("]","").replace(" ","").rsplit(",")
items_bought=['0' + x for x in items_bought]
items_bought=items_bought[:N]

st.text(items_bought)

row3_1, row3_2, row3_3, row3_4, row3_5, row3_6, row3_7, row3_8, row3_9, row3_10, row3_11, row3_12 = st.columns((1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
row3=[row3_1, row3_2, row3_3, row3_4, row3_5, row3_6, row3_7, row3_8, row3_9, row3_10, row3_11, row3_12]
i=1
for element in items_bought:
    image = Image.open('data/articles/'+str(element)+'.jpg')
    with row3[i-1] :
        st.image(image)
        i=i+1

# Baseline Model
st.subheader('Baseline Model')
purchase_dict = pickle.load(open("data/purchase_dict.pkl", 'rb'))
best_ever = pickle.load(open("data/best_ever.pkl", 'rb'))
best_from_customer = purchase_dict.get(customer_id_input, {})
best_from_customer = sorted(best_from_customer.items(), key=lambda x: x[1], reverse=True)
best_from_customer = [ar_id for ar_id, count in best_from_customer]
n_bought = len(best_from_customer)
pred_baseline = []
if not n_bought:
    pred_baseline = best_ever[:N]
elif n_bought >= N:
    pred_baseline = best_from_customer[:N]
else:
    pred_baseline = best_from_customer[:n_bought]+ best_ever[:N-n_bought]
pred_baseline=['0' + str(x) for x in pred_baseline]
st.text(pred_baseline)

row4_1, row4_2, row4_3, row4_4, row4_5, row4_6, row4_7, row4_8, row4_9, row4_10, row4_11, row4_12 = st.columns((1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
row4=[row4_1, row4_2, row4_3, row4_4, row4_5, row4_6, row4_7, row4_8, row4_9, row4_10, row4_11, row4_12]
i=1
for element in pred_baseline:
    image = Image.open('data/articles/'+str(element)+'.jpg')
    with row4[i-1] :
        st.image(image)
    i=i+1

# Content-Based Algorithm
st.subheader('Content-Based Algorithm')

content_df = pd.read_csv("data/content_df.csv")  
df_pred=content_df[content_df['customer_id']==customer_id_input].reset_index(drop=True)
l = df_pred['predicted_count'].nlargest(N).index.tolist()
pred_content_based=list(df_pred.iloc[l]['article_id'])
pred_content_based=['0' + str(x) for x in pred_content_based]
st.text(pred_content_based)

row5_1, row5_2, row5_3, row5_4, row5_5, row5_6, row5_7, row5_8, row5_9, row5_10, row5_11, row5_12 = st.columns((1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
row5=[row5_1, row5_2, row5_3, row5_4, row5_5, row5_6, row5_7, row5_8, row5_9, row5_10, row5_11, row5_12]
i=1
for element in pred_content_based:
    image = Image.open('data/articles/'+str(element)+'.jpg')
    with row5[i-1] :
        st.image(image)
    i=i+1

# Rule Based Algorithm
st.subheader('Rule Based Algorithm')

purchase_df = pd.read_csv("data/purchase_df.csv") 
text_file = open("data/general_pred_str.txt", "r")
general_pred_str = text_file.read()
text_file.close()

customer_id_input_16=int(customer_id_input[-16:], 16)
pred_rule_based=purchase_df[purchase_df['customer_id']==customer_id_input_16]['prediction']
pred_rule_based=list(purchase_df[purchase_df['customer_id']==customer_id_input_16]['prediction'])[0].split(" ")
if len(pred_rule_based) < N:
    for item in general_pred_str.split(" ")[:N-len(pred_rule_based)]:
        pred_rule_based.append(item)
pred_rule_based=pred_rule_based[:N]
st.text(pred_rule_based)

row6_1, row6_2, row6_3, row6_4, row6_5, row6_6, row6_7, row6_8, row6_9, row6_10, row6_11, row6_12 = st.columns((1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
row6=[row6_1, row6_2, row6_3, row6_4, row6_5, row6_6, row6_7, row6_8, row6_9, row6_10, row6_11, row6_12]
i=1
for element in pred_rule_based:
    image = Image.open('data/articles/'+str(element)+'.jpg')
    with row6[i-1] :
        st.image(image)
    i=i+1