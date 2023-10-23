#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import streamlit as st
import joblib
from joblib import load
#modelo = joblib.load('modelo.joblib')


# In[6]:


modelo = joblib.load('modelo.joblib')
x_num = {'acumulado':0, 'MTBF':0}


# In[7]:


for item in x_num:
    
    valor = st.number_input(f'{item}')
    
botao = st.button('Previsão de custo de peças')

