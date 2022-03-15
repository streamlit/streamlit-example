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
df = pd.read_csv('rides.csv')

with st.expander("Parâmetros Utilizados"):
    pedro_ride4 = st.number_input("Valor da Carona Pedro (4 pessoas)= ", value = df_parameters['pedroRide4'][0]) #rota casa da gi
    pedro_ride5 = st.number_input("Valor da Carona Pedro (5 pessoas) = ", value = df_parameters['pedroRide5'][0])
    carlos_ride3 = st.number_input("Valor da Carona Carlos (3 pessoas)= ", value = df_parameters['carlosRide3'][0])
    carlos_ride5 = st.number_input("Valor da Carona Carlos (5 pessoas)= ", value = df_parameters['carlosRide5'][0])

    if st.button('Atualizar Parâmetros'):
        df['pedroRide1'][0] = pedro_ride4
        df['pedroRide2'][0] = pedro_ride5
        df['carlosRide'][0] = carlos_ride3
        df['carlosRide'][0] = carlos_ride5

text_contents = '' 
with st.expander("Fechar o mês"):
    text_contents += '---GABRIEL---\n'
    text_contents += '\nCaronas com Pedro = \n' + str(df['ridesPedro'][0])
    text_contents += '\nPreço para pagar ao Pedro = \n' + str(df['priceToPayPedro'][0])
    text_contents += '\nCaronas com Carlos = \n' + str(df['ridesPedro'][0])
    text_contents += '\nPreço para pagar ao Carlos = \n' + str(df['priceToPayCarlos'][0])
    text_contents += '\n\n' 
        
    st.download_button('Zerar Caronas e Gerar Extrato', text_contents)
        

                # f.write('---LUCAS---\n')
                # f.write('Caronas com Pedro = \n' + df['ridesPedro'][1])
                # f.write('Preço para pagar ao Pedro = \n' + df['priceToPayPedro'][1])
                # f.write('Caronas com Carlos = \n' + df['ridesPedro'][1])
                # f.write('Preço para pagar ao Carlos = \n' + df['priceToPayCarlos'][1])
                # f.write('\n\n')
                # f.write('---LEO---\n')
                # f.write('Caronas com Pedro = \n' + df['ridesPedro'][2])
                # f.write('Preço para pagar ao Pedro = \n' + df['priceToPayPedro'][2])
                # f.write('Caronas com Carlos = \n' + df['ridesPedro'][2])
                # f.write('Preço para pagar ao Carlos = \n' + df['priceToPayCarlos'][2])
                # f.write('\n\n')
                # f.write('---PEDRO---\n')
                # f.write('Caronas com Carlos = \n' + df['ridesPedro'][3])
                # f.write('Preço para pagar ao Carlos = \n' + df['priceToPayCarlos'][3])
                # f.write('\n\n')
                # f.write('---CARLOS---\n')
                # f.write('Caronas com Pedro = \n' + df['ridesPedro'][4])
                # f.write('Preço para pagar ao Pedro = \n' + df['priceToPayPedro'][4])
                # f.write('\n\n')
                # f.write('---GIOVANNA---\n')
                # f.write('Caronas com Pedro = \n' + df['ridesPedro'][5])
                # f.write('Preço para pagar ao Pedro = \n' + df['priceToPayPedro'][5])
                # f.write('\n\n')
                # f.write('---GIOVANA---\n')
                # f.write('Caronas com Pedro = \n' + df['ridesPedro'][6])
                # f.write('Preço para pagar ao Pedro = \n' + df['priceToPayPedro'][6])
    for i in range(6):
        df['ridesPedro'][i] = 0
        df['ridesCarlos'][i] = 0
        df['priceToPayPedro'][i] = 0
        df['priceToPayCarlos'][i] = 0 
        


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
with st.expander("Carona com Pedro"):
    pedro_rides_count[0] = st.number_input('',min_value=0, step=1, key="gabrielToPedro", value = ridesPedro[0])

    four= st.checkbox('4 pessoas', key="check4GabrielToPedro")
    five = st.checkbox('5 pessoas', key="check5GabrielToPedro")
    if four:
        pricesToPayPedro[0] += pedro_ride4
    if five:
        pricesToPayPedro[0] += pedro_ride5

with st.expander("Carona com Carlos"):
    carlos_rides_count[0] = st.number_input('', min_value=0, step=1, key="gabrielToCarlos", value = ridesCarlos[0])
    three = st.checkbox('3 pessoas',key="check3GabrielToCarlos")
    five = st.checkbox('5 pessoas',key="check5GabrielToCarlos")
    if three:
        pricesToPayCarlos[0] += carlos_ride3
    if five:
        pricesToPayCarlos[0] += carlos_ride5

st.write("Valor a pagar ao Pedro = R$ ",pricesToPayPedro[0])
st.write("Valor a pagar ao Carlos = R$ ",pricesToPayCarlos[0])


st.header("Lucas")
with st.expander("Carona com Pedro"):
    pedro_rides_count[1] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="lucasToPedro", value = ridesPedro[1])
    four= st.checkbox('4 pessoas', key="check4LucasToPedro")
    five = st.checkbox('5 pessoas', key="check5LucasToPedro")
    if four:
        pricesToPayPedro[1] += pedro_ride4
    if five:
        pricesToPayPedro[1] += pedro_ride5

with st.expander("Carona com Carlos"):
    carlos_rides_count[1] = st.number_input('Caronas com Carlos', min_value=0, step=1, key="lucasToCarlos", value = ridesCarlos[1])
    three = st.checkbox('3 pessoas',key="check3LucasToCarlos")
    five = st.checkbox('5 pessoas',key="check5LucasToCarlos")
    if three:
        pricesToPayCarlos[1] += carlos_ride3
    if five:
        pricesToPayCarlos[1] += carlos_ride5

st.write("Valor a pagar ao Pedro = R$ ",pricesToPayPedro[1])
st.write("Valor a pagar ao Carlos = R$ ",pricesToPayCarlos[1])



st.header("Leo")
with st.expander("Carona com Pedro"):
    pedro_rides_count[2] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="leoToPedro", value = ridesPedro[2])
    four= st.checkbox('4 pessoas', key="check4LeoToPedro")
    five = st.checkbox('5 pessoas', key="check5LeoToPedro")
    if four:
        pricesToPayPedro[2] += pedro_ride4
    if five:
        pricesToPayPedro[2] += pedro_ride5

with st.expander("Carona com Carlos"):       
    carlos_rides_count[2] = st.number_input('Caronas com Carlos', min_value=0, step=1, key="leoToCarlos", value = ridesCarlos[2])
    three = st.checkbox('3 pessoas',key="check3LeoToCarlos")
    five = st.checkbox('5 pessoas',key="check5LeoToCarlos")
    if three:
        pricesToPayCarlos[2] += carlos_ride3
    if five:
        pricesToPayCarlos[2] += carlos_ride5

st.write("Valor a pagar ao Pedro = R$ ",pricesToPayPedro[2])
st.write("Valor a pagar ao Carlos = R$ ",pricesToPayCarlos[2])

st.header("Pedro")
with st.expander("Carona com Carlos"):
    carlos_rides_count[3] = st.number_input('Caronas com Carlos', min_value=0, step=1, key="pedroToCarlos", value = ridesCarlos[3])

st.write("Valor a pagar ao Carlos = R$ ",pricesToPayCarlos[3])

st.header("Carlos")
with st.expander("Carona com Pedro"):
    pedro_rides_count[4] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="carlosToPedro", value = ridesPedro[4])
   
st.write("Valor a pagar ao Pedro = R$ ",pricesToPayPedro[4])

st.header("Giovanna")
with st.expander("Carona com Pedro"):
   
    pedro_rides_count[5] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="giovannaToPedro", value = ridesPedro[5])

    

st.write("Valor a pagar ao Pedro = R$ ",pricesToPayPedro[5])

st.header("Giovana")
with st.expander("Carona com Pedro"):
    pedro_rides_count[6] = st.number_input('Caronas com Pedro', min_value=0, step=1, key="giovanaToPedro", value = ridesPedro[6])



st.write("Valor a pagar ao Pedro = R$ ",pricesToPayPedro[6])


if st.button('SALVAR E ATUALIZAR'):

    #Gabriel
    if pedro_rides_count[0] > df['ridesPedro'][0]:
        df['ridesPedro'][0] = pedro_rides_count[0]
        df['priceToPayPedro'][0] = pricesToPayPedro[0]

    if carlos_rides_count[0] > df['ridesCarlos'][0]:
        df['priceToPayCarlos'][0] = pricesToPayCarlos[0]
        df['ridesCarlos'][0] = carlos_rides_count[0]


    #Lucas
    if pedro_rides_count[1] > df['ridesPedro'][1]:
        df['ridesPedro'][1] = pedro_rides_count[1]
        df['priceToPayPedro'][1] = pricesToPayPedro[1]

    if carlos_rides_count[1] > df['ridesCarlos'][1]:
        df['priceToPayCarlos'][1] = pricesToPayCarlos[1]
        df['ridesCarlos'][1] = carlos_rides_count[1]

    #Leo
    if pedro_rides_count[2] > df['ridesPedro'][2]:
        df['ridesPedro'][2] = pedro_rides_count[2]
        df['priceToPayPedro'][2] = pricesToPayPedro[2]

    if carlos_rides_count[2] > df['ridesCarlos'][2]:
        df['priceToPayCarlos'][2] = pricesToPayCarlos[2]
        df['ridesCarlos'][2] = carlos_rides_count[2]

    #Pedro
    if carlos_rides_count[3] > df['ridesCarlos'][3]:
        df['ridesCarlos'][3] = carlos_rides_count[3]
        pricesToPayCarlos[3] += carlos_ride5
        df['priceToPayCarlos'][3] = pricesToPayCarlos[3]

    #Carlos
    if pedro_rides_count[4] > df['ridesPedro'][4]:
        df['ridesPedro'][4] = pedro_rides_count[4]
        pricesToPayPedro[4] += pedro_ride5
        df['priceToPayPedro'][4] = pricesToPayPedro[4]

    #Giovanna
    if pedro_rides_count[5] > df['ridesPedro'][5]:
        df['ridesPedro'][5] = pedro_rides_count[5]
        pricesToPayPedro[5] += pedro_ride4
        df['priceToPayPedro'][5] = pricesToPayPedro[5]
        

    #Giovana
    if pedro_rides_count[6] > df['ridesPedro'][6]:
        df['ridesPedro'][6] = pedro_rides_count[6]
        pricesToPayPedro[6] += pedro_ride4
        df['priceToPayPedro'][6] = pricesToPayPedro[6]

    df.to_csv("rides.csv", index=False)
    st.write('Atualize a página')
