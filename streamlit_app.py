import streamlit as st
from datetime import datetime,date,timedelta
import pandas as pd
import requests



def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}
@st.cache
def fetch_analytics(session, start_date, end_date):
    data = fetch(session,f"""http://localhost:8000/analytics/?start={start_date}&end={end_date}""")
    return data

def main():
    st.set_page_config(page_title="Pocketed Metrics Dashboard",layout='wide', initial_sidebar_state='expanded')
    session = requests.Session()
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


    today = datetime.today()
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(days=7)
    



    st.sidebar.header('Pocketed Analytics')

    


    st.sidebar.markdown('''
    ---
    # Quarterly Goals
    ''')
    
    st.sidebar.markdown("Objective 1: $65K B2C SaaS Revenue")
    st.sidebar.markdown("Objective 2: $40K B2C Service Revenue")
    st.sidebar.markdown("Objective 3: $15K B2B SaaS Revenue")
    # data_total = fetch_analytics(session,start_of_pocketed,end_date) 

    

    since, total = st.tabs(["Date Range","Total"])
    
    

    with since:

        start_date = st.date_input('Start date:', last_week) 
        end_date = st.date_input('End date:', yesterday, key='2') 
        # add a day so that it's inclusive of input date
        end_date = end_date + timedelta(days=1)
        # fetch data
        data = fetch_analytics(session,start_date,end_date) 
        # display metrics using data
        display_metrics(data,start_date, end_date)

    with total:
        start_of_pocketed = date(2020,1,1)
        end_date = st.date_input('End date:', yesterday, key='1') 
        # add a day so that it's inclusive of input date
        end_date = end_date + timedelta(days=1)
        data = fetch_analytics(session, start_of_pocketed, end_date)
        # display metrics using data
        display_metrics(data, "January 1st 2020", end_date)

    


def display_metrics(data, start_date, end_date):
    users = data.get('users')
    referral_users = data.get('referrals')
    free_trial_starts = data.get('free_trials')
    free_trial_cancellations = data.get('free_trial_cancellations')
    free_trial_conversions = data.get('free_trial_conversions')
    basic_subscriptions = data.get("basic_subscriptions")
    pplus_subscriptions = data.get('pplus_subscriptions')
    concierge_subscriptions = data.get('concierge_subscriptions')
    total_active_subscriptions = data.get('total_active_subscriptions')
    new_user_conversion = data.get("new_user_conversion")
    churn = data.get("churn")
    saas_cad = data.get("saas_cad")
    saas_usd = data.get("saas_usd")
    service_cad = data.get("service_cad")
    service_usd = data.get("service_usd")
    st.success(f""" Between: {start_date} at 00:00 AND {end_date} at 00:00""")
    # Row A
    st.markdown('### User Metrics')
    
    col0, col1,  = st.columns(2)
    col0.metric("Users", users)
    col1.metric("Users with referral code", referral_users)
    
    st.markdown('### Free Trial Metrics')
    col2, col3, col4 = st.columns(3)
    col2.metric("Free Trial Starts", free_trial_starts)
    col3.metric("Free Trial Cancellations", free_trial_cancellations)
    col4.metric("Free Trial Conversions", free_trial_conversions)

    # st.text(f""" Since: {time_period}""")
    st.markdown('### General Saas Metrics')
    col5a, col5b, col5c = st.columns(3)
    col5a.metric("Total Active Subscriptions", total_active_subscriptions)
    col5b.metric("New User Conversion", f"{new_user_conversion}%")
    col5c.metric("Churn", f"{churn}%")
    st.markdown('Active Subscriptions')
    
    col5, col6, col7 = st.columns(3)
    col5.metric("Basic Subscriptions", basic_subscriptions)
    col6.metric("Pocketed+ Subscriptions", pplus_subscriptions)
    col7.metric("Concierge Subscriptions", concierge_subscriptions)

    st.markdown('Revenue')
    col8, col9, col10, col11 = st.columns(4)
    col8.metric("CAD SaaS Revenue", f"${saas_cad}CAD")
    col9.metric("USD SaaS Revenue", f"${saas_usd}")
    col10.metric("CAD Service Revenue", f"${service_cad}CAD")
    col11.metric("USD Service Revenue", f"${service_usd}")

    
    

def set_time_on_date(date):
    end_date_with_time = datetime.combine(date, datetime.min.time())
    end_of_day_date = end_date_with_time.replace(hour=11, minute=59)
    return end_of_day_date

if __name__ == '__main__':
    main()
# c1, c2 = st.columns((7,3))
# with c1:
#     st.markdown('### Heatmap')
#     plost.time_hist(
#     data=seattle_weather,
#     date='date',
#     x_unit='week',
#     y_unit='day',
#     color=time_hist_color,
#     aggregate='median',
#     legend=None,
#     height=345,
#     use_container_width=True)
# with c2:
#     st.markdown('### Donut chart')
#     plost.donut_chart(
#         data=stocks,
#         theta=donut_theta,
#         color='company',
#         legend='bottom', 
#         use_container_width=True)

# # Row C
# st.markdown('### Line chart')
# st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)