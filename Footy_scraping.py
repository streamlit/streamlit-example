import streamlit as st

st.set_page_config(
    page_title="Footy data scraping",
    page_icon="📊",
)

st.write("# Welcome to Footy Scraping! 👋")

st.markdown(
    """
    Use this app to scrape a variety of footy statistics from various sources.
    
    **👈 Select a source from the sidebar**
    
    ### Instructions
    
    Input your scraping parameters and press 'scrape'. After a few seconds, the data 
    should appear. This app will allow you to make changes just like you would in excel!
    After you have reviewed the data, press 'download' to download data as a .csv 
"""
)