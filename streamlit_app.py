# Exemplo de solicitação de dados meteorológicos da NASA Power

import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# URL da API do NASAPower
nasapower_api_url = "https://power.larc.nasa.gov/api/temporal/hourly/point"

# Função para validar e formatar a data corretamente
def format_date(date_str):
    try:
        datetime.strptime(date_str, "%Y%m%d%H")
        return date_str
    except ValueError:
        st.error("Por favor, forneça uma data no formato YYYYMMDDHH.")
        return None

# Crie uma função para fazer solicitações à API
def get_nasapower_data(start, end, latitude, longitude, community, parameters, format_type):
    params = {
        "start": start,
        "end": end,
        "latitude": latitude,
        "longitude": longitude,
        "community": community,
        "parameters": parameters,
        "format": format_type,
    }

    response = requests.get(nasapower_api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error(f"Erro ao obter dados da API. Código de status: {response.status_code}")
        st.write(response.text)  # Isso exibirá a resposta da API para diagnóstico
        return None

st.title("Dados Meteorológicos da NASA Power")

# Adicione campos de entrada para os parâmetros da API
start_date = st.text_input("Data de Início (formato YYYYMMDDHH):")
end_date = st.text_input("Data de Término (formato YYYYMMDDHH):")
latitude = st.number_input("Latitude:")
longitude = st.number_input("Longitude:")
community = st.selectbox("Comunidade de Usuários:", ["ag", "sb", "re"])
parameters = st.text_input("Parâmetros (separados por vírgula):")
format_type = st.selectbox("Formato de Saída:", ["json", "text/ascii", "text/csv"])

# Crie um botão para fazer a solicitação à API
if st.button("Obter Dados"):
    # Valide e formate as datas antes de fazer a solicitação
    start_date_formatted = format_date(start_date)
    end_date_formatted = format_date(end_date)

    if start_date_formatted and end_date_formatted:
        # Remova os parâmetros inválidos
        parameters = parameters.replace("SRAD", "")
        parameters = parameters.replace("VPD", "")

        data = get_nasapower_data(
            start_date_formatted,
            end_date_formatted,
            latitude,
            longitude,
            community,
            parameters,
            format_type,
        )

        if data:
            # Converter dados JSON em um DataFrame do Pandas para exibi-lo em uma tabela
            df = pd.json_normalize(data["features"][0]["properties"]["parameter"])
            st.write("Dados Recebidos:")
            st.write(df)
