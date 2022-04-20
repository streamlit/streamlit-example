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

# Section about data overview
st.header('Data overview')

"""
The data used to make recommendations for H&M products includes **three datasets: customers information, articles informations and transactions history**.
"""
no_customers_original = 1371980 
no_articles_original = 105542 
no_transactions_original = 31788324 
transactions_data0 = "2018-09-20"
transactions_datefinal = "2020-09-22"

st.write("The original dataset contains information about a total of", no_transactions_original, "transactions, that correspond to", no_customers_original, 
"customers and refer to a total of", no_articles_original, "articles.")

st.write(
        """    
- **Customer data** includes demographic information such as the **age** or the **postal code**, as well as information about their **H&M club membership** and how active the customer is.
- **Article data** includes detailed information about the article itself, including the **group of items** to which it belongs, the **colour**, the **graphical appearance** or the type of garment it is.
- For **each transaction**, the **customer id** and **article id** are registered, as well as the **price** of the transaction and the **channel** where it took place (shop or online). 
- The transactions registered go from **2018-09-20 to 2020-09-22.**
        """
)


# st.write("The transactions registered go from", transactions_data0, "to", transactions_datefinal)
st.write("One of the limitations found by the team was how big the datasets were. Therefore, only **one month worth of transactions** has been considered in the project. Additionally, only those transactions that involve the **top 5,000 customers** and the **top 5,000 articles** will be considered for the models.")
         
no_customers = 189510
no_articles = 26252
no_transactions = 727334

st.write("The dataset considered for recommendation includes information about a total of", no_transactions, "transactions,", no_customers, "customers, and", no_articles, "articles.")

st.write("Even after reducing the dataset, it is representative enough of the traits and habits of the customers and, hence, will be used to generate the recommendations of articles for the customers of H&M database.")


# Section about data visualization
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

# Customer segmentation
st.header('Customer Segmentation')
df_agg = pd.read_csv("data/df_agg.csv") 
df_cluster = pd.read_csv("data/df_cluster.csv")
df_agg=df_agg.reset_index(drop=True)
df_agg=df_agg.head(5000)
fig = px.scatter_3d(df_agg, x='Recency', y='Monetary', z='Frequency',
              color='Cluster', title='Visualization of customer segments in 3 dimensions: Monetary, Recency and Frequency')
st.plotly_chart(fig)


# Product recommendation
st.header('Product recommendation')

customer_id_input = st.text_input('Give us your Customer id', '8e0e166ba96a7d4e2fa83ebe7fed15d07c87011085831e4f221b5c2ce14faf93')

# 51 : 8e0e166ba96a7d4e2fa83ebe7fed15d07c87011085831e4f221b5c2ce14faf93
# 29 : 1bfde6cd02ea3321284a057dd05c9e6460ea855b217080b94c52cdceb32687ae

N = st.slider('Number of items you want to be recommended', 0, 12, 12)


# Items bought by the customer
st.subheader('Items bought')
st.write("These are the items that customer", customer_id_input, "bought in the past.")

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
st.write("The first recommendation approach was to recommend to each users the items they have bought the most in the past. In the case the user had bought less than 12 items, we would recommend the client the top selling items overall.")
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
st.write ("The second recommendation system is based on content filtering. The item recommendation to user A is based on the interests of a similar user B and on different features of the item. ")

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
st.write ("The third recommendation system combines two approaches: items previously purchased by the user and some of the most popular items.")

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