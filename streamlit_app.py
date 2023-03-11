# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import forex_python.converter as fpc

currencies = ['USD', 'EUR', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF']

st.title('Conversor de moedas')

base_currency = st.selectbox('Selecione a moeda base:', currencies)
target_currency = st.selectbox('Selecione a moeda de destino:', currencies)

amount = st.number_input('Insira a quantidade a ser convertida:', value=1.00)

result = fpc.CurrencyRates().convert(base_currency, target_currency, amount)

st.write(f'{amount:.2f} {base_currency} = {result:.2f} {target_currency}')
