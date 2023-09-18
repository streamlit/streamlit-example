from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
# Após a criação do DataFrame 'data'
df = pd.DataFrame(data)

# Salvar o DataFrame como um arquivo CSV
df.to_csv("./trabalho_microclimatologia.csv", index=False)


st.title('Meus dados')
    

read_file.to_csv ("./trabalho_microclimatologia.csv",
                  index = None,
                  header=True)
