from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import csv

"""
# Valor Caronas

"""
df_parameters = pd.read_csv('parameters.csv')

with st.expander("Parâmetros Utilizados"):
    pedro_ride1 = st.number_input("Valor da Carona Pedro = ", value = df_parameters['pedroRide1'][0])
    pedro_ride2 = st.number_input("Valor da Carona Pedro Rota 2 = ", value = df_parameters['pedroRide2'][0])
    carlos_ride = st.number_input("Valor da Carona Carlos = ", value = df_parameters['carlosRide'][0])

    if st.button('Atualizar Parâmetros'):
        df['pedroRide1'] = df['pedroRide1'].replace([0], pedro_ride1)
        df['pedroRide2'] = df['pedroRide2'].replace([0], pedro_ride2)
        df['carlosRide'] = df['carlosRide'].replace([0], carlos_ride)

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


if st.button('SALVAR E ATUALIZAR'):

    for i in range(7):
        pricesToPayCarlos[i] = ridesCarlos[i] * carlos_ride
        df['priceToPayCarlos'][i] = pricesToPayCarlos[i]
        df['ridesCarlos'][i] = carlos_rides_count[i]
        pricesToPayPedro[i] = ridesPedro[i] * pedro_ride1
        df['priceToPayPedro'][i] = pricesToPayPedro[i]
        df['ridesPedro'][i] = pedro_rides_count[i]

    #Gabriel
    # pricesToPayCarlos[0] = ridesCarlos[0] * carlos_ride
    # df['priceToPayCarlos'][0] = pricesToPayCarlos[0]
    # df['ridesCarlos'][0] = carlos_rides_count[0]


    # pricesToPayPedro[0] = ridesPedro[0] * pedro_ride1
    # df['priceToPayPedro'][0] = pricesToPayPedro[0]
    # df['ridesPedro'][0] = pedro_rides_count[0]

    # #Lucas
    # pricesToPayCarlos[1] = ridesCarlos[1] * carlos_ride
    # df['priceToPayCarlos'][1] = pricesToPayCarlos[1]
    # df['ridesCarlos'][1] = carlos_rides_count[1]

    # pricesToPayPedro[1] = ridesPedro[1] * pedro_ride1
    # df['priceToPayPedro'][1] = pricesToPayPedro[1]
    # df['ridesPedro'][1] = pedro_rides_count[1]

    # #Leo
    # pricesToPayCarlos[2] = ridesCarlos[2] * carlos_ride
    # df['priceToPayCarlos'][2] = pricesToPayCarlos[2]
    # df['ridesCarlos'][2] = carlos_rides_count[2]


    # pricesToPayPedro[2] = ridesPedro[2] * pedro_ride1
    # df['priceToPayPedro'][2] = pricesToPayPedro[2]
    # df['ridesPedro'][2] = pedro_rides_count[2]

    # #Pedro
    # pricesToPayCarlos[3] = ridesCarlos[3] * carlos_ride
    # df['priceToPayCarlos'] = df['priceToPayCarlos'].replace([3],pricesToPayCarlos[3])
    # df['ridesCarlos'] = df['ridesCarlos'].replace([3],carlos_rides_count[3])

    # #Carlos
    # pricesToPayPedro[4] = ridesPedro[4] * pedro_ride1
    # df['priceToPayPedro'] = df['priceToPayPedro'].replace([4],pricesToPayPedro[4])
    # df['ridesPedro'] = df['ridesPedro'].replace([4],pedro_rides_count[4])

    # #Giovanna
    # pricesToPayPedro[5] = ridesPedro[5] * pedro_ride2
    # df['priceToPayPedro'] = df['priceToPayPedro'].replace([5],pricesToPayPedro[5])
    # df['ridesPedro'] = df['ridesPedro'].replace([5],pedro_rides_count[5])

    # #Giovana
    # pricesToPayPedro[6] = ridesPedro[6] * pedro_ride2
    # df['priceToPayPedro'] = df['priceToPayPedro'].replace([6],pricesToPayPedro[6])
    # df['ridesPedro'] = df['ridesPedro'].replace([6],pedro_rides_count[6])

    df.to_csv("rides.csv", index=False)
    st.write('Atualize a página')
