import pandas as pd
import numpy as np
import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from time import sleep
from hugchat_api import HuggingChat
import os


ti=st.title("AI Utility Services 📇")
st.write('Developed By [Jordy](https://www.linkedin.com/in/manye-jordana-0315731b1)')
page=st.selectbox("What I offer",("Select","AI Powered AllTalK","AllSummary","AllVisuals"))