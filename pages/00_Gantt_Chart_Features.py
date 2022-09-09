from collections import namedtuple
from turtle import window_width
import altair as alt
import math
import pandas as pd
import streamlit as st

import plotly.express as px


import pandas as pd
import gspread

import datetime
import plotly.figure_factory as ff
from datetime import datetime, date, timedelta

st.set_page_config(layout="wide")

def main_app():


    credentials = {
                        "type": st.secrets.credentials["type"],
                        "project_id": st.secrets.credentials["project_id"],
                        "private_key_id": st.secrets.credentials["private_key_id"],
                        "private_key": st.secrets.credentials["private_key"], 
                        "client_email": st.secrets.credentials["client_email"], 
                        "client_id": st.secrets.credentials["client_id"], 
                        "auth_uri": st.secrets.credentials["auth_uri"], 
                        "token_uri": st.secrets.credentials["token_uri"], 
                        "auth_provider_x509_cert_url": st.secrets.credentials["auth_provider_x509_cert_url"], 
                        "client_x509_cert_url": st.secrets.credentials["client_x509_cert_url"]
                        }

    # gc = gspread.service_account(filename='Authentification\key_google.json')
    # gc = gspread.service_account(credentials)
    gc = gspread.service_account_from_dict(credentials)


    sps = gc.open('Product Portfolio Planning')
        # product_feedback = sps.get_worksheet_by_id(1479889959)
    features_list = sps.get_worksheet_by_id(1779994857)


    

    
    data = features_list.get_all_values()

    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)


    # st.write(df)
    df_features_with_dates = df[df["Date Started"] != ""]
    df_features_with_dates["Start"] = pd.to_datetime(df_features_with_dates["Date Started"], format=r'%d/%m/%Y')
    df_features_with_dates["Finish"] = pd.to_datetime(df_features_with_dates["Date Started"], format=r'%d/%m/%Y') + timedelta(weeks=3)
    df_features_with_dates["Task"] = df_features_with_dates["Feature / Module"]

    df_features_with_dates = df_features_with_dates.sort_values(by = ["Category"])

    print(df_features_with_dates)

    # st.write(df_features_with_dates)

    

    fig = ff.create_gantt(df_features_with_dates, title  = "Overview of features planned and in progress", showgrid_x=True, width  = 1000,show_hover_fill = True, index_col='Main type of work needed', show_colorbar=True)


    fig.add_vline(x=datetime.today())



    st.plotly_chart(fig, wuse_container_width = True, window_width = True)



    return 
  


    

main_app()


    
