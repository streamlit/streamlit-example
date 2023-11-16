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
    st.table(pd.DataFrame(likes_received_data, index=['Stats']).T)

    # Match / No Match % from Likes Received
    match_percent_likes_received = {
        "Match % from Likes Received": [round(stats['percent_liked_back'], 2)],
        "No Match % from Likes Received": [round(stats['percent_rejected'], 2)]
    }
    df = pd.DataFrame(match_percent_likes_received, index=['Stats']).T
    df_fmt = df.style.format("{:,.2f}")
    st.table(df)
    
    # Likes Sent Stats
    likes_sent_data = {
        "Sent Like, Match": [stats['outgoing_matches']],
        "Sent Like, No Match": [stats['outgoing_no_matches']],
        "Total Likes Sent": [stats['total_likes_sent']]
    }
    st.table(pd.DataFrame(likes_sent_data, index=['Stats']).T)

    # Match / No Match % from Likes Sent
    match_percent_likes_sent = {
        "Match % from Likes Sent": [round(stats['percent_they_matched'], 2)],
        "No Match % from Likes Sent": [round(stats['percent_they_rejected'], 2)]
    }
    st.table(pd.DataFrame(match_percent_likes_sent, index=['Stats']).T)

    

    # Total Matches and Paths Crossed
    total_matches_data = {
        "Total Matches": [stats['total_matches']],
        "Total Paths Crossed": [stats['total_paths']],
        "Matches as % of Total Paths Crossed": [round(stats['percent_matches_of_paths'], 2)]
    }
    st.table(pd.DataFrame(total_matches_data, index=['Stats']).T)

# Streamlit interface
st.title(":red[Hinge Matches Analysis]")
st.header("Step 1: Upload your matches.json file", divider="red")

# File uploader
uploaded_file = st.file_uploader("Upload your matches.json file", type="json")



if uploaded_file is not None:
    # Process and display the file
    stats = process_file(uploaded_file)
    display_stats(stats)
