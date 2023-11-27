# app.py
import streamlit as st
import pandas as pd
import json
from datetime import datetime

def find_timestamps(data):

    # Extract all timestamps
    timestamps = []
    for entry in data:
        for action in entry.values():
            for item in action:
                timestamps.append(item['timestamp'])
                if 'like' in item:
                    timestamps.extend([like_item['timestamp'] for like_item in item['like']])
                if 'match' in item:
                    timestamps.extend([match_item['timestamp'] for match_item in item['match']])
                if 'chats' in item:
                    timestamps.extend([chat_item['timestamp'] for chat_item in item['chats']])

    # Convert timestamps to datetime objects
    timestamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f" if '.' in ts else "%Y-%m-%d %H:%M:%S") for ts in timestamps]

    # Find the oldest and most recent timestamps
    oldest_timestamp = min(timestamps)
    most_recent_timestamp = max(timestamps)

    return oldest_timestamp, most_recent_timestamp

def process_file(uploaded_file):
    # Read the uploaded file
    matches = json.load(uploaded_file)

    oldest, newest = find_timestamps(matches)
    duration_in_days = (newest - oldest).days
    years_of_data = duration_in_days / 365.25
    
    # Normalize the JSON using pandas
    data = pd.json_normalize(matches)

    """ 
    Gathering the Data
    We are going to pull apart each type of "like" you can receive on the app from the
    messy JSON file that Hinge sends us.
    Basically, the logic I'm using is as follows:
        
        - If "like" is not null, and "match" is not null, then this is where we sent a like and got a match.
        - If "like" is not null, and "match" is null, then this is where we sent a like and got no match.
        - If "match" is not null, and "like" is null, then this is where we received a like and got a match.
        - If "match" is null, and "like" is null, then this is where we redeived a like but did not match.
    """

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
        "oldest": oldest,
        "newest": newest,
        "years_of_data": years_of_data,
    }


def display_stats(stats):
    st.balloons()
    st.success('You did it!', icon="✅")
    st.divider()
    st.header("Step 2: Read your results", divider="grey")
    div_color = "violet"

    # green
    st.markdown("""
        <style>
        .number-highlight-green {
            background-color: #4CAF50; /* Green background */
            border-radius: 10px;       /* Rounded corners */
            color: white;              /* White text color */
            padding: 0px 5px;         /* Some padding */
            font-weight: bold;         /* Make the number bold */
            display: inline-block;     /* Align inline with the text */
            margin-left: 5px;          /* Space from the preceding text */
        }
        </style>
        """, unsafe_allow_html=True
    )

    # red
    st.markdown("""
        <style>
        .number-highlight-red {
            background-color: #FF0000; /* Green background */
            border-radius: 10px;       /* Rounded corners */
            color: white;              /* White text color */
            padding: 0px 5px;         /* Some padding */
            font-weight: bold;         /* Make the number bold */
            display: inline-block;     /* Align inline with the text */
            margin-left: 5px;          /* Space from the preceding text */
        }
        </style>
        """, unsafe_allow_html=True
    )

    # no background
    st.markdown("""
        <style>
        .number-highlight-nb {
            
            border-radius: 10px;       /* Rounded corners */
            
            padding: 0px 5px;         /* Some padding */
            font-weight: bold;         /* Make the number bold */
            display: inline-block;     /* Align inline with the text */
            margin-left: 5px;          /* Space from the preceding text */
        }
        </style>
        """, unsafe_allow_html=True
    )

    
    # YEARS OF DATA
    st.header(":violet[Years of Data]")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Oldest:")
        st.write("Most Recent:")
        st.write("Years of Data:")
    with col2:
        st.write(stats["oldest"])
        st.write(stats["newest"])
        years_of_data = stats["years_of_data"]
        st.write(round(stats["years_of_data"], 2))

    
    # LIKES RECEIVED
    st.header(":violet[Likes Received]")
    with st.container():
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Item", divider=div_color)
            st.write("Received Like, You Matched")
            st.write("Received Like, You Rejected")
            st.markdown("**Total Likes Recieved**")
        
        with col2:
            st.subheader("Number", divider=div_color)
            st.markdown(f'<span class="number-highlight-green">{stats["incoming_match"]:,}</span>', unsafe_allow_html=True)
            st.markdown(f'<span class="number-highlight-red">{stats["incoming_no_match"]:,}</span>', unsafe_allow_html=True)
            st.markdown(f'<span class="number-highlight-nb">{stats["total_likes_received"]:,}</span>', unsafe_allow_html=True)

        with col3:
            st.subheader("% of Received", divider=div_color)
            st.markdown(f'<span class="number-highlight-nb">{stats["incoming_match"] / stats["total_likes_received"]:.0%}</span>', unsafe_allow_html=True)
            st.markdown(f'<span class="number-highlight-nb">{stats["incoming_no_match"] / stats["total_likes_received"]:.0%}</span>', unsafe_allow_html=True)


    # LIKES SENT
    st.divider()
    st.header(":violet[Likes Sent]")
    with st.container():
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Item", divider=div_color)
            st.write("Sent Like, They Matched")
            st.write("Sent Like, They Rejected")
            st.markdown("**Total Likes Sent**")
        
        with col2:
            st.subheader("Number", divider=div_color)
            st.markdown(f'<span class="number-highlight-green">{stats["outgoing_matches"]:,}</span>', unsafe_allow_html=True)
            st.markdown(f'<span class="number-highlight-red">{stats["outgoing_no_matches"]:,}</span>', unsafe_allow_html=True)
            st.markdown(f'<span class="number-highlight-nb">{stats["total_likes_sent"]:,}</span>', unsafe_allow_html=True)
        
        with col3:
            st.subheader("% of Sent", divider=div_color)
            st.markdown(f'<span class="number-highlight-nb">{stats["outgoing_matches"] / stats["total_likes_sent"]:.0%}</span>', unsafe_allow_html=True)
            st.markdown(f'<span class="number-highlight-nb">{stats["outgoing_no_matches"] / stats["total_likes_sent"]:.0%}</span>', unsafe_allow_html=True)

    # GRAND TOTALS
    st.divider()
    st.header(":violet[Grand Totals]")
    with st.container():
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Item", divider=div_color)
            st.write("Total Matches")
            st.write("Total Paths Crossed")

        with col2:
            st.subheader("Number", divider=div_color)
            st.markdown(f'<span class="number-highlight-nb">{stats["total_matches"]:,}</span>', unsafe_allow_html=True)
            st.markdown(f'<span class="number-highlight-nb">{stats["total_paths"]:,}</span>', unsafe_allow_html=True)

        with col3:
            st.subheader("% of Paths", divider=div_color)
            st.markdown(f'<span class="number-highlight-nb">{stats["total_matches"] / stats["total_paths"]:.0%}</span>', unsafe_allow_html=True)

    st.write("")
    st.write("TradeMarkRobery")
    st.write("MRJ")

# Streamlit interface
st.title(":violet[Hinge Matches Analysis]")
st.header("Step 1: Upload your matches.json file", divider="grey")

# File uploader
uploaded_file = st.file_uploader("Upload your matches.json file", type="json")

if uploaded_file is not None:

    # Process the file then display stats 
    stats = process_file(uploaded_file)
    display_stats(stats)
