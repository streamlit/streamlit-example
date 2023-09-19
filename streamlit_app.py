import altair as alt
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

#######################################################

# Título da página
st.title("Filtros para Gráfico de Dispersão")

# Filtrar por NDA (Multiselect com opção "Selecionar Todos")
st.subheader("Filtrar por NDA:")
nda_options = list(range(1, 366))  # Lista de 1 a 365
nda_options.insert(0, "Selecionar Todos")
nda_selected = st.multiselect("Selecione o(s) NDA(s):", nda_options, default=["Selecionar Todos"])

# Filtrar por Dia (Multiselect com opção "Selecionar Todos")
st.subheader("Filtrar por Dia:")
dia_options = list(range(1, 32))  # Lista de 1 a 31
dia_options.insert(0, "Selecionar Todos")
dia_selected = st.multiselect("Selecione o(s) Dia(s):", dia_options, default=["Selecionar Todos"])

# Filtrar por Mês (Multiselect com opção "Selecionar Todos")
st.subheader("Filtrar por Mês:")
mes_options = list(range(1, 13))  # Lista de 1 a 12
mes_options.insert(0, "Selecionar Todos")
mes_selected = st.multiselect("Selecione o(s) Mês(es):", mes_options, default=["Selecionar Todos"])


st.subheader("Filtrar por Ano:")
ano_options = [2021, 2022]  # Lista de 2021 a 2022
ano_options.insert(0, "Selecionar Todos")
ano_selected = st.multiselect("Selecione o(s) Ano(es):", ano_options, default=["Selecionar Todos"])


# Filtrar por Hora (Multiselect com opção "Selecionar Todos")
st.subheader("Filtrar por Hora:")
hora_options = list(range(24))  # Lista de 0 a 23
hora_options.insert(0, "Selecionar Todos")
hora_selected = st.multiselect("Selecione a(s) Hora(s):", hora_options, default=["Selecionar Todos"])

# Aplicar filtros
if "Selecionar Todos" in nda_selected:
    nda_selected = nda_options[1:]  # Remover "Selecionar Todos" se selecionado
if "Selecionar Todos" in dia_selected:
    dia_selected = dia_options[1:]  # Remover "Selecionar Todos" se selecionado
if "Selecionar Todos" in mes_selected:
    mes_selected = mes_options[1:]  # Remover "Selecionar Todos" se selecionado
if "Selecionar Todos" in hora_selected:
    hora_selected = hora_options[1:]  # Remover "Selecionar Todos" se selecionado

# Aplicar filtros
filtered_df = df[
    (df['NDA'].isin(nda_selected)) &
    (df['Dia'].isin(dia_selected)) &
    (df['Mes'].isin(mes_selected)) &
    (df['Ano'] == ano_selected) &
    (df['Hora'].isin(hora_selected))
]

# Gráfico de Dispersão com os dados filtrados
st.subheader("Gráfico de Dispersão com Filtros Aplicados:")
x_column = st.selectbox("Selecione a coluna para o eixo X:", filtered_df.columns)
y_column_primary = st.selectbox("Selecione a coluna para o eixo Y principal:", filtered_df.columns)
y_column_secondary = st.selectbox("Selecione a coluna para o eixo Y secundário:", filtered_df.columns)

# Crie o gráfico de dispersão com eixo secundário
scatter_chart_primary = alt.Chart(filtered_df).mark_circle().encode(
    x=alt.X(x_column, axis=alt.Axis(title='Eixo X Principal')),
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
