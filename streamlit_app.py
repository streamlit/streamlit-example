import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

#hola
titulos_pestanas = ['Página principal', 'Nacional', 'Internacional','Departamentos','Países','Sobre nosotras']
pestaña1, pestaña2, pestaña3, pestaña4, pestaña5, pestaña6 = st.tabs(titulos_pestanas)

with pestaña1:
    st.title('Análisis de Población identificada con DNI de mayor de edad por condición de donante de órganos')
    st.write("Texto sobre donación de órganos")
    st.write("")
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.button("Nacional", type="secondary")
            chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
            st.bar_chart(chart_data)
        with right_column:
            st.button("Internacional", type="secondary") 
            chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
            st.bar_chart(chart_data)
            st.caption('Los datos de este gráfico no están actualizados a la fecha actual.')

with pestaña2:
    st.title("Condición de donante de órganos a nivel nacional")
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.button("2022", type="secondary")
            chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
            st.bar_chart(chart_data)
        with right_column:
            st.button("2023", type="secondary")
            chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
            st.bar_chart(chart_data)
            st.caption("Los datos de este gráfico no están actualizados a la fecha actual.")

with pestaña3:
    st.title ("Condición de donante de órganos a nivel internacional")
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.button(" 2022", type="secondary")
            chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
            st.bar_chart(chart_data)
        with right_column:
            st.button(" 2023", type="secondary")
            chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
            st.bar_chart(chart_data)
            st.caption("Los datos de este gráfico no están actualizados a la fecha actual.")

with pestaña4:
    st.title("Condición de donante de órganos por departamentos")
    option = st.selectbox(
        "Elije un departamento",
        ("Amazonas", "Áncash","Apurímac","Arequipa","Ayacucho","Cajamarca","Cusco","Huancavelica","Huánuco","Ica","Junín","La Libertad","Lambayeque","Lima","Loreto","Madre de Dios","Moquegua","Pasco","Piura","Puno","San Martín","Tacna","Tumbes","Callao","Ucayali"))
    option2 = st.selectbox(
        "Elige un año",
        ("2022","2023"))

with pestaña5:
    st.title("Condición de donante de órganos por países")
    option3 = st.selectbox(
        "Elige un continente",
        ("África","América","Asia","Europa","Oceanía"))
    if option3 == "África":
        option5 = st.selectbox(
                "Elige un país",
                ("Argelia","Costa de Marfil"))
    elif option3 == "América":
        option5 = st.selectbox(
            "Elige un país",
            ("Antillas Holandesas","Argentina"))
    elif option3 == "Asia":
        option5 = st.selectbox(
            "Elige un país",
            ("Catar","India"))
    elif option3 == "Europa":
        option5 = st.selectbox(
            "ELige un país",
            ("Alemania","Austria"))
    elif option3 == "Oceanía":
        option5 = st.selectbox(
            "Elige un país",
            ("Australia","Nueva Zelanda"))
    option4 = st.selectbox(
        "Elige un año",
        (" 2022","2023"))

st.link_button("Para más información de click aquí", "https://www.datosabiertos.gob.pe/dataset/reniec-poblaci%C3%B3n-identificada-con-dni-de-mayor-de-edad-por-condici%C3%B3n-de-donante-de-%C3%B3rganos")
