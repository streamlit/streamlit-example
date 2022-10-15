from collections import namedtuple




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
    df_features_with_dates["Finish"] = pd.to_datetime(df_features_with_dates["Date Started"], format=r'%d/%m/%Y') + pd.to_timedelta(pd.to_numeric(df_features_with_dates["Estimated Weeks"]),"W") # timedelta(weeks=3)
    df_features_with_dates["Task"] = df_features_with_dates["Feature / Module"]

    df_features_with_dates = df_features_with_dates.sort_values(by = ["Category"])


    df_features_with_dates_p1 = df_features_with_dates[df_features_with_dates["Timing"] == "Pilot"]
    df_features_with_dates_p2 = df_features_with_dates[df_features_with_dates["Timing"] == "Pilot part 2 "]
    # df_features_with_dates_p3 = df_features_with_dates[df_features_with_dates["Timing" == "Later updates"]]



    # Where no date is added
    df_without_dates = df[df["Date Started"] == ""]



    st.title('Pilot Part 1 (Goal: Allow for a non-enernite user)')

    fig1= ff.create_gantt(df_features_with_dates_p1, title  = "Overview of features for Part1", showgrid_x=True, width  = 1000,show_hover_fill = True, index_col='Category', show_colorbar=True)
    fig1.add_vline(x=datetime.today())
    st.plotly_chart(fig1, wuse_container_width = True, window_width = True)


    st.title('Pilot Part 2 (Goal: Enable enhanced functionality & Capital PV)')

    fig2 = ff.create_gantt(df_features_with_dates_p2, title  = "Overview of features planned for Part2", showgrid_x=True, width  = 1000, index_col='Category', show_hover_fill = True, show_colorbar=True)

    fig2.add_vline(x=datetime.today())
    st.plotly_chart(fig2, wuse_container_width = True, window_width = True)



    st.title('Without dates')

    st.dataframe(df_without_dates)



    return 
  


    

main_app()


    
