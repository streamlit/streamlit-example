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

customer_id_input = st.text_input('Give us your Customer id', '00007d2de826758b65a93dd24ce629ed66842531df6699338c5570910a014cc2')
N = st.slider('Number of items you want to be recommended', 0, 12, 12)

# Baseline Model
st.subheader('Baseline Model')
purchase_dict = pickle.load(open("data/purchase_dict.pkl", 'rb'))
best_ever = pickle.load(open("data/best_ever.pkl", 'rb'))
best_from_customer = purchase_dict.get(customer_id_input, {})
best_from_customer = sorted(best_from_customer.items(), key=lambda x: x[1], reverse=True)
best_from_customer = [ar_id for ar_id, count in best_from_customer]
n_bought = len(best_from_customer)
lst = []
if not n_bought:
    lst = best_ever[:N]
elif n_bought >= N:
    lst = best_from_customer[:N]
else:
    lst = best_from_customer[:n_bought]+ best_ever[:N-n_bought]
st.text(lst)

row3_1, row3_2, row3_3, row3_4, row3_5, row3_6, row3_7, row3_8, row3_9, row3_10, row3_11, row3_12 = st.columns((1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
row3=[row3_1, row3_2, row3_3, row3_4, row3_5, row3_6, row3_7, row3_8, row3_9, row3_10, row3_11, row3_12]
i=1
for element in lst:
    image = Image.open('data/articles/'+str(element)+'.jpg')
    with row3[i-1] :
        st.image(image)
    i=i+1

# Rule Based Algorithm
st.subheader('Rule Based Algorithm')

