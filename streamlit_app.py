import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import eda_view as view1
import prediction_view as view2
import streamlit_option_menu
from streamlit_option_menu import option_menu

# # st.sidebar.title('Selecciona una vista')
# options = ['Gestión de incidencias EDA', 'Nueva incidencia']
# menu = st.sidebar.selectbox('Selecciona una vista', options)

# if menu == options[0]:
#     view1.run()
# elif menu == options[1]:
#     view2.run()



with st.sidebar:
    selected = option_menu(
    menu_title = "Menu",
    options = ['Gestión de incidencias EDA', 'Nueva incidencia'],
    icons = ["house","gear"],
    menu_icon = "cast",
    default_index = 0,
    #orientation = "horizontal",
)
    

if selected == 'Gestión de incidencias EDA':
    view1.run()
elif selected == 'Nueva incidencia':
    view2.run() 