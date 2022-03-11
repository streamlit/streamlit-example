from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Valor Caronas

"""

gas_price = st.number_input('Valor Combustível')

pedro_rides_count = []
carlos_rides_count = []

"""
### Caronas Pedro

"""
pedro_rides_count[0] = st.number_input('GABRIEL',  step=int)
pedro_rides_count[1] = st.number_input('GIOVANNA', step=int)
pedro_rides_count[2] = st.number_input('GIOVANA', step=int)
pedro_rides_count[3] = st.number_input('LUCAS',  step=int)
pedro_rides_count[4] = st.number_input('LEO', step=int)
pedro_rides_count[5] = st.number_input('CARLOS', step=int)


"""
### Caronas Carlos

"""

carlos_rides_count[0] = st.number_input('GABRIEL', step=int)
carlos_rides_count[1] = st.number_input('PEDRO',  step=int)
carlos_rides_count[3] = st.number_input('LUCAS', step=int)
carlos_rides_count[4] = st.number_input('LEO',  step=int)
carlos_rides_count[5] = st.number_input('CARLOS', step=int)