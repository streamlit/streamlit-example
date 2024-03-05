import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import eda_view as view1
import prediction_view as view2

st.sidebar.title('Selecciona una vista')
options = ['Gestión de incidencias - Análisis exploratorio de datos', 'Nueva incidencia - predicciones y LLM']
menu = st.sidebar.selectbox('Select a view', options)

if menu == options[0]:
    view1.run()
elif menu == options[1]:
    view2.run()
