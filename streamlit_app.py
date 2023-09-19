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
st.title("Gráfico de Dispersão com Eixo Secundário")

# Escolha as colunas para o eixo Y (principal) e Y2 (secundário)
y_column_primary_options = ['NDA', 'Dia', 'Mes', 'Ano', 'Hora']
y_column_primary = st.selectbox("Selecione a coluna para o eixo Y principal:", y_column_primary_options)

y_column_secondary = st.selectbox("Selecione a coluna para o eixo Y secundário:", df.columns)

# Crie um multi-select drop-down list para o eixo X
x_columns_selected = st.multiselect("Selecione as colunas para o eixo X:", df.columns)

# Verifique se pelo menos uma coluna foi selecionada
if not x_columns_selected:
    st.warning("Selecione pelo menos uma coluna para o eixo X.")
else:
    # Configurações específicas para cada coluna
    if y_column_primary == 'NDA':
        nda_min = st.slider("Selecione o valor mínimo de NDA:", 1, 365, 1)
        nda_max = st.slider("Selecione o valor máximo de NDA:", nda_min, 365, 365)
    elif y_column_primary == 'Dia':
        dia_min = st.slider("Selecione o valor mínimo do Dia:", 1, 31, 1)
        dia_max = st.slider("Selecione o valor máximo do Dia:", dia_min, 31, 31)
    elif y_column_primary == 'Mes':
        mes_min = st.slider("Selecione o valor mínimo do Mês:", 1, 12, 1)
        mes_max = st.slider("Selecione o valor máximo do Mês:", mes_min, 12, 12)
    elif y_column_primary == 'Ano':
        ano_options = [2021, 2022]
        ano = st.selectbox("Selecione o ano:", ano_options)
    elif y_column_primary == 'Hora':
        hora_min = st.slider("Selecione o valor mínimo da Hora:", 0, 23, 0)
        hora_max = st.slider("Selecione o valor máximo da Hora:", hora_min, 23, 23)

    # Crie o gráfico de dispersão com eixo secundário
    scatter_chart_primary = alt.Chart(df).mark_circle().encode(
        x=alt.X(x_columns_selected[0], axis=alt.Axis(title='Eixo X Principal')),  # Use a primeira coluna selecionada
        y=alt.Y(y_column_primary, axis=alt.Axis(title='Eixo Y Principal')),
        tooltip=[x_columns_selected[0], y_column_primary]
    ).properties(
        width=600  # Defina a largura do gráfico
    )

    scatter_chart_secondary = alt.Chart(df).mark_circle().encode(
        x=alt.X(x_columns_selected[0], axis=None),  # Use um eixo sem rótulos
        y=alt.Y(y_column_secondary, axis=alt.Axis(title='Eixo Y Secundário')),
        tooltip=[x_columns_selected[0], y_column_secondary],
        color=alt.value('red')  # Cor dos pontos no eixo secundário
    )

    # Combine os gráficos usando layer (camada)
    combined_chart = alt.layer(scatter_chart_primary, scatter_chart_secondary)

    # Exiba o gráfico com eixo secundário
    st.altair_chart(combined_chart, use_container_width=True)
