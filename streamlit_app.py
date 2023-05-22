from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pickle
import numpy as np
import plotly.express as px

# Загрузка моделей
with open('new_model.pkl', 'rb') as alc_model_pkl:
    lr_alc = pd.read_pickle(alc_model_pkl)
with open('drug_model.pkl', 'rb') as drug_model_pkl:
    lr_drug = pd.read_pickle(drug_model_pkl)



# Данные введенные пользователем
unseen = st.slider("Количество безработных (в тыс. человек)", min_value = 20.0, max_value = 200.0, step = 0.1)
decimal = st.slider("Знаки после запятой", min_value = 0, max_value = 10, step = 1)
X_test_sm = [[float(1.0)], [float(unseen)]]
X_test_sm = np.squeeze(X_test_sm)

# Прогноз
result_alc = lr_alc.predict(X_test_sm)[0]
result_drug = lr_drug.predict(X_test_sm)[0]
delta_alc = 0
delta_drug = 0

# Вывод
col1, col2= st.columns(2)
if (result_alc > 0) and (result_drug > 0):
    col1.metric(label = "Количество алкоголиков", value = str(result_alc)[:(len(str(int(result_alc)))+decimal+1)], delta = delta_alc-result_alc)
    col2.metric(label = "Количество наркоманов", value = str(result_drug)[:(len(str(int(result_drug)))+decimal+1)], delta = "1.2")
    source = pd.DataFrame({
    'a': ['Алкаши', 'Наркоши'],
    'b': [result_alc, result_drug]})
    de
else:
    col1.metric(label = "Количество алкоголиков", value = 0, delta = "1.2")
    col2.metric(label = "Количество наркоманов", value = 0, delta = "1.2")
    source = pd.DataFrame({
    'a': ['Алкаши', 'Наркоши'],
    'b': [0, 0]})

# Подсчет разницы
if delta_alc != result_alc:
    delta_alc = result_alc

st.altair_chart(alt.Chart(pd.DataFrame(source), height = 500, width = 500)
                .mark_bar()
                .encode(x='a', y='b'))




