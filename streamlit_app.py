import streamlit as st

import numpy as np
import pandas as pd
import datetime as dt
import json
import csv
import openpyxl

df = pd.read_excel('crossMeetings.xlsx')

# str format todays date
today_date = dt.datetime.today().strftime('%d/%m/%Y')


today_date_dt = dt.datetime.strptime(today_date, '%d/%m/%Y').date()
today_date_week_number = today_date_dt.strftime('%U')

# add a week column
df["Date"] = pd.to_datetime(df['Date'],format="%d/%m/%Y")
df['Week'] = df['Date'].dt.strftime('%U')

df['Date'].dt.strftime('%d/%m/%Y')

# add a week column
df['Week'] = df['Date'].dt.strftime('%U')

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

people = [
 'furkan berkan gulkan',
 'dilara sahan',
 'berkay gemici',
 'mehmet kocer',
 'caglar erdiz',
 'eda ayse gurbuz',
 'sarp ali saygi',
 'irem kandemir',
 'ugurcan muftuoglu',
 'mehmet tuzcu',
 'narges valipour',
 'yunus emre yildiz',
 'safak baris',
 'emir efe erez',
 'ragip yusuf yilmaz',
 'aylin akdemir',
 'haktan kocyigit',
 'onur kuyucu',
 'erkin akgoz',
 'vahit kuruosman',
 'onur kodakoglu',
 'ugur caglayan',
 'laelae win',
 'selin durmus',
 'cansu belek cagri',
 'yetkin aydemir',
 'kumru orkun']

cole, col1, cole, col2, cole = st.columns([0.1, 1, 0.05, 1, 0.1])
name_slider = people


with col1:

    checkbox_values = {}

    # Make checkbox for corresponding person
    selected_person = st.selectbox("Pick your name", name_slider)

    # If a name has been selected, display a text input
    for count, person in enumerate(people):
        if selected_person == person :
            
                condition1 = (df['Week'] == today_date_week_number)
                condition2 = (df['A'] == selected_person)
                condition3 = (df['B'] == selected_person)

                budy1 = df.loc[condition1 & condition2, 'B']
                budy2 = df.loc[condition1 & condition3, 'A']

                st.write(f"You selected: {person}")

                if not budy1.empty and not budy2.empty:
                    st.write(f"Today is {today_date} this week you should make a meeting with {budy1.values} {budy2.values}")
                elif not budy1.empty:
                    st.write(f"Today is {today_date} this week you should make a meeting with {budy1.values}")
                elif not budy2.empty:
                    st.write(f"Today is {today_date} this week you should make a meeting with {budy2.values}")
                else:
                    st.write("No meeting")


                # Display a text input for the user to enter their data
                input_data = st.text_input("Did the meeting take place? You can write 'OK'")

    # Add a button to submit the data
    if st.button("Submit"):
        if input_data == 'OK':
            with open("data.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([selected_person, input_data, today_date_week_number, today_date])
            st.success("Data submitted!")
        else: st.warning('You have to write "OK"')

with col2:
        st.balloons()
