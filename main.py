import streamlit as st
import joblib
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import shap
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.metrics import accuracy_score, precision_score
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.set_option('deprecation.showPyplotGlobalUse', False)

dtc_model = joblib.load('modelo_dtc_tunned.sav')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("NeoVision")

# NAVBAR

selected = option_menu(
    menu_title=None,
    options=["Sobre", "Modelo", "Dataset"],
    icons=["house", "activity", "clipboard"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important"},
        "nav-link-selected": {"background-color": "#904bff"}
    }
)


if selected == "Sobre":
    st.title('Modelo Preditivo para escolha do Tratamento no Câncer de Mama')

    st.title(f"{selected}")

    image = Image.open("time-neovision.png")
    st.image(image, caption="Time Neovision - Estudantes do Inteli")

    st.subheader("Objetivo")
    st.markdown("O principal objetivo do projeto é criar um modelo preditivo que categorize qual tratamento é mais recomendado para casos de câncer de mama para pacientes do Instituto de Câncer de São Paulo (ICESP), conforme o perfil e dados disponibilizados desses pacientes. Os tipos de tratamentos foram restringidos em 2 principais: neo, que consiste em 1º quimioterapia e 2º cirurgia, ou adjuvante, que consiste em 1º cirurgia e 2º terapia. O intuito é gerar mais eficiência e possibilidade de revisão de diagnósticos.")

    st.subheader("Proposta de solução")
    st.markdown("A nossa proposta de solução envolve o consumo de dados que começaram a ser coletados a partir de 2008 de pacientes diagnosticados com câncer de mama. Através deles, será aplicado técnicas de machine learning para criação de modelos de classificações a fim de identificar o melhor tipo de tratamento (neo ou adjuvante), de acordo com o perfil e dados de cada paciente. Dessa forma, a classificação irá auxiliar os médicos responsáveis na decisão de qual tratamento recomendar ao paciente.")

    st.subheader("Justificativa")
    st.markdown("O uso de modelo preditivo é sem dúvidas uma excelente alternativa, pois o tratamento de câncer de mama se enquadra em casos que não sabemos exatamente o comportamento do fenômeno, ou seja, há uma grande influência da ótica de cada profissional de acordo com sua experiência. Com isso, como a IA trabalha diretamente com padrões, é possível ter uma acurácia pelo menos tão boa quanto a de profissionais formados. Além disso, a tecnologia apenas será utilizada para auxiliar na decisão, ou seja, a decisão final ainda será dos médicos, em que terão à disposição uma tecnologia que possibilitará ter mais assertividade na escolha do tratamento a sugerir.")

    st.subheader("Agradecimentos")
    st.markdown("Gostaríamos de agradecer o Inteli (Instituto de Tecnologia e Liderança) e o ICESP (Instituto do Câncer do Estado de São Paulo) pela oportunidade.")


if selected == "Modelo":
    print(dtc_model)

    st.title(f"{selected}")
    st.markdown(
        "Adicione os dados do paciente para prever a escolha do tratamento.")

    with st.form("form_features"):
        idade_primeiro_diagnostico = st.slider(
            "Digite sua idade no primeiro diagnóstico?", 0, 100, 25)
        print(f"\n{idade_primeiro_diagnostico}")

        if idade_primeiro_diagnostico <= 45:
            grupo_idade = "Menor que 45"
            grupo_idade_encoded = 2
        if idade_primeiro_diagnostico > 45 and idade_primeiro_diagnostico < 60:
            grupo_idade = "Entre 45 e 60"
            grupo_idade_encoded = 0
        if idade_primeiro_diagnostico >= 60:
            grupo_idade = "Maior que 60"
            grupo_idade_encoded = 1

        dict_classific_tnm_t1 = {'3': 7,
                                 '1C': 4,
                                 '1': 1,
                                 '4B': 10,
                                 '2': 6,
                                 '1B': 3,
                                 'IS': 14,
                                 '4D': 12,
                                 '4': 8,
                                 '1A': 2,
                                 'X - Não foi possível determinar': 15,
                                 '4C': 11,
                                 '1MIC': 5,
                                 '4A': 9,
                                 'Y: NA': 16,
                                 'CDIS': 13,
                                 '0': 0,
                                 }
        classific_tnm_t1 = st.selectbox('Selecione uma opção de TNM Clínico T1', list(
            dict_classific_tnm_t1.keys()), index=0)
        valor_tnm_t1 = dict_classific_tnm_t1.get(classific_tnm_t1)
        print(f"Esse é o keys do tnm T1: {classific_tnm_t1}")
        print(f"Esse é o values do tnm T1: {valor_tnm_t1}")

        dict_classific_tnm_n1 = {'1': 1,
                                 '2': 2,
                                 '0': 0,
                                 '2A': 3,
                                 '3A': 6,
                                 'X - Não foi possível determinar': 9,
                                 '3': 5,
                                 '2B': 4,
                                 '3B': 7,
                                 '3C': 8,
                                 'Y: Na': 10
                                 }
        classific_tnm_n1 = st.selectbox('Selecione uma opção de TNM Clínico N1:', list(
            dict_classific_tnm_n1.keys()), index=0)
        valor_tnm_n1 = dict_classific_tnm_n1.get(classific_tnm_n1)
        print(f"Esse é o keys do tnm N1: {classific_tnm_n1}")
        print(f"Esse é o values do tnm N1: {valor_tnm_n1}")

        dict_classific_tnm_m1 = {'0': 0,
                                 '1': 1,
                                 'X - Não foi possível determinar': 2,
                                 'Y: Na': 3
                                 }

        classific_tnm_m1 = st.selectbox('Selecione uma opção de TNM Clínico M1:', list(
            dict_classific_tnm_m1.keys()), index=0)
        valor_tnm_m1 = dict_classific_tnm_m1.get(classific_tnm_m1)
        print(f"Esse é o keys do tnm M1: {classific_tnm_m1}")
        print(f"Esse é o values do tnm M1: {valor_tnm_m1}")

        dict_estagio_tumor = {'I': 0,
                              'II': 1,
                              'III': 2,
                              'IV': 3,
                              'nan': 4
                              }

        estagio_tumor = st.selectbox('Selecione qual é o Estágio do Tumor: ', list(
            dict_estagio_tumor.keys()), index=0)
        valor_estagio_tumor = dict_estagio_tumor.get(estagio_tumor)
        print(f"Esse é o keys do Estágio do tumor: {estagio_tumor}")
        print(f"Esse é o values Estágio do tumor: {valor_estagio_tumor}")

        dict_possui_metastase = {'Não': 0,
                                 'Sim': 1
                                 }

        possui_metastase = st.selectbox('Possui Metástase? ', list(
            dict_possui_metastase.keys()), index=0)
        valor_possui_metastase = dict_possui_metastase.get(possui_metastase)
        print(f"Esse é o keys do Possui Metastase: {possui_metastase}")
        print(f"Esse é o values do Possui Metastase: {valor_possui_metastase}")

        dict_risk_metastase = {'0.0': 0,
                               '2.0': 1,
                               '3.0': 2
                               }

        risk_metastase = st.selectbox('Qual é o risco de possuir metástase? ', list(
            dict_risk_metastase.keys()), index=0)
        valor_risk_metastase = dict_risk_metastase.get(risk_metastase)
        print(f"Esse é o keys do Risk Metastase: {risk_metastase}")
        print(f"Esse é o values do Risk Metastase: {valor_risk_metastase}")

        dict_tipo_histologico = {
            'NÃO-ESPECIAL - Carcinoma de mama ductal invasivo (CDI)/SOE': 0,
            'Carcinoma mamário invasivo multifocal': 0,
            'Tumor PHYLLODES maligno': 0,
            'Carcinoma de mama mucinoso': 0,
            'Carcinoma lobular pleomórfico': 0,
            'Carcinoma de mama tubular': 0,
            'Carcinoma de mama papilifero': 0,
            'Carcinoma de mama misto (ductal e micropapilífero) invasivo': 0,
            'Carcinoma de mama medular': 0,
            'Carcinoma de mama metaplasico': 0,
            'Carcinoma de mama micropapilar': 1,
            'Carcinoma de mama lobular invasivo': 0,
            'Carcinoma de mama misto (ductal e lobular) invasivo': 0,
            'CARCINOMA MAMÁRIO INVASIVO DO TIPO APÓCRINO': 0,
            'Adenomioepitelioma maligno': 0,
            'Carcinoma de mama cistico adenoide': 1,
            'Carcinoma de mama lobular in situ': 0,
            'Outros': 0
        }

        tipo_histologico = st.selectbox('Qual é o tipo histológico? ', list(
            dict_tipo_histologico.keys()), index=0)
        valor_tipo_histologico = dict_tipo_histologico.get(tipo_histologico)
        print(f"Esse é o keys do Tipo Histológico: {tipo_histologico}")
        print(f"Esse é o values do Tipo Histológico: {valor_tipo_histologico}")

        if tipo_histologico == 'Carcinoma de mama cistico adenoide' and valor_tipo_histologico == 1:
            carcinoma_adenoide = 1
            carcinoma_adenoide_value = 'Carc. adenoide'
            print("Este é o if do carcinoma adenoide\n")
            print(carcinoma_adenoide)

        else:
            carcinoma_adenoide = 0
            carcinoma_adenoide_value = 'Carc. adenoide 0'

        if tipo_histologico == 'Carcinoma de mama micropapilar' and valor_tipo_histologico == 1:
            carcinoma_micropapilar = 1
            carcinoma_micropapilar_value = 'Carc. micropapilar'

            print("Este é o if do carcinoma micropapilar\n")
            print(carcinoma_micropapilar)
        else:
            carcinoma_micropapilar = 0
            carcinoma_micropapilar_value = 'Carc. micropapilar 0'
        dict_cod_topografia_cid = {
            'C508': 1,
            'C509': 0,
            'C504': 0,
            'C505': 0,
            'C501': 0,
            'C502': 1,
            'C503': 0,
            'C500': 0,
            'C506': 0,
            'C180': 0,
            'C209': 0
        }

        cod_topografia_cid = st.selectbox('Qual é o Código da Topografia CID? ', list(
            dict_cod_topografia_cid.keys()), index=0)
        valor_cod_topografia_cid = dict_cod_topografia_cid.get(
            cod_topografia_cid)
        print(
            f"Esse é o keys do Código da Topografia CID: {cod_topografia_cid}")
        print(
            f"Esse é o values do Código da Topografia CID: {valor_cod_topografia_cid}")

        if cod_topografia_cid == '502' and valor_cod_topografia_cid == 1:
            cod_topografia_cid_502 = 1
            cod_topografia_cid_502_value = '502'

        else:
            cod_topografia_cid_502 = 0
            cod_topografia_cid_502_value = '502 - 0'

        if cod_topografia_cid == '508' and valor_cod_topografia_cid == 1:
            cod_topografia_cid_508 = 1
            cod_topografia_cid_508_value = '508'

        else:
            cod_topografia_cid_508 = 0
            cod_topografia_cid_508_value = '508 - 0'

        submit_model = st.form_submit_button(label='Enviar',
                                             help='Clique para enviar',
                                             type='primary')

        features = [grupo_idade_encoded, valor_tnm_t1, valor_tnm_n1, valor_tnm_m1, valor_estagio_tumor, valor_possui_metastase,
                    valor_risk_metastase, carcinoma_adenoide, carcinoma_micropapilar, cod_topografia_cid_502, cod_topografia_cid_508]

        features_categ = [grupo_idade, classific_tnm_t1, classific_tnm_n1, classific_tnm_m1, estagio_tumor, possui_metastase,
                          risk_metastase, carcinoma_adenoide_value, carcinoma_micropapilar_value, cod_topografia_cid_502_value, cod_topografia_cid_508_value]

        if submit_model:
            predicao_modelo = dtc_model.predict([features])
            # accuracy = dtc_model.score(predicao_modelo)
            # print(accuracy)

            # y_test = dtc_model(['y_test_new'])

            # accuracy = accuracy_score(y_test, predicao_modelo)
            # precision = precision_score(y_test, predicao_modelo)

            st.subheader(f"Tratamento indicado: {predicao_modelo[0]}")
            st.markdown(
                f"O melhor tratamento previsto foi {predicao_modelo[0]}. Isso significa que esse resultado serve apenas de suporte ao médico e não deve ser 100% confiavel.")

            explainer = shap.TreeExplainer(dtc_model)

            features_array = np.array(features)
            # shap_values= explainer.shap_values(features_array)

            shap_values = explainer.shap_values(features_array)

            # expl= shap.Explanation(shap_values, features_array)

            shap_values_array = np.vstack(shap_values)
            st.subheader('Valores que o modelo está dando mais importância:')

            plt.title('Importância das Features')
            shap.summary_plot(shap_values_array,
                              features_categ, plot_type='bar')
            st.pyplot(bbox_inches='tight')

            # plt.title('visualize all the training set predictions')
            # shap.plots.force(explainer.expected_value, shap_values_array)
            # st.pyplot(bbox_inches='tight')


if selected == 'Dataset':
    st.markdown(
        "Adicione um arquivo CSV para obter a predição em massa de pacientes.")

    data_file = st.file_uploader("Upload CSV", type=["csv"])
    if data_file is not None:
        st.write(type(data_file))
        file_details = {"filename": data_file.name,
                        "filetype": data_file.type,
                        "filesize": data_file.size}
        st.write(file_details)
        df = pd.read_csv(data_file, sep=';', encoding="ISO-8859-1")

        le = joblib.load('label_encoding.sav')

        def label_encode_cat(df, columns):
            df_desencoded = df.copy()
            for column in columns:
                # df[column] = df[column].fillna('')
                df_desencoded[f"{column}_desenconded"] = df[column]
                df_desencoded[column] = le.fit_transform(df[column])
                df[column] = le.fit_transform(df[column])
            return df, df_desencoded

        lista_colunas_label_encode = [
            'grupo_idade',
            'classificacao_tnm_clinico_m_1',
            'classificacao_tnm_clinico_n_1',
            'classificacao_tnm_clinico_t_1',
            'possui_metastase',
            'risk_metastase',
            'estagio_tumor',
        ]

        df_encoded, df_desencoded = label_encode_cat(
            df, lista_colunas_label_encode)

        def one_hot_encoding_cat(df, columns):
            for column in columns:
                df = pd.concat(
                    [df, pd.get_dummies(df[column], prefix=column)], axis=1)
                df.drop(column, axis=1, inplace=True)
            return df

        lista_colunas_one_hot_encode = [
            'tipo_histologico',
            'codigo_da_topografia_cid_o_1'
        ]
        df_original = one_hot_encoding_cat(
            df_encoded, lista_colunas_one_hot_encode)
        df_sem_target = df_original.drop('regime_de_tratamento', axis=1)

        features_para_df = [
            'grupo_idade',
            'classificacao_tnm_clinico_m_1',
            'classificacao_tnm_clinico_n_1',
            'classificacao_tnm_clinico_t_1',
            'possui_metastase',
            'risk_metastase',
            'estagio_tumor',
            'tipo_histologico_Carcinoma de mama cistico adenoide',
            'tipo_histologico_Carcinoma de mama micropapilar',
            'codigo_da_topografia_cid_o_1_C502',
            'codigo_da_topografia_cid_o_1_C508'
        ]

        df_features = df_sem_target[features_para_df]
        df_predicao = dtc_model.predict(df_features)
        df_original['regime_de_tratamento'] = df_predicao

        def convert_df_to_csv(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df_to_csv(df_original)

        st.download_button(
            label="Baixar arquivo com todas as predições",
            data=csv,
            file_name='Modelo_Predição.csv',
            mime='text/csv',
        )
        st.dataframe(df_original)
