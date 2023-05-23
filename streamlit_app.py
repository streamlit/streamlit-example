import altair as alt
import pandas as pd
import streamlit as st
import pickle
import numpy as np
from PIL import Image
st.title("Курсовая работа")
st.write("Выполнили: Данилов Д.С. / Федоров А.С.")
st.write("Группа: МИИ-22")
# Загрузка моделей
with open('new_model.pkl', 'rb') as alc_model1_pkl:
    lr_alc1 = pd.read_pickle(alc_model1_pkl)
with open('drug_model.pkl', 'rb') as drug_model1_pkl:
    lr_drug1 = pd.read_pickle(drug_model1_pkl)
with open('.pkl', 'rb') as alc_model2_pkl:
    lr_alc2 = pd.read_pickle(alc_model2_pkl)
with open('.pkl', 'rb') as drug_model2_pkl:
    lr_drug2 = pd.read_pickle(drug_model2_pkl)
    
image = Image.open('media/alcohol.jpg')

st.header("Настраиваемые данные")   
# Данные введенные пользователем
unseen = st.slider("Количество безработных (в тыс. человек)", min_value = 20.0, max_value = 200.0, step = 0.1)
decimal = st.slider("Знаки после запятой", min_value = 0, max_value = 10, step = 1)

# Прогноз
X_test_sm = [[float(1.0)], [float(unseen)]]
X_test_sm = np.squeeze(X_test_sm)
result_alc_model1 = lr_alc1.predict(X_test_sm)[0]
result_drug_model1 = lr_drug1.predict(X_test_sm)[0]
result_alc_model2 = lr_acl2.predict()
result_drug_model2 = lr_drug2.predict()

@st.cache_data
def delta_model1():
    a = result_alc_model1
    b = result_drug_model1
    c = unseen
    return a, b, c

@st.cache_data
def delta_model2():
    a = result_alc_model2
    b = result_drug_model2
    c = unseen
    return a, b, c

delta_alc_model1, delta_drug_model1, delta_unseen_model1 = delta_model1()
delta_alc_model2, delta_drug_model2, delta_unseen_model2 = delta_model2()

st.write("Нажмите на кнопку, затем укажите сверху данные (количество безработных), которые хотите сравнивать.")
if st.button("Сравнить"):
    st.cache_data.clear()
# Вывод  

tab_model_1, tab_model_2 = st.tabs(["Линейная регрессия", "Градиентный бустинг"])

with tab_model_1:

    st.header("Метрика")    
    col1, col2, col3= st.columns(3)    


    if (result_alc_model1 > 0) and (result_drug_model1 > 0):
        col1.metric(label = "Количество алкоголиков", value = str(result_alc_model1)[:(len(str(int(result_alc_model1))) + decimal + 1)], delta = str(result_alc_model1-delta_alc_model1)[:(len(str(int(result_alc_model1-delta_alc_model1))) + decimal + 1)], delta_color = "inverse")
        col2.metric(label = "Количество наркоманов", value = str(result_drug_model1)[:(len(str(int(result_drug_model1))) + decimal + 1)], delta = str(result_drug_model1-delta_drug_model1)[:(len(str(int(result_drug_model1-delta_drug_model1))) + decimal + 1)], delta_color = "inverse")
        col3.metric(label = "Количество безработных", value = str(unseen)[:(len(str(int(unseen))) + decimal + 1)], delta = str(unseen-delta_unseen_model1)[:(len(str(int(unseen-delta_unseen_model1))) + decimal + 1)], delta_color = "inverse")
        source1_model1 = pd.DataFrame({
        'Прогноз': ['Безраб.', 'Алк.', 'Нарк.'],
        'Количество людей в тыс': [unseen, result_alc_model1, result_drug_model1]})
        source2_model1 = pd.DataFrame({
        'Прогноз': ['Алк.', 'Нарк.'],
        'Количество людей в тыс': [result_alc_model1, result_drug_model1]})
    else:
        col1.metric(label = "Количество алкоголиков", value = 0, delta = str(result_alc_model1-delta_alc_model1)[:(len(str(int(result_alc_model1-delta_alc_model1))) + decimal + 1)], delta_color = "inverse")
        col2.metric(label = "Количество наркоманов", value = 0, delta = str(result_drug_model1-delta_drug_model1)[:(len(str(int(result_drug_model1-delta_drug_model1))) + decimal + 1)], delta_color = "inverse")
        col3.metric(label = "Количество безработных", value = str(unseen)[:(len(str(int(unseen))) + decimal + 1)], delta = str(unseen-delta_unseen_model1)[:(len(str(int(unseen-delta_unseen_model1))) + decimal + 1)], delta_color = "inverse")
        source1_model1 = pd.DataFrame({
        'Прогноз': ['Безраб.', 'Алк.', 'Нарк.'],
        'Количество людей в тыс': [unseen, 0, 0]})
        source2_model1 = pd.DataFrame({
        'Прогноз': ['Алк.', 'Нарк.'],
        'Количество людей в тыс': [0, 0]})

    st.header("Столбчатая диаграмма")         
    tab_diagram_1, tab_diagram_2 = st.tabs(["Алк/Нарк", "Алк/Безраб/Нарк"])
    with tab_diagram_1:
        st.altair_chart(alt.Chart(pd.DataFrame(source2_model1)).mark_bar().encode(x = 'Прогноз', y = 'Количество людей в тыс'), use_container_width = True)
    with tab_diagram_2:
        st.altair_chart(alt.Chart(pd.DataFrame(source1_model1)).mark_bar().encode(x = 'Прогноз', y = 'Количество людей в тыс'), use_container_width = True)

with tab_model_2:
    st.write('check')

st.header("Почему это важно")    
st.write("<p style='text-align: justify;'><span>Прогнозирование количества людей с алкогольной и наркотической зависимостью от количества безработных имеет большое значение для разработки эффективных социальных программ и мер для борьбы с наркотиками и алкогольной зависимостью.</span></p>", unsafe_allow_html=True)
st.write("<p style='text-align: justify;'><span>Безработные люди имеют повышенный риск развития алкогольной и наркотической зависимости, так как они часто сталкиваются с социальным и психологическим стрессом, чувством безнадёжности и неуверенности в будущем.</span></p>", unsafe_allow_html=True)
st.write("<p style='text-align: justify;'><span>Учитывая все вышеперечисленные факторы, прогнозирование количества людей с алкогольной и наркотической зависимостью от количества безработных позволяет руководителям и специалистам в области здравоохранения и социальной защиты разработать целенаправленные программы и меры для профилактики и лечения этих проблем. Это также может помочь определить необходимость расширения и усиления социальной поддержки и проведения образовательных программ для безработных людей.</span></p>", unsafe_allow_html=True)
st.image(image)
st.info('Круглосуточная горячая линия по вопросам алкоголизма и наркомании: 8 800 551-70-14', icon="ℹ️")

