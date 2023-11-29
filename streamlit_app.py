import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from utils import bin_packing_fair_seeding, schedule_matches, schedule_matches_v1, schedule_to_dataframe, schedule_matches_mip, filter_dataframe   # import your function
import importlib.util
if importlib.util.find_spec("openpyxl") is None:
    st.error("openpyxl is not installed. Please install it to continue.")


# Streamlit UI components
st.title('Tournament Scheduling Application')

# File upload
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Read the uploaded Excel file
    data = pd.read_excel(uploaded_file)

    #show the data to the user
    st.write('Uploaded Data (This only shows a sinppet of the data):...')
    st.dataframe(data.head())

    # Drop the header row and reset the index for a clean dataframe
    data = data.drop(0).reset_index(drop=True)

    # Convert columns to numeric for sorting
    data['Average Points'] = pd.to_numeric(data['Unnamed: 10'])
    data['Player1 Rank'] = pd.to_numeric(data['Unnamed: 4'])

    # Extract team information (Team Name and Average Rank)
    teams_info_rank = list(zip(data['Unnamed: 9'], data['Average Points']))


    # User inputs for scheduling
    group_size = st.slider('Select Group Size', 2, 10, 3)  # Adjust the range as needed
    match_duration = st.slider('Match Duration (in minutes)', 20, 120, 30)
    num_courts = st.slider('Number of Courts', 1, 10, 2)

    if st.button('Generate Schedule'):
        # Seeding teams into groups
        groups = bin_packing_fair_seeding(teams_info_rank, group_size)

        #display the groups to the user
        display_groups = groups
        flattened_data = []
        for group_number, group in enumerate(groups, start=1):
            for team in group:
                team_name, points = team
                flattened_data.append({"Group Number": group_number, "Team Name": team_name, "Points": points})
        
        df_groups = pd.DataFrame(flattened_data)
        
        # Display the DataFrame
        st.write('Generated groups ....')
        st.dataframe(df_groups)


        # Defining available times (this could also be user input)
        available_times = {
    "Thursday": [(datetime(2023, 11, 23, 18, 0), datetime(2023, 11, 23, 23, 59))],
    "Friday": [(datetime(2023, 11, 24, 14, 0), datetime(2023, 11, 24, 20, 0))],
    "Saturday": [(datetime(2023, 11, 25, 14, 0), datetime(2023, 11, 25, 22, 0))]
}

        # Generating the schedule
        scheduled_matches = schedule_matches(groups, available_times, match_duration, num_courts)
        scheduled_matches_v1 = schedule_matches_v1(groups, available_times, match_duration, num_courts)
        scheduled_matches_mip = schedule_matches_mip(groups, available_times, match_duration, num_courts)

        # Convert schedule to DataFrame - Original
        st.title('Original version of the schedule')
        schedule_df = schedule_to_dataframe(scheduled_matches)
        st.write('Generated Schedules ...')
        st.dataframe(filter_dataframe(schedule_df, 'schedule_df'))

        # Convert schedule to DataFrame - V1
        st.title('version 1 of the schedule')
        schedule_df_v1 = schedule_to_dataframe(scheduled_matches_v1)
        st.write('Generated Schedules ...')
        st.dataframe(filter_dataframe(schedule_df_v1, 'schedule_df_v1'))
        


        # Convert schedule to DataFrame - mip
        # add mip scheduling
        st.title('version mip of the schedule')
        schedule_df_mip = schedule_to_dataframe(scheduled_matches_mip)
        st.write('Generated Schedules ...')
        st.dataframe(filter_dataframe(schedule_df_mip, 'schedule_df_mip'))
