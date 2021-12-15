# Import libraries to read in a file line-by-line (txt file)
import io
import os
import sys
import time
import datetime
import re


timelineData = {}
datadir = os.getcwd() + '/Arkouda-Benchmark-Data'

# Iterate over all files in the current directory
for filename in os.listdir(datadir):
    if not filename.endswith('32.out') or (filename.find('IO') == -1 and filename.find('lanl') == -1):
        continue
    # print(f"==========================={filename}================================")
    timelineData[filename] = {}
    # Read line-by-line and grab timestamp at beginnning of line...
    with io.open(f'{datadir}/{filename}', 'r', encoding='utf-8') as f:
        t = 0
        lastKey = None
        for line in f:
            if line.startswith("2021"):
                # Extract timestamp from example: "2021-12-09:11:30:59"
                timestamp = ':'.join(line.split(':')[:2] + [line.split(':')[2][:2]]) + '.' + line.split(".")[1][:6]
                # Convert timestamp to datetime object
                dt = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
                # Convert datetime object to UNIX timestamp
                unix_timestamp = time.mktime(dt.timetuple())
                # Extract for example: ">>> getconfig took 0.00025399999999997647 sec"
                # and obtain both the name (i.e. getconfig) and the time (i.e. 0.00025399999999997647)
                # from "2021-12-09:11:31:23 [arkouda_server] main Line 410 INFO [Chapel] <<< getconfig took 0.00025399999999997647 sec"
                ret = re.match("(.*) <<< (.*) took (.*) sec", line)
                if ret is not None:
                    ret = ret.groups()
                    key = ret[1]
                    if ret[1].startswith('shutdown'):
                        key = 'shutdown'


                    if key not in  timelineData[filename]:
                        timelineData[filename][key] = []
                    timelineData[filename][key].append((t, t+int(ret[2])))

                    # Print the name and the time
                    # timeTakenStr = str(int(ret[2]) / 1000000) + "s" if int(ret[2]) >= 1000000 else str(int(ret[2])/1000) + "ms" if int(ret[2]) >= 1000 else ret[2] + "μs"
                    # currentStartTimeStr = str(t / 1000000) + "s" if t >= 1000000 else str(t/1000) + "ms" if t >= 1000 else str(t) + "μs"
                    # endStartTimeStr = str((t+int(ret[2])) / 1000000) + "s" if (t+int(ret[2])) >= 1000000 else str((t+int(ret[2]))/1000) + "ms" if (t+int(ret[2])) >= 1000 else str(t+int(ret[2])) + "μs"
                    # print(f'{ret[1]} took {timeTakenStr} @ ({currentStartTimeStr},{endStartTimeStr})')
                    t += int(ret[2])
                    lastKey = key
                else:
                    ret = re.match(".* bytes of memory used after command (.*)", line)
                    if ret is not None:
                        memory = int(ret[1])
                        lastTuple = timelineData[filename][lastKey][-1]
                        timelineData[filename][lastKey][-1] = (lastTuple[0], lastTuple[1], memory)
                    if lastKey == 'shutdown':
                        lastTuple = timelineData[filename][lastKey][-1]
                        timelineData[filename][lastKey][-1] = (lastTuple[0], lastTuple[1], 0)

# print(timelineData)

import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Gather all names from timelineData
names = []
for filename in timelineData:
    for key in timelineData[filename]:
        if key not in names:
            names.append(key)
cmap = plt.get_cmap('tab20c')
colors = cmap(np.linspace(0, 1, len(names)))
colorMap = {k:str(px.colors.label_rgb(tuple(v)[0:3])) for k,v in zip(names, colors)}
for plotName in timelineData.keys():
    today = dt.datetime.now()
    df = pd.DataFrame(
        [dict(Task='Workload', Start=str(today + timedelta(microseconds=s)), Finish=str(today + timedelta(microseconds=f)), Memory=m, Color=t) for t, xs in timelineData[plotName].items() for (s,f,m) in xs]
    )
    df.sort_values(by=['Start'], inplace=True)
    df['Index'] = range(1, len(df) + 1)
    fig = px.timeline(df, x_start='Start', x_end='Finish', y='Task', color='Color')
    fig.update_yaxes(autorange="reversed")
    f = fig.full_figure_for_development(warn=False)
    st.header(plotName)
    st.subheader("Timeline")
    st.write(fig)
    st.subheader("Memory Usage")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df['Finish'], y=df['Memory'], mode='lines+markers', name='Memory'))
    st.write(fig)
    st.subheader("Data")
    # Set name of plot to `plotName` as subheading
    st.write(df)
    