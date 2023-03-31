import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.graph_objs as go

# The code below is for the title and logo for this page.
st.set_page_config(page_title="Cross Feedback Meetings", page_icon="🥡")

#st.image(
#    "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/takeout-box_1f961.png",
#    width=160,
#)

st.title("Cross Feedback Meetings")

st.write("")

st.markdown(
    """
"""
)
st.markdown(
    """
    This demo should use instead of this [Cross Feedback Excel](https://teams.microsoft.com/l/channel/19%3A05485c82202648f6b0ee6e199da8203a%40thread.tacv2/tab%3A%3A2dce3841-c6b0-4d5c-a2a0-f1c49c5cbcb6?groupId=b28b8e6b-822e-4a1b-9687-eef1c204fe8e&tenantId=46c4de19-0ffc-4c54-aa86-ee7274afa9d7&allowXTenantAccess=false).
"""
)

with st.expander("About this app"):

    st.write("")

    st.markdown(
        """
This app deployed for a Module in d3c community which named Cross Feedback

We will evaluate this module with several phases.  First phase will take 7 weeks. During cross feedback sessions is proceeding, Mentors will get feedbacks about this module from yours. 
 
Structure :
 

Every community member will match whole community members in different weeks.
This sessions should  be planned as 10 minutes.
Creators in crossfeedback calendar, will create meeting at specified week.
Date in crossfeedback calendar represents first day of week. Creators should create sessions with members whom to attended.
Important Structure Thing: Please talk any case that make you disturbing. This is the main purpose that we organized these sessions.
"""
    )

    st.write("")

    st.markdown(
        """
For more information abaout d3c calture please visit [this wiki page](https://confluence.nttdata-solutions.com/x/kLggCQ).
    """
    )

    st.write("")

# loading dataset XLSX
df = pd.read_excel("datasets/relay-foods.xlsx", sheet_name=1)

df["OrderPeriod"] = df.OrderDate.apply(lambda x: x.strftime("%Y-%m"))
df.set_index("UserId", inplace=True)

df["CohortGroup"] = (
    df.groupby(level=0)["OrderDate"].min().apply(lambda x: x.strftime("%Y-%m"))
)
df.reset_index(inplace=True)
# df.head()

# loading dataset CSV
relay_foods_csv = pd.read_csv("datasets/relay-foods.csv")

with st.expander("Show the `Food` dataframe"):
    st.write(relay_foods_csv)

grouped = df.groupby(["CohortGroup", "OrderPeriod"])

# count the unique users, orders, and total revenue per Group + Period
cohorts = grouped.agg(
    {"UserId": pd.Series.nunique, "OrderId": pd.Series.nunique, "TotalCharges": np.sum}
)

# make the column names more meaningful
cohorts.rename(columns={"UserId": "TotalUsers", "OrderId": "TotalOrders"}, inplace=True)
cohorts.head()


def cohort_period(df):
    """
    Creates a `CohortPeriod` column, which is the Nth period based on the user's first purchase.
    """
    df["CohortPeriod"] = np.arange(len(df)) + 1
    return df


with st.form("my_form"):
    # st.write("Inside the form")
    # slider_val = st.slider("Form slider")
    # checkbox_val = st.checkbox("Form checkbox")

    cole, col1, cole = st.columns([0.1, 1, 0.1])

    with col1:

        TotalCharges_slider = st.slider(
            "Total Charges (in $)", step=50, min_value=2, max_value=690
        )
        # Every form must have a submit button.

    submitted = st.form_submit_button("Refine results")

# st.write("slider", slider_val, "checkbox", checkbox_val)

cohorts = cohorts[cohorts["TotalCharges"] > TotalCharges_slider]

cohorts = cohorts.groupby(level=0).apply(cohort_period)
cohorts.head()

# reindex the DataFrame
cohorts.reset_index(inplace=True)
cohorts.set_index(["CohortGroup", "CohortPeriod"], inplace=True)

# create a Series holding the total size of each CohortGroup
cohort_group_size = cohorts["TotalUsers"].groupby(level=0).first()
cohort_group_size.head()

user_retention = cohorts["TotalUsers"].unstack(0).divide(cohort_group_size, axis=1)
user_retention.head(10)

user_retention[["2009-06", "2009-07", "2009-08"]].plot(figsize=(10, 5))
plt.title("Cohorts: User Retention")
plt.xticks(np.arange(1, 12.1, 1))
plt.xlim(1, 12)
plt.ylabel("% of Cohort Purchasing")
cohorts["TotalUsers"].head()

user_retention = cohorts["TotalUsers"].unstack(0).divide(cohort_group_size, axis=1)
user_retention.head(10)

user_retention[["2009-06", "2009-07", "2009-08"]].plot(figsize=(10, 5))
plt.title("Cohorts: User Retention")
plt.xticks(np.arange(1, 12.1, 1))
plt.xlim(1, 12)
plt.ylabel("% of Cohort Purchasing")

user_retention = user_retention.T

fig = go.Figure()

fig.add_heatmap(
    x=user_retention.columns,
    y=user_retention.index,
    z=user_retention,
    # colorscale="Reds",
    # colorscale="Sunsetdark",
    colorscale="Redor"
    # colorscale="Viridis",
)

fig.update_layout(title_text="Monthly cohorts showing retention rates", title_x=0.5)
fig.layout.xaxis.title = "Cohort Group"
fig.layout.yaxis.title = "Cohort Period"
fig["layout"]["title"]["font"] = dict(size=25)
fig.layout.plot_bgcolor = "#efefef"  # Set the background color to white
fig.layout.width = 750
fig.layout.height = 750
fig.layout.xaxis.tickvals = user_retention.columns
fig.layout.yaxis.tickvals = user_retention.index
fig.layout.margin.b = 100
fig
