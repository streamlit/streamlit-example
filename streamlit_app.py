from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

# Carregue o DataFrame a partir do arquivo CSV
df = pd.read_csv("./trabalho_microclimatologia.csv")

# Título da página
st.title("Apresentação dos Dados")

# Exiba a tabela com os dados
st.write(df)
