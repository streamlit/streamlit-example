import altair as alt
import math
import pandas as pd
import streamlit as st

# Carregue o DataFrame a partir do arquivo CSV
df = pd.read_csv("./trabalho_microclimatologia.csv")

# Defina o título da página
st.title("Análise Exploratória dos Dados")

# Exiba um texto explicativo antes da tabela de dados
st.write("Aqui estão os dados do seu arquivo CSV:")

# Exiba a tabela com os dados
st.write(df)

# Adicione mais texto explicativo após a tabela
st.write("Agora, vamos incluir uma coluna 'hora_min' aos dados para facilitar a hora do dia:")

# Calcule as horas e minutos separadamente
df['horas'] = df['Hora'].astype(int)  # Parte inteira como horas
df['minutos'] = ((df['Hora'] - df['horas']) * 60).astype(int)  # Parte decimal como minutos

# Combine as horas e minutos no formato 'hora:minuto'
df['hora_min'] = df['horas'].astype(str).str.zfill(2) + ':' + df['minutos'].astype(str).str.zfill(2)

# Mais transformações nos dados...

# Exiba a tabela de dados transformados
st.write("Aqui estão os novos dados:")

# Reorganize as colunas para ter 'hora_min' entre 'Hora' e 'h'
df = df[['NDA', 'Dia', 'Mes', 'Ano', 'Hora', 'hora_min', 'h', 'Declinacao solar', 'hn', 'N', 'ns', 'ps', 'Zn', '(D/d)2', 'Ih', 'Qg', 'PARi', 'PARi corrigida', 'k', 'Tar', 'IAF', 'IAF.1', 'PARt', 'PARa', 'Assimilacao CO2 (milimol/m2.s)', 'Produçcao Glicose (g Glicose/m2.15min)']]

# Exiba a tabela com os dados transformados
st.write(df)

st.write("Para entender os tipos de dados, vamos usar df.info():")

# Crie um DataFrame com informações sobre o DataFrame principal
info_df = pd.DataFrame({
    'Nome da Coluna': df.columns,
    'Tipos de Dados': df.dtypes,
    'Valores Não Nulos': df.count(),
})

# Título para as informações
st.subheader("Informações sobre o DataFrame:")

# Exiba o DataFrame com as informações
st.write(info_df)

# Exiba estatísticas descritivas dos dados
st.write("Estatísticas Descritivas dos Dados:")
st.write(df.describe())

# Exiba estatísticas descritivas dos dados
st.write("Podemos selecionar apenas as colunas de interesse, antes de chamar o método df.describe() e arredondar os números para 2 casas após a vírgula com o método .round():")
selected_columns = ['Zn', 'k']
selected_stats = df[selected_columns].describe().round(2)
st.write(selected_stats)

# Exiba estatísticas descritivas de uma só variável 'Tar'
st.write("Estatísticas Descritivas de uma só variável 'Tar'")
tar_stats = df['Tar'].describe().round(2)
st.write(tar_stats)

# Carregue o DataFrame a partir do arquivo CSV
df = pd.read_csv("./trabalho_microclimatologia.csv")

#######################################################

# Título da página
st.title("Filtros para Gráfico de Dispersão")

# Filtrar por NDA (Checkbox)
st.subheader("Filtrar por NDA:")
nda_min = st.slider("NDA Mínimo:", min_value=1, max_value=365, value=1)
nda_max = st.slider("NDA Máximo:", min_value=1, max_value=365, value=365)

# Filtrar por Dia (Checkbox)
st.subheader("Filtrar por Dia:")
dia_min = st.slider("Dia Mínimo:", min_value=1, max_value=31, value=1)
dia_max = st.slider("Dia Máximo:", min_value=1, max_value=31, value=31)

# Filtrar por Mês (Checkbox)
st.subheader("Filtrar por Mês:")
mes_min = st.slider("Mês Mínimo:", min_value=1, max_value=12, value=1)
mes_max = st.slider("Mês Máximo:", min_value=1, max_value=12, value=12)

# Filtrar por Ano (Radio Button)
st.subheader("Filtrar por Ano:")
ano_options = [2021, 2022]
ano_selected = st.radio("Selecione o Ano:", ano_options)

# Filtrar por Hora (Checkbox)
st.subheader("Filtrar por Hora:")
hora_min = st.slider("Hora Mínima:", min_value=0, max_value=23, value=0)
hora_max = st.slider("Hora Máxima:", min_value=0, max_value=23, value=23)

# Aplicar filtros
filtered_df = df[
    (df['NDA'] >= nda_min) & (df['NDA'] <= nda_max) &
    (df['Dia'] >= dia_min) & (df['Dia'] <= dia_max) &
    (df['Mes'] >= mes_min) & (df['Mes'] <= mes_max) &
    (df['Ano'] == ano_selected) &
    (df['Hora'] >= hora_min) & (df['Hora'] <= hora_max)
]

# Gráfico de Dispersão com os dados filtrados
st.subheader("Gráfico de Dispersão com Filtros Aplicados:")
x_column = st.selectbox("Selecione a coluna para o eixo X:", filtered_df.columns)
y_column_primary = st.selectbox("Selecione a coluna para o eixo Y principal:", filtered_df.columns)
y_column_secondary = st.selectbox("Selecione a coluna para o eixo Y secundário:", filtered_df.columns)

# Crie o gráfico de dispersão com eixo secundário
scatter_chart_primary = alt.Chart(filtered_df).mark_circle().encode(
    x=x_column,
    y=alt.Y(y_column_primary, axis=alt.Axis(title='Eixo Y Principal')),
    tooltip=[x_column, y_column_primary]
).properties(
    width=600  # Defina a largura do gráfico
)

scatter_chart_secondary = alt.Chart(filtered_df).mark_circle().encode(
    x=alt.X(x_column, axis=None),  # Use um eixo sem rótulos
    y=alt.Y(y_column_secondary, axis=alt.Axis(title='Eixo Y Secundário')),
    tooltip=[x_column, y_column_secondary],
    color=alt.value('red')  # Cor dos pontos no eixo secundário
)

# Combine os gráficos usando layer (camada)
combined_chart = alt.layer(scatter_chart_primary, scatter_chart_secondary)

# Exiba o gráfico com eixo secundário
st.altair_chart(combined_chart, use_container_width=True)
