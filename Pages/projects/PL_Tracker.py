import requests
import streamlit as st

def get_premier_league_standings():
    url = "https://api.example.com/premier_league/standings"  # Replace with the actual API URL
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Fetch Premier League standings
standings_data = get_premier_league_standings()

if standings_data:
    st.title("Premier League Football Tracker")
    st.subheader("Current Standings")

    # Display the standings data in a table
    st.write(standings_data)
else:
    st.error("Failed to retrieve data. Please check the data source.")