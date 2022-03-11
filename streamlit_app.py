from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import csv

"""
# Valor Caronas

"""

with st.expander("Parâmetros Utilizados"):
    gas_price = st.number_input('Preço Combustível', value = 4.29)
    pedro_ride1 = st.number_input("Valor da Carona Pedro = ", value = 2)
    pedro_ride2 = st.number_input("Valor da Carona Pedro Rota 2 = ", value = 2)
    carlos_ride = st.number_input("Valor da Carona Carlos = ", value = 2)
    st.button('Atualizar Parâmetros')

with st.expander("Fechar o mês"):
#     st.download_button(
#      label="Download extrato de caronas",
#      data=csv,
#      file_name='rides.csv',
#      mime='text/csv',
#  )
    st.button('Zerar Caronas')


df = pd.read_csv('rides.csv')

ridesPedro = []
ridesCarlos = []
pricesToPayPedro = []
pricesToPayCarlos = []

for i in range(7):
  ridesPedro.append(df['ridesPedro'][i])
  ridesCarlos.append(df['ridesCarlos'][i])
  pricesToPayPedro.append(df['priceToPayPedro'][i])
  pricesToPayCarlos.append(df['priceToPayCarlos'][i])


pedro_rides_count = [None] * 7
carlos_rides_count = [None] * 6

st.header("Gabriel")
pedro_rides_count[0] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="gabrielToPedro", value = ridesPedro[0])
carlos_rides_count[0] = st.number_input('Caronas com Carlos', min_value=0, step=1, key="gabrielToCarlos", value = ridesCarlos[0])
st.write("Valor a pagar ao Pedro = R$ ",pricesToPayPedro[0])
st.write("Valor a pagar ao Carlos = R$ ",pricesToPayCarlos[0])

st.header("Lucas")
pedro_rides_count[1] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="lucasToPedro", value = ridesPedro[1])
carlos_rides_count[1] = st.number_input('Caronas com Carlos', min_value=0, step=1, key="lucasToCarlos", value = ridesCarlos[1])
st.write("Valor a pagar ao Pedro = R$ ",pricesToPayPedro[1])
st.write("Valor a pagar ao Carlos = R$ ",pricesToPayCarlos[1])
st.header("Leo")
pedro_rides_count[2] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="leoToPedro", value = ridesPedro[2])
carlos_rides_count[2] = st.number_input('Caronas com Carlos', min_value=0, step=1, key="leoToCarlos", value = ridesCarlos[2])
st.write("Valor a pagar ao Pedro = R$ ",pricesToPayPedro[2])
st.write("Valor a pagar ao Carlos = R$ ",pricesToPayCarlos[2])

st.header("Pedro")
carlos_rides_count[3] = st.number_input('Caronas com Carlos', min_value=0, step=1, key="pedroToCarlos", value = ridesCarlos[3])
st.write("Valor a pagar ao Carlos = R$ ",pricesToPayCarlos[3])

st.header("Carlos")
pedro_rides_count[4] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="carlosToPedro", value = ridesPedro[4])
st.write("Valor a pagar ao Pedro = R$ ",pricesToPayPedro[4])

st.header("Giovanna")
pedro_rides_count[5] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="giovannaToPedro", value = ridesPedro[5])
st.write("Valor a pagar ao Pedro = R$ ",pricesToPayPedro[5])

st.header("Giovana")
pedro_rides_count[6] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="giovanaToPedro", value = ridesPedro[6])
st.write("Valor a pagar ao Pedro = R$ ",pricesToPayPedro[6])


st.button('SALVAR E ATUALIZAR')