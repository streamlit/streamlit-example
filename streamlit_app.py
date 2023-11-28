import streamlit as st
import pandas as pd
from utils import bin_packing_fair_seeding  # import your function
from utils import schedule_matches  # import your function
from utils import schedule_to_dataframe  # import your function

# Streamlit UI components
st.title('Tournament Scheduling Application')

# File upload
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)  # Adjust if a different format is used

    # Process the file to extract teams and their rankings
    # Assuming a specific format; adjust as necessary
    teams_info_rank = list(zip(data['Team Name Column'], data['Rank Column']))

    # User inputs for scheduling
    group_size = st.slider('Select Group Size', 2, 10, 3)  # Adjust the range as needed
    match_duration = st.slider('Match Duration (in minutes)', 20, 120, 30)
    num_courts = st.slider('Number of Courts', 1, 10, 2)

    if st.button('Generate Schedule'):
        # Seeding teams into groups
        groups = bin_packing_fair_seeding(teams_info_rank, group_size)

        # Defining available times (this could also be user input)
        available_times = {
            # Provide a way for the user to input available times
        }

        # Generating the schedule
        scheduled_matches = schedule_matches(groups, available_times, match_duration, num_courts)

        # Convert schedule to DataFrame
        schedule_df = schedule_to_dataframe(scheduled_matches)
        st.dataframe(schedule_df)
