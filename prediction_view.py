import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def run():
    # boton en el centro para crear una nueva incidencia que abra un formulario con campos basicos
    if st.button('Crear una nueva incidencia'):
        with st.form(key='my_form'):
            st.write('Cree una nueva incidencia:')

            # Aquí puedes agregar los campos que necesites para tu formulario
            campo1 = st.text_input(label='Campo 1')
            campo2 = st.text_input(label='Campo 2')
            campo3 = st.text_input(label='Campo 3')

            # Botón de envío del formulario
            submit_button = st.form_submit_button(label='Enviar')

            # botón para cancelr el formulario
            cancel_button = st.form_submit_button(label='Cancelar')
