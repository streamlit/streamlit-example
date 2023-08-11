import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Setting up Google Sheets API authentication
def init_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    
    creds = ServiceAccountCredentials.from_json_keyfile_name(/Users/hectorstanley/Downloads/spring-395512-5bef0d0d2984.json, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Your_Google_Sheet_Name").sheet1  # Change the sheet name accordingly
    return sheet

sheet = init_sheet()

# Streamlit app starts here
st.title("Streamlit Google Sheets Integration")

# Login Page (Simple authentication for demonstration, not secure for production)
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type='password')
if username == "admin" and password == "admin":  # For demo purpose, you can integrate a proper authentication
    st.sidebar.success("Logged in successfully")

    st.header("Forms")

    form_option = st.selectbox("Select Form", ["Personal Information", "Role Information"])

    # First Form: Personal Information
    if form_option == "Personal Information":
        with st.form("personal_info"):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            role_title = st.text_input("Current Role Title")
            dev_goals = st.text_input("Development Goals")
            salary = st.number_input("Salary", value=0.0)
            submit = st.form_submit_button("Submit")

            if submit:
                sheet.append_row([first_name, last_name, role_title, dev_goals, salary])
                st.success("Data added to Google Sheet!")

    # Second Form: Role Information
    elif form_option == "Role Information":
        with st.form("role_info"):
            role_name = st.text_input("Role Name")
            start_date = st.date_input("Start Date", datetime.now())
            end_date = st.date_input("End Date", datetime.now())
            requirements = st.text_input("Requirements")
            salary = st.number_input("Role Salary", value=0.0)
            submit = st.form_submit_button("Submit")

            if submit:
                sheet.append_row([role_name, start_date, end_date, requirements, salary])
                st.success("Data added to Google Sheet!")
else:
    st.sidebar.warning("Please enter username and password")

if __name__ == "__main__":
    st.write("Welcome to the Streamlit App!")
