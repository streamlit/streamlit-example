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

with st.expander("Chaves Pix"):
    st.write("Pix Pedro: +5514998167179")
    st.write("Pix Carlos: 79105599-8e7c-47ec-9a0b-c192cced1791")

with st.expander("Fechar o mês"):
    st.write("Valores Zerados")


rides = [None] * 8

with st.expander("Preço das Caronas"):
    with st.container():
        st.header('Pedro')
        rides[0] = st.number_input('2 passageiros', key='ridepedro2')
        rides[1] = st.number_input('3 passageiros', key='ridepedro3')
        rides[2] = st.number_input('4 passageiros', key='ridepedro4')
        rides[3] = st.number_input('5 passageiros', key='ridepedro5')    
    with st.container():
        st.header('Carlos')
        rides[4] = st.number_input('2 passageiros', key='ridecarlos2')
        rides[5] = st.number_input('3 passageiros', key='ridecarlos3')
        rides[6] = st.number_input('4 passageiros', key='ridecarlos4')
        rides[7] = st.number_input('5 passageiros', key='ridecarlos5')  


pedro = [None] * 5
carlos = [None] * 5
lucas = [None] * 10
gabriel = [None] * 10
leo = [None] * 10
giovanna = [None] * 10
giovana = [None] * 10

with st.expander("Pedro"):
    with st.container():
        st.header("Caronas com Carlos")
        pedro[0] = st.number_input('2 passageiros')
        pedro[1] = st.number_input('3 passageiros')
        pedro[2] = st.number_input('4 passageiros')
        pedro[3] = st.number_input('5 passageiros')

with st.expander("Carlos"):
    with st.container():
        st.header("Caronas com Pedro")
        carlos[0] = st.number_input('2 passageiros', key='carlos2')
        carlos[1] = st.number_input('3 passageiros', key='carlos3')
        carlos[2] = st.number_input('4 passageiros', key='carlos4')
        carlos[3] = st.number_input('5 passageiros', key='carlos5')

with st.expander("Lucas"):
    with st.container():
        st.header("Caronas com Pedro")
        lucas[0] = st.number_input('2 passageiros', key='lucas2pedro')
        lucas[1] = st.number_input('3 passageiros', key='lucas3pedro')
        lucas[2] = st.number_input('4 passageiros', key='lucas4pedro')
        lucas[3] = st.number_input('5 passageiros', key='lucas5pedro')

    with st.container():
        st.header("Caronas com Carlos")
        lucas[4] = st.number_input('2 passageiros', key='lucas2carlos')
        lucas[5] = st.number_input('3 passageiros', key='lucas2carlos')
        lucas[6] = st.number_input('4 passageiros', key='lucas2carlos')
        lucas[7] = st.number_input('5 passageiros', key='lucas2carlos')


with st.expander("Gabriel"):
    with st.container():
        st.header("Caronas com Pedro")
        gabriel[0] = st.number_input('2 passageiros', key='gabriel2pedro')
        gabriel[1] = st.number_input('3 passageiros', key='gabriel3pedro')
        gabriel[2] = st.number_input('4 passageiros', key='gabriel4pedro')
        gabriel[3] = st.number_input('5 passageiros', key='gabriel5pedro')

    with st.container():
        st.header("Caronas com Carlos")  
        gabriel[4] = st.number_input('2 passageiros', key='gabriel2carlos')
        gabriel[5] = st.number_input('3 passageiros', key='gabriel2carlos')
        gabriel[6] = st.number_input('4 passageiros', key='gabriel2carlos')
        gabriel[7] = st.number_input('5 passageiros', key='gabriel2carlos')      

with st.expander("Leo"):
    with st.container():
        st.header("Caronas com Pedro")
        leo[0] = st.number_input('2 passageiros', key='leo2pedro')
        leo[1] = st.number_input('3 passageiros', key='leo3pedro')
        leo[2] = st.number_input('4 passageiros', key='leo4pedro')
        leo[3] = st.number_input('5 passageiros', key='leo5pedro')

    with st.container():
        st.header("Caronas com Carlos")    
        leo[4] = st.number_input('2 passageiros', key='leo2carlos')
        leo[5] = st.number_input('3 passageiros', key='leo2carlos')
        leo[6] = st.number_input('4 passageiros', key='leo2carlos')
        leo[7] = st.number_input('5 passageiros', key='leo2carlos')

with st.expander("Giovanna"):
    with st.container():
        st.header("Caronas com Pedro")
        giovanna[0] = st.number_input('2 passageiros', key='giovanna2pedro')
        giovanna[1] = st.number_input('3 passageiros', key='giovanna3pedro')
        giovanna[2] = st.number_input('4 passageiros', key='giovanna4pedro')
        giovanna[3] = st.number_input('5 passageiros', key='giovanna5pedro')

with st.expander("Giovana"):
    with st.container():
        st.header("Caronas com Pedro")
        giovana[0] = st.number_input('2 passageiros', key='giovana2pedro')
        giovana[1] = st.number_input('3 passageiros', key='giovana3pedro')
        giovana[2] = st.number_input('4 passageiros', key='giovana4pedro')
        giovana[3] = st.number_input('5 passageiros', key='giovana5pedro')


with st.expander("Total à pagar para o Pedro"):
        carlos[4] = (rides[0]*carlos[0])+(rides[1]*carlos[1])+(rides[2]*carlos[2])+(rides[3]*carlos[3])
        st.write('Carlos = ' + str(carlos[4]))

        lucas[8] = (rides[0]*lucas[0])+(rides[1]*lucas[1])+(rides[2]*lucas[2])+(rides[3]*lucas[3])
        st.write('Lucas = ' + str(lucas[8]))

        gabriel[8] = (rides[0]*gabriel[0])+(rides[1]*gabriel[1])+(rides[2]*gabriel[2])+(rides[3]*gabriel[3])
        st.write('Gabriel = ' + str(gabriel[8]))

        leo[8] = (rides[0]*leo[0])+(rides[1]*leo[1])+(rides[2]*leo[2])+(rides[3]*leo[3])
        st.write('Leo = ' + str(leo[8]))

        giovanna[8] = (rides[0]*giovanna[0])+(rides[1]*giovanna[1])+(rides[2]*giovanna[2])+(rides[3]*giovanna[3])
        st.write('Giovanna = ' + str(giovanna[8]))

        giovana[8] = (rides[0]*giovana[0])+(rides[1]*giovana[1])+(rides[2]*giovana[2])+(rides[3]*giovana[3])
        st.write('Giovana = ' +  str(giovana[8]))

with st.expander("Total à pagar para o Pedro"):
        pedro[4] = (rides[4]*pedros[0])+(rides[5]*pedro[1])+(rides[6]*pedro[2])+(rides[7]*pedro[3])
        st.write('Pedro = ' + str(pedro[4]))

        lucas[9] = (rides[4]*lucas[4])+(rides[5]*lucas[5])+(rides[6]*lucas[6])+(rides[7]*lucas[7])
        st.write('Lucas = ' + str(lucas[9]))

        gabriel[9] = (rides[4]*gabriel[4])+(rides[5]*gabriel[5])+(rides[6]*gabriel[6])+(rides[7]*gabriel[7])
        st.write('Gabriel = ' + str(gabriel[9]))

        leo[9] = (rides[4]*leo[4])+(rides[5]*leo[5])+(rides[6]*leo[6])+(rides[7]*leo[7])
        st.write('Leo = '+ str(leo[9]))
