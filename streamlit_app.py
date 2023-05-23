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
with open('models/lr_alco.pkl', 'rb') as alc_model1_pkl:
    lr_alc = pd.read_pickle(alc_model1_pkl)
with open('models/lr_drug.pkl', 'rb') as drug_model1_pkl:
    lr_drug = pd.read_pickle(drug_model1_pkl)
with open('models/gboost_alco.pkl', 'rb') as alc_model2_pkl:
    gb_alc = pd.read_pickle(alc_model2_pkl)
with open('models/gboost_drug.pkl', 'rb') as drug_model2_pkl:
    gb_drug = pd.read_pickle(drug_model2_pkl)
    
image = Image.open('media/alcohol.jpg')

#st.header("Настраиваемые данные")   
# Данные введенные пользователем
#unseen = st.slider("Количество безработных (в тыс. человек)", min_value = 20.0, max_value = 200.0, step = 0.1)
#decimal = st.slider("Знаки после запятой", min_value = 0, max_value = 10, step = 1)

# Прогноз

#X_test_gb = [[float(unseen)]]
#X_test_gb = np.squeeze(X_test_gb)
#X_test_gb = X_test_gb.reshape(-1,1)
#result_alc_model2 = gb_alc.predict(X_test_gb)[0]
#result_drug_model2 = gb_drug.predict(X_test_gb)[0]

@st.cache_data
def delta_calc(x):

    if x == "lr":
        a1 = result_alc_model1
        b1 = result_drug_model1
        c1 = unseen_lr
        return a1, b1, c1
    else:
        a2 = result_alc_model2
        b2 = result_drug_model2
        c2 = unseen_gb
        return a2, b2, c2

#delta_alc_model1, delta_drug_model1, delta_alc_model2, delta_drug_model2, delta_unseen_lr, delta_unseen_gb= delta_calc()


st.write("Нажмите на кнопку, затем укажите сверху данные (количество безработных), которые хотите сравнивать.")
if st.button("Сравнить"):
    st.cache_data.clear()
    
# Вывод  

tab_model_1, tab_model_2 = st.tabs(["Линейная регрессия", "Градиентный бустинг"])

with tab_model_1:
    
    st.header("Настраиваемые данные")   
    # Данные введенные пользователем
    unseen_lr = st.slider("Количество безработных (в тыс. человек)", min_value = 20.0, max_value = 200.0, step = 0.1)
    decimal_lr = st.slider("Знаки после запятой", min_value = 0, max_value = 10, step = 1)
    # Прогноз
    X_test_lr = [[float(1.0)], [float(unseen_lr)]]
    X_test_lr = np.squeeze(X_test_lr)
    result_alc_model1 = lr_alc.predict(X_test_lr)[0]
    result_drug_model1 = lr_drug.predict(X_test_lr)[0]
    delta_alc_model1, delta_drug_model1, delta_unseen_lr = delta_calc('lr')
    # Данные введенные пользователем
    st.header("Метрика")    
    col1, col2, col3= st.columns(3)    

    if (result_alc_model1 > 0) and (result_drug_model1 > 0):
        col1.metric(label = "Количество алкоголиков", value = str(result_alc_model1)[:(len(str(int(result_alc_model1))) + decimal_lr + 1)], delta = str(result_alc_model1-delta_alc_model1)[:(len(str(int(result_alc_model1-delta_alc_model1))) + decimal_lr + 1)], delta_color = "inverse")
        col2.metric(label = "Количество наркоманов", value = str(result_drug_model1)[:(len(str(int(result_drug_model1))) + decimal_lr + 1)], delta = str(result_drug_model1-delta_drug_model1)[:(len(str(int(result_drug_model1-delta_drug_model1))) + decimal_lr + 1)], delta_color = "inverse")
        col3.metric(label = "Количество безработных", value = str(unseen_lr)[:(len(str(int(unseen_lr))) + decimal_lr + 1)], delta = str(unseen_lr-delta_unseen_lr)[:(len(str(int(unseen_lr-delta_unseen_lr))) + decimal_lr + 1)], delta_color = "inverse")
        source1_model1 = pd.DataFrame({
        'Прогноз': ['Безраб.', 'Алк.', 'Нарк.'],
        'Количество людей в тыс': [unseen_lr, result_alc_model1, result_drug_model1]})
        source2_model1 = pd.DataFrame({
        'Прогноз': ['Алк.', 'Нарк.'],
        'Количество людей в тыс': [result_alc_model1, result_drug_model1]})
    else:
        col1.metric(label = "Количество алкоголиков", value = 0, delta = str(result_alc_model1-delta_alc_model1)[:(len(str(int(result_alc_model1-delta_alc_model1))) + decimal_lr + 1)], delta_color = "inverse")
        col2.metric(label = "Количество наркоманов", value = 0, delta = str(result_drug_model1-delta_drug_model1)[:(len(str(int(result_drug_model1-delta_drug_model1))) + decimal_lr + 1)], delta_color = "inverse")
        col3.metric(label = "Количество безработных", value = str(unseen_lr)[:(len(str(int(unseen_lr))) + decimal_lr + 1)], delta = str(unseen_lr-delta_unseen_lr)[:(len(str(int(unseen_lr-delta_unseen_lr))) + decimal_lr + 1)], delta_color = "inverse")
        source1_model1 = pd.DataFrame({
        'Прогноз': ['Безраб.', 'Алк.', 'Нарк.'],
        'Количество людей в тыс': [unseen_lr, 0, 0]})
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
    
    st.header("Настраиваемые данные")   
    # Данные введенные пользователем
    unseen_gb = st.slider("Количество безработных (в тыс. человек)", min_value = 24.0, max_value = 200.0, step = 0.01)
    decimal_gb = st.slider("Знаки после запятой", min_value = 0, max_value = 12, step = 1)
    
    # Прогноз
    X_test_gb = [[float(unseen_gb)]]
    X_test_gb = np.squeeze(X_test_gb)
    X_test_gb = X_test_gb.reshape(-1,1)
    result_alc_model2 = gb_alc.predict(X_test_gb)[0]
    result_drug_model2 = gb_drug.predict(X_test_gb)[0]
    delta_alc_model2, delta_drug_model2, delta_unseen_gb= delta_calc('gb')
    st.header("Метрика")    
    col1, col2, col3= st.columns(3)    

    if (result_alc_model2 > 0) and (result_drug_model2 > 0):
        col1.metric(label = "Количество алкоголиков", value = str(result_alc_model2)[:(len(str(int(result_alc_model2))) + decimal_gb + 1)], delta = str(result_alc_model2-delta_alc_model2)[:(len(str(int(result_alc_model2-delta_alc_model2))) + decimal_gb + 1)], delta_color = "inverse")
        col2.metric(label = "Количество наркоманов", value = str(result_drug_model2)[:(len(str(int(result_drug_model2))) + decimal_gb + 1)], delta = str(result_drug_model2-delta_drug_model2)[:(len(str(int(result_drug_model2-delta_drug_model2))) + decimal_gb + 1)], delta_color = "inverse")
        col3.metric(label = "Количество безработных", value = str(unseen_gb)[:(len(str(int(unseen_gb))) + decimal_gb + 1)], delta = str(unseen_gb-delta_unseen_gb)[:(len(str(int(unseen-delta_unseen_gb))) + decimal_gb + 1)], delta_color = "inverse")
        source1_model2 = pd.DataFrame({
        'Прогноз': ['Безраб.', 'Алк.', 'Нарк.'],
        'Количество людей в тыс': [unseen_gb, result_alc_model2, result_drug_model2]})
        source2_model2 = pd.DataFrame({
        'Прогноз': ['Алк.', 'Нарк.'],
        'Количество людей в тыс': [result_alc_model2, result_drug_model2]})
    else:
        col1.metric(label = "Количество алкоголиков", value = 0, delta = str(result_alc_model2-delta_alc_model2)[:(len(str(int(result_alc_model2-delta_alc_model2))) + decimal_gb + 1)], delta_color = "inverse")
        col2.metric(label = "Количество наркоманов", value = 0, delta = str(result_drug_model2-delta_drug_model2)[:(len(str(int(result_drug_model2-delta_drug_model2))) + decimal_gb + 1)], delta_color = "inverse")
        col3.metric(label = "Количество безработных", value = str(unseen_gb)[:(len(str(int(unseen_gb))) + decimal_gb + 1)], delta = str(unseen_gb-delta_unseen_gb)[:(len(str(int(unseen_gb-delta_unseen_gb))) + decimal_gb + 1)], delta_color = "inverse")
        source1_model2 = pd.DataFrame({
        'Прогноз': ['Безраб.', 'Алк.', 'Нарк.'],
        'Количество людей в тыс': [unseen_gb, 0, 0]})
        source2_model2 = pd.DataFrame({
        'Прогноз': ['Алк.', 'Нарк.'],
        'Количество людей в тыс': [0, 0]})

    st.header("Столбчатая диаграмма")         
    tab_diagram_1, tab_diagram_2 = st.tabs(["Алк/Нарк", "Алк/Безраб/Нарк"])
    with tab_diagram_1:
        st.altair_chart(alt.Chart(pd.DataFrame(source2_model2)).mark_bar().encode(x = 'Прогноз', y = 'Количество людей в тыс'), use_container_width = True)
    with tab_diagram_2:
        st.altair_chart(alt.Chart(pd.DataFrame(source1_model2)).mark_bar().encode(x = 'Прогноз', y = 'Количество людей в тыс'), use_container_width = True)

st.header("Почему это важно")    
st.write("<p style='text-align: justify;'><span>Прогнозирование количества людей с алкогольной и наркотической зависимостью от количества безработных имеет большое значение для разработки эффективных социальных программ и мер для борьбы с наркотиками и алкогольной зависимостью.</span></p>", unsafe_allow_html=True)
st.write("<p style='text-align: justify;'><span>Безработные люди имеют повышенный риск развития алкогольной и наркотической зависимости, так как они часто сталкиваются с социальным и психологическим стрессом, чувством безнадёжности и неуверенности в будущем.</span></p>", unsafe_allow_html=True)
st.write("<p style='text-align: justify;'><span>Учитывая все вышеперечисленные факторы, прогнозирование количества людей с алкогольной и наркотической зависимостью от количества безработных позволяет руководителям и специалистам в области здравоохранения и социальной защиты разработать целенаправленные программы и меры для профилактики и лечения этих проблем. Это также может помочь определить необходимость расширения и усиления социальной поддержки и проведения образовательных программ для безработных людей.</span></p>", unsafe_allow_html=True)
st.image(image)
st.info('Круглосуточная горячая линия по вопросам алкоголизма и наркомании: 8 800 551-70-14', icon="ℹ️")

