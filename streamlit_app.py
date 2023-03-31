import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

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
    
cole, col1, cole, col2, cole = st.columns([0.1, 1, 0.05, 1, 0.1])
name_slider = ["Kumru"]
with col1:

    name_slider = st.selectbox("Pick your name", name_slider)

    st.write("")
    
with col2:

    try:
        name_filter = df["Name"].isin[(name_slider)]
        date_filter = df["Date"].isin[(name_slider)]

        final_df = df[name_filter & date_filter]

    except IndexError:
        st.warning("This is throwing an exception, bear with us!")

fig
