from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Valor Caronas

"""

with st.expander("Parâmetros Utilizados"):
    gas_price = st.number_input('Preço Combustível', value = 4.29)
    pedro_ride1 = st.number_input("Valor da Carona Pedro = ", value = 2)
    pedro_ride2 = st.number_input("Valor da Carona Pedro Rota 2 = ", value = 2)
    carlos_ride = st.number_input("Valor da Carona Carlos = ", value = 2)
    st.button('Atualizar Parâmetros')

pedro_rides_count = [None] * 6
carlos_rides_count = [None] * 6

st.header("Gabriel")
pedro_rides_count[0] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="gabrielToPedro")
carlos_rides_count[0] = st.number_input('Caronas com Carlos', min_value=0, step=1, key="gabrielToCarlos")
st.write("Valor a pagar ao Pedro = ")
st.write("Valor a pagar ao Carlos = ")

st.header("Lucas")
pedro_rides_count[1] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="lucasToPedro")
carlos_rides_count[1] = st.number_input('Caronas com Carlos', min_value=0, step=1, key="lucasToCarlos")
st.write("Valor a pagar ao Pedro = ")
st.write("Valor a pagar ao Carlos = ")

st.header("Leo")
pedro_rides_count[2] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="leoToPedro")
carlos_rides_count[2] = st.number_input('Caronas com Carlos', min_value=0, step=1, key="leoToCarlos")
st.write("Valor a pagar ao Pedro = ")
st.write("Valor a pagar ao Carlos = ")

st.header("Pedro")
carlos_rides_count[3] = st.number_input('Caronas com Carlos', min_value=0, step=1, key="pedroToCarlos")
st.write("Valor a pagar ao Carlos = ")

st.header("Carlos")
pedro_rides_count[3] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="carlosToPedro")
st.write("Valor a pagar ao Pedro = ")

st.header("Giovanna")
pedro_rides_count[4] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="giovannaToPedro")
st.write("Valor a pagar ao Pedro = ")

st.header("Giovana")
pedro_rides_count[5] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="giovanaToPedro")
st.write("Valor a pagar ao Pedro = ")


st.button('SALVAR E ATUALIZAR')