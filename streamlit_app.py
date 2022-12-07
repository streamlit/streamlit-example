import streamlit as st
import pandas as pd
import requests
import plost


def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

def main():
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    session = requests.Session()
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
    st.sidebar.header('Pocketed Analytics')

    
    time_period = st.sidebar.date_input('Figures since:') 


    st.sidebar.markdown('''
    ---
    Created with ❤️ by [Donal](https://github.com/donaldev).
    ''')

    data = fetch(session,f"""http://localhost:8000/analytics/?since={time_period}""")
    print(data)
    referral_users = data.get('referral_users')
    free_trial_starts = data.get('free_trial_starts')
    free_trial_cancellations = data.get('free_trial_canceled_subs')
    free_trial_conversions = data.get('free_trial_conversions')
    pplus_conversions = data.get('pplus_subscriptions')
    # Row A
    st.markdown('### User Metrics')
    st.text(f""" Since: {time_period}""")
    col1, col2, col3 = st.columns(3)
    col1.metric("Users with referral code", referral_users)
    col2.metric("Free Trial Starts", free_trial_starts)
    col3.metric("Free Trial Cancellations", free_trial_cancellations)
    # st.markdown('### Saas Purchase Metrics')
    # st.text(f""" Since: {time_period}""")
    
    col4,col5 = st.columns(2)
    col4.metric("Free Trial Conversions", free_trial_conversions)
    col5.metric("Pocketed+ Conversions", pplus_conversions)
    # col5.metric("Pocketed+ ", "24")
    # col6.metric("Pocketed Concierge ", 0)

    # st.text(f""" Referral Users: {referral_users}""")
    # st.text(f""" Free Trial Starts: {free_trial_starts}""")
    # st.text(f""" Free Trial Cancellations: {free_trial_cancellations}""")
    # st.text(f""" Free Trial Cancellations: {free_trial_conversions}""")



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