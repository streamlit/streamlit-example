import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import eda_view as view1
import prediction_view as view2
import streamlit_option_menu
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide",
                   initial_sidebar_state="expanded")
alt.themes.enable("dark")

with st.sidebar:
    st.title("Gestión de incidencias")
    selected = option_menu(
    menu_title = "Menu",
    options = ['Overview', 'Nueva incidencia'],
    icons = ["house","gear"],
    menu_icon = "cast",
    default_index = 0,
)
    
#df = pd.read_excel('/Users/carlotapersonal/Library/CloudStorage/OneDrive-UFV/CURSO_5/PFG/Code/proyecto-fin-de-grado-2024-2-carlotagomezr/data-analysis/eda/dataset_post_EDA.xlsx')
df = pd.read_excel('/Users/carlotro/Desktop/Escritorio/Personal-Carlota/UFV/PFG/APP-REPO/dataset_post_EDA.xlsx')
df['reassingment_count_bool'] = df['reassignment_count'].apply(lambda x: 1 if x > 0 else 0) # indicar si ha habido reasignacion o no
 

if selected == 'Overview':
    view1.run(df)
elif selected == 'Nueva incidencia':
    view2.run(df) 