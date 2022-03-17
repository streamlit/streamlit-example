from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import csv
from datetime import date

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
        df['pedroRide4'][0] = pedro_ride4
        df['pedroRide5'][0] = pedro_ride5
        df['carlosRide3'][0] = carlos_ride3
        df['carlosRide5'][0] = carlos_ride5

text_contents = '' 
with st.expander("Fechar o mês"):
    text_contents += '---GABRIEL---\n'
    text_contents += '\nCaronas com Pedro = ' + str(df['ridesPedro'][0])
    text_contents += '\nPreço para pagar ao Pedro = ' + str(df['priceToPayPedro'][0])
    text_contents += '\nCaronas com Carlos = ' + str(df['ridesCarlos'][0])
    text_contents += '\nPreço para pagar ao Carlos = ' + str(df['priceToPayCarlos'][0])
    text_contents += '\n\n' 
    text_contents += '---LUCAS---\n'
    text_contents += '\nCaronas com Pedro = ' + str(df['ridesPedro'][1])
    text_contents += '\nPreço para pagar ao Pedro = ' + str(df['priceToPayPedro'][1])
    text_contents += '\nCaronas com Carlos = ' + str(df['ridesCarlos'][1])
    text_contents += '\nPreço para pagar ao Carlos = ' + str(df['priceToPayCarlos'][1])
    text_contents += '\n\n'    
    text_contents += '---LEO---\n'
    text_contents += '\nCaronas com Pedro = ' + str(df['ridesPedro'][2])
    text_contents += '\nPreço para pagar ao Pedro = ' + str(df['priceToPayPedro'][2])
    text_contents += '\nCaronas com Carlos = ' + str(df['ridesCarlos'][2])
    text_contents += '\nPreço para pagar ao Carlos = ' + str(df['priceToPayCarlos'][2])
    text_contents += '\n\n'  
    text_contents += '---PEDRO---\n'
    text_contents += '\nCaronas com Carlos = ' + str(df['ridesCarlos'][3])
    text_contents += '\nPreço para pagar ao Carlos = ' + str(df['priceToPayCarlos'][3])
    text_contents += '\n\n'  
    text_contents += '---CARLOS---\n'
    text_contents += '\nCaronas com Pedro = ' + str(df['ridesPedro'][4])
    text_contents += '\nPreço para pagar ao Pedro = ' + str(df['priceToPayPedro'][4])
    text_contents += '\n\n' 
    text_contents += '---GIOVANNA---\n'
    text_contents += '\nCaronas com Pedro = ' + str(df['ridesPedro'][5])
    text_contents += '\nPreço para pagar ao Pedro = ' + str(df['priceToPayPedro'][5])
    text_contents += '\n\n'  
    text_contents += '---GIOVANA---\n'
    text_contents += '\nCaronas com Pedro = ' + str(df['ridesPedro'][6])
    text_contents += '\nPreço para pagar ao Pedro = ' + str(df['priceToPayPedro'][6])
    text_contents += '\n\n'   
    dataExtrato = "extrato-" + str(date.today()) + ".txt"
    
    if st.download_button('Zerar Caronas e Gerar Extrato', text_contents, file_name=dataExtrato):
        for i in range(7):
            df['ridesPedro'][i] = 0
            df['ridesCarlos'][i] = 0
            df['priceToPayPedro'][i] = 0
            df['priceToPayCarlos'][i] = 0 
        df.to_csv("rides.csv", index=False)
        

pedro_rides_count = [None] * 7
carlos_rides_count = [None] * 6


st.header("Gabriel")
with st.expander("Carona com Pedro"):
    st.write("Total de caronas com Pedro = ", df['ridesPedro'][0])

    pedro_rides_count[0] = st.number_input('Adicionar carona:',min_value=0, step=1, key="gabrielToPedro", value = 0)

    four= st.checkbox('4 pessoas', key="check4GabrielToPedro")
    five = st.checkbox('5 pessoas', key="check5GabrielToPedro")

    if st.button('ADICIONAR CARONA', key="addGabrielPedro"):
        df['ridesPedro'][0] += pedro_rides_count[0]
        if four:
            df['priceToPayPedro'][0] += pedro_ride4 * pedro_rides_count[0]
        if five:
            df['priceToPayPedro'][0] += pedro_ride5 * pedro_rides_count[0]
        st.write("ATUALIZE A PÁGINA")

with st.expander("Carona com Carlos"):

    st.write("Total de caronas com Carlos = ", df['ridesCarlos'][0])

    carlos_rides_count[0] = st.number_input('Adicionar carona:', min_value=0, step=1, key="gabrielToCarlos", value = 0)

    three = st.checkbox('3 pessoas',key="check3GabrielToCarlos")
    five = st.checkbox('5 pessoas',key="check5GabrielToCarlos")

    if st.button('ADICIONAR CARONA', key="addGabrielCarlos"):
        df['ridesCarlos'][0] += carlos_rides_count[0]
        if three:
            df['priceToPayCarlos'][0] += carlos_ride3 * carlos_rides_count[0]
        if five:
            pdf['priceToPayCarlos'][0] += carlos_ride5 * carlos_rides_count[0]
        st.write("ATUALIZE A PÁGINA")

st.write("Valor a pagar ao Pedro = R$ ", df['priceToPayPedro'][0])
st.write("Valor a pagar ao Carlos = R$ ", df['priceToPayCarlos'][0])


st.header("Lucas")
with st.expander("Carona com Pedro"):
    st.write("Total de caronas com Pedro = ", df['ridesPedro'][1])

    pedro_rides_count[1] = st.number_input('Adicionar carona:',min_value=0, step=1, key="lucasToPedro", value = 0)

    four= st.checkbox('4 pessoas', key="check4LucasToPedro")
    five = st.checkbox('5 pessoas', key="check5LucasToPedro")

    if st.button('ADICIONAR CARONA', key="addLucasPedro"):
        df['ridesPedro'][1] += pedro_rides_count[1]
        if four:
            df['priceToPayPedro'][1] += pedro_ride4 * pedro_rides_count[1]
        if five:
            df['priceToPayPedro'][1] += pedro_ride5 * pedro_rides_count[1]
        st.write("ATUALIZE A PÁGINA")

with st.expander("Carona com Carlos"):

    st.write("Total de caronas com Carlos = ", df['ridesCarlos'][1])

    carlos_rides_count[1] = st.number_input('Adicionar carona:', min_value=0, step=1, key="lucasToCarlos", value = 0)

    three = st.checkbox('3 pessoas',key="check3LucasToCarlos")
    five = st.checkbox('5 pessoas',key="check5LucasToCarlos")

    if st.button('ADICIONAR CARONA', key="addLucasCarlos"):
        df['ridesCarlos'][1] += carlos_rides_count[1]
        if three:
            df['priceToPayCarlos'][1] += carlos_ride3 * carlos_rides_count[1]
        if five:
            pdf['priceToPayCarlos'][1] += carlos_ride5 * carlos_rides_count[1]
        st.write("ATUALIZE A PÁGINA")

st.write("Valor a pagar ao Pedro = R$ ", df['priceToPayPedro'][1])
st.write("Valor a pagar ao Carlos = R$ ", df['priceToPayCarlos'][1])


st.header("Leo")
with st.expander("Carona com Pedro"):
    st.write("Total de caronas com Pedro = ", df['ridesPedro'][2])

    pedro_rides_count[2] = st.number_input('Adicionar carona:',min_value=0, step=1, key="leoToPedro", value = 0)

    four= st.checkbox('4 pessoas', key="check4LeoToPedro")
    five = st.checkbox('5 pessoas', key="check5LeoToPedro")

    if st.button('ADICIONAR CARONA', key="addLeoPedro"):
        df['ridesPedro'][2] += pedro_rides_count[2]
        if four:
            df['priceToPayPedro'][2] += pedro_ride4 * pedro_rides_count[2]
        if five:
            df['priceToPayPedro'][2] += pedro_ride5 * pedro_rides_count[2]
        st.write("ATUALIZE A PÁGINA")

with st.expander("Carona com Carlos"):

    st.write("Total de caronas com Carlos = ", df['ridesCarlos'][2])

    carlos_rides_count[2] = st.number_input('Adicionar carona:', min_value=0, step=1, key="leoToCarlos", value = 0)

    three = st.checkbox('3 pessoas',key="check3LeoToCarlos")
    five = st.checkbox('5 pessoas',key="check5LeoToCarlos")

    if st.button('ADICIONAR CARONA', key="addLeoCarlos"):
        df['ridesCarlos'][2] += carlos_rides_count[2]
        if three:
            df['priceToPayCarlos'][2] += carlos_ride3 * carlos_rides_count[2] 
        if five:
            pdf['priceToPayCarlos'][2] += carlos_ride5 * carlos_rides_count[2] 
        st.write("ATUALIZE A PÁGINA")

st.write("Valor a pagar ao Pedro = R$ ", df['priceToPayPedro'][2])
st.write("Valor a pagar ao Carlos = R$ ", df['priceToPayCarlos'][2])


st.header("Pedro")
with st.expander("Carona com Carlos"):

    st.write("Total de caronas com Carlos = ", df['ridesCarlos'][3])

    carlos_rides_count[3] = st.number_input('Adicionar carona:', min_value=0, step=1, key="pedroToCarlos", value = 0)

    three = st.checkbox('3 pessoas',key="check3PedroToCarlos")
    five = st.checkbox('5 pessoas',key="check5PedroToCarlos")

    if st.button('ADICIONAR CARONA', key="addPedro"):
        df['ridesCarlos'][3] += carlos_rides_count[3]
        if three:
            df['priceToPayCarlos'][3] += carlos_ride3 * carlos_rides_count[3]
        if five:
            pdf['priceToPayCarlos'][3] += carlos_ride5 * carlos_rides_count[3]
        st.write("ATUALIZE A PÁGINA")

st.write("Valor a pagar ao Pedro = R$ ", df['priceToPayPedro'][3])
st.write("Valor a pagar ao Carlos = R$ ", df['priceToPayCarlos'][3])

st.header("Carlos")
with st.expander("Carona com Pedro"):
    st.write("Total de caronas com Pedro = ", df['ridesPedro'][4])

    pedro_rides_count[4] = st.number_input('Adicionar carona:',min_value=0, step=1, key="carlosToPedro", value = 0)

    four= st.checkbox('4 pessoas', key="check4CarlosToPedro")
    five = st.checkbox('5 pessoas', key="check5CarlosToPedro")

    if st.button('ADICIONAR CARONA', key="addCarlos"):
        df['ridesPedro'][4] += pedro_rides_count[4]
        if four:
            df['priceToPayPedro'][4] += pedro_ride4 * pedro_rides_count[4]
        if five:
            df['priceToPayPedro'][4] += pedro_ride5 * pedro_rides_count[4]
        st.write("ATUALIZE A PÁGINA")

st.write("Valor a pagar ao Pedro = R$ ", df['priceToPayPedro'][4])


st.header("Giovanna")
with st.expander("Carona com Pedro"):
    st.write("Total de caronas com Pedro = ", df['ridesPedro'][5])

    pedro_rides_count[5] = st.number_input('Adicionar carona:',min_value=0, step=1, key="giovannaToPedro", value = 0)

    four= st.checkbox('4 pessoas', key="giovanna4GiovannaToPedro") 
    five = st.checkbox('5 pessoas', key="giovanna5GiovannaToPedro") 

    if st.button('ADICIONAR CARONA', key="addGiovanna"):
        df['ridesPedro'][5] += pedro_rides_count[5]
        if four:
            df['priceToPayPedro'][5] += pedro_ride4 * pedro_rides_count[5]
        if five:
            df['priceToPayPedro'][5] += pedro_ride5 * pedro_rides_count[5]
        st.write("ATUALIZE A PÁGINA")

st.write("Valor a pagar ao Pedro = R$ ", df['priceToPayPedro'][5])

st.header("Giovana")
with st.expander("Carona com Pedro"):
    st.write("Total de caronas com Pedro = ", df['ridesPedro'][6])

    pedro_rides_count[6] = st.number_input('Adicionar carona:',min_value=0, step=1, key="giovanaToPedro", value = 0)

    four= st.checkbox('4 pessoas', key="giovanna4GiovanaToPedro")
    five = st.checkbox('5 pessoas', key="giovanna5GiovanaToPedro")

    if st.button('ADICIONAR CARONA', key="addGiovana"):
        df['ridesPedro'][6] += pedro_rides_count[6]
        if four:
            df['priceToPayPedro'][6] += pedro_ride4 * pedro_rides_count[6]
        if five:
            df['priceToPayPedro'][6] += pedro_ride5 * pedro_rides_count[6]
        st.write("ATUALIZE A PÁGINA")

st.write("Valor a pagar ao Pedro = R$ ", df['priceToPayPedro'][6])

df.to_csv("rides.csv", index=False)

