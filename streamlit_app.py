# app.py
import streamlit as st
import pandas as pd
import json


def process_file(uploaded_file):
    # Read the uploaded file
    matches = json.load(uploaded_file)

    # Normalize the JSON using pandas
    data = pd.json_normalize(matches)

    # ==================================
    # Gathering the Data
    # ==================================

    # We are going to pull apart each type of "like" you can receive on the app from the
    # messy JSON file that Hinge sends us.
    # Basically, the logic I'm using is as follows:
    #
    # - If "like" is not null, and "match" is not null, then this is where we sent a like and got a match.
    # - If "like" is not null, and "match" is null, then this is where we sent a like and got no match.
    # - If "match" is not null, and "like" is null, then this is where we received a like and got a match.
    # - If "match" is null, and "like" is null, then this is where we redeived a like but did not match.

    # Get data
    outgoing_matches = data.loc[(data["like"].isna() == False) & (data["match"].isna() == False)].reset_index()
    outgoing_no_matches = data.loc[(data["like"].isna() == False) & (data["match"].isna() == True)].reset_index()
    incoming_match = data.loc[(data["match"].isna() == False) & (data["like"].isna() == True)].reset_index()
    incoming_no_match = data.loc[(data["like"].isna() == True) & (data["match"].isna() == True)].reset_index()

    # Calculate metrics
    total_likes_received = len(incoming_match) + len(incoming_no_match)
    total_likes_sent = len(outgoing_matches) + len(outgoing_no_matches)
    total_matches = len(outgoing_matches) + len(incoming_match)
    total_paths = total_matches + len(outgoing_no_matches) + len(incoming_no_match)

    # Return the calculated stats
    return {
        "incoming_match": len(incoming_match),
        "incoming_no_match": len(incoming_no_match),
        "total_likes_received": total_likes_received,
        "percent_liked_back": len(incoming_match) / total_likes_received * 100 if total_likes_received > 0 else 0,
        "percent_rejected": len(incoming_no_match) / total_likes_received * 100 if total_likes_received > 0 else 0,
        "outgoing_matches": len(outgoing_matches),
        "outgoing_no_matches": len(outgoing_no_matches),
        "total_likes_sent": total_likes_sent,
        "percent_they_matched": len(outgoing_matches) / total_likes_sent * 100 if total_likes_sent > 0 else 0,
        "percent_they_rejected": len(outgoing_no_matches) / total_likes_sent * 100 if total_likes_sent > 0 else 0,
        "total_matches": total_matches,
        "total_paths": total_paths,
        "percent_matches_of_paths": total_matches / total_paths * 100 if total_paths > 0 else 0,
    }


def display_stats(stats):
    st.balloons()
    st.success('You did it!', icon="✅")
    st.header("Step 2: Read your results", divider="red")
    # Display the stats
    st.write("Statistics from your Hinge Matches Data:")


    

    # Likes Received Stats
    likes_received_data = {
        "Received Like, Match": [stats['incoming_match']],
        "Received Like, No Match": [stats['incoming_no_match']],
        "Total Likes Received": [stats['total_likes_received']]
    }
    
    df = pd.DataFrame(likes_received_data, index=['Stats'])

    st.table(df.T)



# Streamlit interface
st.title(":red[Hinge Matches Analysis]")
st.header("Step 1: Upload your matches.json file", divider="red")

# File uploader
uploaded_file = st.file_uploader("Upload your matches.json file", type="json")



if uploaded_file is not None:
    # Process and display the file
    stats = process_file(uploaded_file)
    display_stats(stats)
