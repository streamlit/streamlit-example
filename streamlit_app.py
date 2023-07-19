import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Sample data
data = {
    "erpJobOperationRunId": {
        "0": "G9018-1-000900-0003-1313",
        "1": "G9018-1-000900-0005-1625",
        "2": "G9018-1-001000-0002-0600",
        "3": "G9010-1-000200-0007-1555",
        "4": "G9010-1-000200-0004-1608"
    },
    "erpMachineId": {
        "0": "C001",
        "1": "C001",
        "2": "C001",
        "3": "C001",
        "4": "C001"
    },
    "jobName": {
        "0": "G9018-1",
        "1": "G9018-1",
        "2": "G9018-1",
        "3": "G9010-1",
        "4": "G9010-1"
    },
    "operator": {
        "0": "Shawn Couvillion",
        "1": "Robert Allison",
        "2": "Shawn Couvillion",
        "3": "Robert Allison",
        "4": "Shawn Couvillion"
    },
    "operationName": {
        "0": "000900",
        "1": "000900",
        "2": "001000",
        "3": "000200",
        "4": "000200"
    },
    "partName": {
        "0": "84E902045G6",
        "1": "84E902045G6",
        "2": "84E902045G6",
        "3": "84E902045G6",
        "4": "84E902045G6"
    },
    "startAt": {
        "0": 1687194780000,
        "1": 1687206300000,
        "2": 1687255200000,
        "3": 1687290900000,
        "4": 1687291680000
    },
    "endAt": {
        "0": 1687206600000,
        "1": 1687240800000,
        "2": 1687291680000,
        "3": 1687312800000,
        "4": 1687293000000
    }
}

# Convert to DataFrame
df = pd.DataFrame(data)
df["startAt"] = pd.to_datetime(df["startAt"], unit='ms')
df["endAt"] = pd.to_datetime(df["endAt"], unit='ms')

# Check for overlaps and assign colors
df['color'] = 'green'
for i in range(len(df)):
    for j in range(len(df)):
        if i != j and df.iloc[i]['startAt'] < df.iloc[j]['endAt'] and df.iloc[i]['endAt'] > df.iloc[j]['startAt']:
            df.at[i, 'color'] = 'red'

# Streamlit App
st.title("Operator Run Debugger")

# Display Gantt chart
selected_run = st.plotly_chart(px.timeline(df, x_start="startAt", x_end="endAt", y="erpJobOperationRunId", color='color', title="Gantt Chart with Overlapping Operator Runs"), use_container_width=True)

# If a bar (operator run) is selected
if selected_run:
    run_id = selected_run["points"][0]["y"]
    selected_df = df[df["erpJobOperationRunId"] == run_id]

    # Display the details in input fields for editing
    erp_id = st.text_input("erpJobOperationRunId", selected_df["erpJobOperationRunId"].iloc[0])
    operator = st.text_input("Operator", selected_df["operator"].iloc[0])
    start_at = st.text_input("Start At", selected_df["startAt"].iloc[0].strftime('%Y-%m-%d %H:%M:%S'))
    end_at = st.text_input("End At", selected_df["endAt"].iloc[0].strftime('%Y-%m-%d %H:%M:%S'))

    # Save changes
    if st.button("Save"):
        idx = df[df["erpJobOperationRunId"] == run_id].index[0]
        df.at[idx, "erpJobOperationRunId"] = erp_id
        df.at[idx, "operator"] = operator
        df.at[idx, "startAt"] = pd.to_datetime(start_at)
        df.at[idx, "endAt"] = pd.to_datetime(end_at)
        # Replot the graph
        st.plotly_chart(px.timeline(df, x_start="startAt", x_end="endAt", y="erpJobOperationRunId", color='color', title="Gantt Chart with Overlapping Operator Runs"), use_container_width=True)

# Check if any runs overlap
overlaps = False
for i in range(len(df)):
    for j in range(len(df)):
        if i != j and df.iloc[i]['startAt'] < df.iloc[j]['endAt'] and df.iloc[i]['endAt'] > df.iloc[j]['startAt']:
            overlaps = True
            break

# If no overlaps, enable Send Data button
if not overlaps:
    if st.button("Send Data"):
        # Convert modified data to JSON and send as POST request
        json_data = df.to_json()
        response = requests.post("YOUR_API_ENDPOINT_HERE", json=json_data)
        st.write("Data sent successfully!")
