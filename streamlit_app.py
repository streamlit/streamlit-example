from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pickle
import numpy as np
import plotly.express as px

# Загрузка моделей
with open('new_model.pkl', 'rb') as model_pkl:
    lr = pd.read_pickle(model_pkl)

# Данные введенные пользователем
unseen = st.slider("Количество безработных (в тыс. человек)", min_value = 0.0, max_value = 200.0, step = 0.1)
decimal = st.slider("Знаки после запятой", min_value = 0, max_value = 10, step = 1)
X_test_sm = [[float(1.0)], [float(unseen)]]
X_test_sm = np.squeeze(X_test_sm)

# Прогноз
result = lr.predict(X_test_sm)[0]

st.write(f'Количество алкоголиков: {str(result)[:(len(str(int(result)+decimal)]} (в тыс. человек)')

source = pd.DataFrame({
    'a': ['Алкаши', 'Наркоши'],
    'b': [result, 13]
})

st.altair_chart(alt.Chart(pd.DataFrame(source), height = 500, width = 500)
                .mark_bar()
                .encode(x='a', y='b'))


# Display the result
#if result < 0:
#    st.write(f'При количестве безработных в {float(unseen)} тыс. человек, алкоголиков не будет')
#else:
#    st.write(f'При количестве безработных в {float(unseen)} тыс. человек, количество алкоголиков будет составлять {result} тыс. человек')


