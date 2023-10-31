from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
#from src.agstyler import PINLEFT, PRECISION_TWO, draw_grid

col1, col2 = st.columns(2)
col1.write("This is column 1")
col2.write("This is column 2")