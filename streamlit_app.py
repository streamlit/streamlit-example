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
        rides[0] = st.number_input('2 passageiros')
        rides[1] = st.number_input('3 passageiros')
        rides[2] = st.number_input('4 passageiros')
        rides[3] = st.number_input('5 passageiros')    
    with st.container():
        st.header('Carlos')
        rides[4] = st.number_input('2 passageiros')
        rides[5] = st.number_input('3 passageiros')
        rides[6] = st.number_input('4 passageiros')
        rides[7] = st.number_input('5 passageiros')  


pedro = [None] * 5
carlos = [None] * 5
lucas = [None] * 10
gabriel = [None] * 10
leo = [None] * 10
giovanna = [None] * 10
giovana = [None] * 10

# with st.expander("Cadastrar Carona"):
#     with st.expander("Caronas com Pedro"):
#         with st.expander("Carlos"):
#             carlos[0] = st.number_input('2 passageiros')
#             carlos[1] = st.number_input('3 passageiros')
#             carlos[2] = st.number_input('4 passageiros')
#             carlos[3] = st.number_input('5 passageiros')
#         with st.expander("Lucas"):
#             lucas[0] = st.number_input('2 passageiros')
#             lucas[1] = st.number_input('3 passageiros')
#             lucas[2] = st.number_input('4 passageiros')
#             lucas[3] = st.number_input('5 passageiros')
#         with st.expander("Gabriel"):
#             gabriel[0] = st.number_input('2 passageiros')
#             gabriel[1] = st.number_input('3 passageiros')
#             gabriel[2] = st.number_input('4 passageiros')
#             gabriel[3] = st.number_input('5 passageiros')
#         with st.expander("Leo"):
#             leo[0] = st.number_input('2 passageiros')
#             leo[1] = st.number_input('3 passageiros')
#             leo[2] = st.number_input('4 passageiros')
#             leo[3] = st.number_input('5 passageiros')
#         with st.expander("Giovanna"):
#             giovanna[0] = st.number_input('2 passageiros')
#             giovanna[1] = st.number_input('3 passageiros')
#             giovanna[2] = st.number_input('4 passageiros')
#             giovanna[3] = st.number_input('5 passageiros')
#         with st.expander("Giovana"):
#             giovana[0] = st.number_input('2 passageiros')
#             giovana[1] = st.number_input('3 passageiros')
#             giovana[2] = st.number_input('4 passageiros')
#             giovana[3] = st.number_input('5 passageiros')


#     with st.expander("Caronas com Carlos"):
#         with st.expander("Pedro"):
#             pedro[0] = st.number_input('2 passageiros')
#             pedro[1] = st.number_input('3 passageiros')
#             pedro[2] = st.number_input('4 passageiros')
#             pedro[3] = st.number_input('5 passageiros')
#         with st.expander("Lucas"):
#             lucas[4] = st.number_input('2 passageiros')
#             lucas[5] = st.number_input('3 passageiros')
#             lucas[6] = st.number_input('4 passageiros')
#             lucas[7] = st.number_input('5 passageiros')
#         with st.expander("Gabriel"):
#             gabriel[4] = st.number_input('2 passageiros')
#             gabriel[5] = st.number_input('3 passageiros')
#             gabriel[6] = st.number_input('4 passageiros')
#             gabriel[7] = st.number_input('5 passageiros')
#         with st.expander("Leo"):
#             leo[4] = st.number_input('2 passageiros')
#             leo[5] = st.number_input('3 passageiros')
#             leo[6] = st.number_input('4 passageiros')
#             leo[7] = st.number_input('5 passageiros')

   

# with st.expander("Total à pagar"):
#     with st.expander("Para o Pedro"):
#         carlos[8] = (rides[0]*carlos[0])+(rides[1]*carlos[1])+(rides[2]*carlos[2])+(rides[3]*carlos[3])
#         st.write('Carlos = ' + carlos[8])

#         lucas[8] = (rides[0]*lucas[0])+(rides[1]*lucas[1])+(rides[2]*lucas[2])+(rides[3]*lucas[3])
#         st.write('Lucas = ' + lucas[8])

#         gabriel[8] = (rides[0]*gabriel[0])+(rides[1]*gabriel[1])+(rides[2]*gabriel[2])+(rides[3]*gabriel[3])
#         st.write('Gabriel = ' + gabriel[8])

#         leo[8] = (rides[0]*leo[0])+(rides[1]*leo[1])+(rides[2]*leo[2])+(rides[3]*leo[3])
#         st.write('Leo = ' + leo[8])

#         giovanna[8] = (rides[0]*giovanna[0])+(rides[1]*giovanna[1])+(rides[2]*giovanna[2])+(rides[3]*giovanna[3])
#         st.write('Giovanna = ' + giovanna[8])

#         giovana[8] = (rides[0]*giovana[0])+(rides[1]*giovana[1])+(rides[2]*giovana[2])+(rides[3]*giovana[3])
#         st.write('Giovana = ' +  giovana[8])

#     with st.expander("Para o Carlos"):
#         pedro[4] = (rides[4]*pedros[0])+(rides[5]*pedro[1])+(rides[6]*pedro[2])+(rides[7]*pedro[3])
#         st.write('Pedro = ' + pedro[4])

#         lucas[9] = (rides[4]*lucas[4])+(rides[5]*lucas[5])+(rides[6]*lucas[6])+(rides[7]*lucas[7])
#         st.write('Lucas = ' + lucas[9])

#         gabriel[9] = (rides[4]*gabriel[4])+(rides[5]*gabriel[5])+(rides[6]*gabriel[6])+(rides[7]*gabriel[7])
#         st.write('Gabriel = ' + gabriel[9])

#         leo[9] = (rides[4]*leo[4])+(rides[5]*leo[5])+(rides[6]*leo[6])+(rides[7]*leo[7])
#         st.write('Leo = '+ leo[9])
