import random

import numpy
import streamlit as st
import pandas as pd
import pickle
import json
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import openai
import re
from matplotlib.patches import Patch
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


def main():
    global all_features
    st.write("Модель 'Mega-Z 1.0'")
    st.image("intro.png")  # Add the path to your image file here

    # Add the author picture
    author_image = "photo_5269480532511674295_y.jpg"  # Add the path to your author picture file here
    st.sidebar.text("Сделано Ильей Осиповым")
    st.sidebar.image(author_image, use_column_width=True)

    st.sidebar.header("Пользовательский ввод")
    st.sidebar.write("### Загрузите Excel файл")
    test_size = st.sidebar.slider("Выборка вопросов для модели", 0.1, 0.5, 0.2, 0.1)
    degree = st.sidebar.slider(
        "Максимальная степень полиномиальных признаков", 1, 5, 4, 1
    )
    uploaded_file = st.sidebar.file_uploader("Выберите Excel файл", type=["xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        # Convert datetime column to datetime data type

        df["Отметка времени"] = pd.to_datetime(df["Отметка времени"])

        df_cluster1 = df[
            [
                "История",
                "Психология",
                "Математика и/или физика",
                "Интернет и социальные сети",
            ]
        ]
        cluster1_pairs = []  # Список для хранения пар вопросов и булевых значений

        # Итерация по вопросам в кластере df_cluster1
        for column in df_cluster1.columns:
            question = column
            boolean_value = True

            # Создание пары вопроса и булевого значения
            pair = (question, boolean_value)

            # Добавление пары в список
            cluster1_pairs.append(pair)

        for pair in cluster1_pairs:
            print(pair)

        df_cluster2 = df[
            [
                "Химия",
                "Экономика и менеджмент",
                "Биология",
                "Иностранные языки",
                "Медицина",
                "Технические и инженерные дисциплины (уроки)",
                "Социально-экономические и гуманитарные дисциплины (уроки)",
            ]
        ]

        cluster2_pairs = []  # Список для хранения пар вопросов и булевых значений
        # Итерация по вопросам в кластере df_cluster2
        for column in df_cluster2.columns:
            question = column
            boolean_value = True

            # Создание пары вопроса и булевого значения
            pair = (question, boolean_value)

            # Добавление пары в список
            cluster2_pairs.append(pair)

        # Вывод списка пар вопросов и булевых значений для кластера df_cluster2
        for pair in cluster2_pairs:
            print(pair)

        df_cluster3 = df[["Написание стихов и рассказов"]]

        cluster3_pairs = []  # Список для хранения пар вопросов и булевых значений

        # Итерация по вопросам в кластере df_cluster3
        for column in df_cluster3.columns:
            question = column
            boolean_value = True

            # Создание пары вопроса и булевого значения
            pair = (question, boolean_value)

            # Добавление пары в список
            cluster3_pairs.append(pair)

        # Вывод списка пар вопросов и булеввых значений для кластера df_cluster3
        for pair in cluster3_pairs:
            print(pair)

        # Повторите аналогичные шаги для остальных кластеров (df_cluster4, df_cluster5, df_cluster6, df_cluster7)...

        df_cluster4 = df[
            [
                "Престижность места учёбы (школы, колледжа, университета)",
                "Учиться в другом российском городе",
                "Учиться за рубежом",
                "Учёба на «отлично»",
                "Изучить дополнительный иностранный язык",
                "Изучить языки программирования",
                "Представлять школу/колледж/университет на конкурсах, спортивных соревнованиях, олимпиадах",
            ]
        ]

        cluster4_pairs = []  # Список для хранения пар вопросов и булевых значений
        # Итерация по вопросам в кластере df_cluster4
        for column in df_cluster4.columns:
            question = column
            boolean_value = True

            # Создание пары вопроса и булевого значения
            pair = (question, boolean_value)

            # Добавление пары в список
            cluster4_pairs.append(pair)

        # Вывод списка пар вопросов и булевых значений для кластера df_cluster4
        for pair in cluster4_pairs:
            print(pair)

        # Продолжите аналогичные шаги для остальных кластеров (df_cluster5, df_cluster6, df_cluster7)...

        df_cluster5 = df[
            [
                "Мой город комфортный для проживания",
                "Мой город безопасный",
                "Мой город экологически чистый",
                "В моём городе живут самые красивые люди",
                "Мне легко налаживать контакт с жителями нашего города",
            ]
        ]

        cluster5_pairs = []  # Список для хранения пар вопросов и булевых значений
        # Итерация по вопросам в кластере df_cluster4
        for column in df_cluster5.columns:
            question = column
            boolean_value = True

            # Создание пары вопроса и булевого значения
            pair = (question, boolean_value)

            # Добавление пары в список
            cluster5_pairs.append(pair)

        # Вывод списка пар вопросов и булевых значений для кластера df_cluster4
        for pair in cluster5_pairs:
            print(pair)

        df_cluster6 = df[
            [
                "Я бы хотел работать в своём городе",
                "В моём городе много безработных",
                "В моём городе много учебных заведений",
                "Мой город создаёт возможности для моего развития и творчества",
            ]
        ]

        cluster6_pairs = []  # Список для хранения пар вопросов и булевых значений
        # Итерация по вопросам в кластере df_cluster4
        for column in df_cluster6.columns:
            question = column
            boolean_value = True

            # Создание пары вопроса и булевого значения
            pair = (question, boolean_value)

            # Добавление пары в список
            cluster6_pairs.append(pair)

        # Вывод списка пар вопросов и булевых значений для кластера df_cluster4
        for pair in cluster6_pairs:
            print(pair)

        df_cluster7 = df[
            [
                "В моём городе много исторических достопримечательностей",
                "Мой город – это высокоразвитая культура его жителей",
                "В моём городе большие пробки",
                "В моём городе достаточно культурных центров, музеев, театров, кинотеатров",
                "Я с гордостью осознаю, что живу в своём городе",
            ]
        ]

        cluster7_pairs = []  # Список для хранения пар вопросов и булевых значений
        # Итерация по вопросам в кластере df_cluster4
        for column in df_cluster7.columns:
            question = column
            boolean_value = True

            # Создание пары вопроса и булевого значения
            pair = (question, boolean_value)

            # Добавление пары в список
            cluster7_pairs.append(pair)

        # Вывод списка пар вопросов и булевых значений для кластера df_cluster4
        for pair in cluster7_pairs:
            print(pair)

        df_cluster8 = df[
            [
                "Много зарабатывать",
                "Работать не по специальности",
                "Заниматься бизнесом",
                "Работать на государственной службе",
                "Заниматься волонтерством",
                "Аспирантура и учёная степень",
                "Приносить пользу обществу",
                "Работать в СМИ",
            ]
        ]

        cluster8_pairs = []  # Список для хранения пар вопросов и булевых значений

        # Итерация по вопросам в кластере df_cluster6
        for column in df_cluster8.columns:
            question = column
            boolean_value = True

            # Создание пары вопроса и булевого значения
            pair = (question, boolean_value)

            # Добавление пары в список
            cluster8_pairs.append(pair)

        # Вывод списка пар вопросов и булевых значений для кластера df_cluster6
        for pair in cluster8_pairs:
            print(pair)

        df_cluster9 = df[
            [
                "У меня в городе есть что посмотреть даже бывалым туристам и путешественникам",
                "Я периодически устаю от своего города и хочется сменить обстановку",
                "Я не рассматриваю вариантов переехать из моего города",
            ]
        ]

        cluster9_pairs = []  # Список для хранения пар вопросов и булевых значений

        # Итерация по вопросам в кластере df_cluster7
        for column in df_cluster9.columns:
            question = column
            boolean_value = True

            # Создание пары вопроса и булевого значения
            pair = (question, boolean_value)

            # Добавление пары в список
            cluster9_pairs.append(pair)

        # Вывод списка пар вопросов и булевых значений для кластера df_cluster7
        for pair in cluster9_pairs:
            print(pair)

        cluster1_pairs = [
            ("История", True),
            ("Психология", True),
            ("Математика и/или физика", True),
            ("Интернет и социальные сети", True),
        ]
        cluster2_pairs = [
            ("Химия", True),
            ("Экономика и менеджмент", True),
            ("Биология", True),
            ("Иностранные языки", True),
            ("Медицина", True),
            ("Технические и инженерные дисциплины (уроки)", True),
            ("Социально-экономические и гуманитарные дисциплины (уроки)", True),
        ]
        cluster3_pairs = [("Написание стихов и рассказов", True)]
        cluster4_pairs = [
            ("Престижность места учёбы (школы, колледжа, университета)", True),
            ("Учиться в другом российском городе", False),
            ("Учиться за рубежом", False),
            ("Учёба на «отлично»", True),
            ("Изучить дополнительный иностранный язык", True),
            ("Изучить языки программирования", True),
            (
                "Представлять школу/колледж/университет на конкурсах, спортивных соревнованиях, олимпиадах",
                True,
            ),
        ]
        # Создание массивов пар для df_cluster5
        cluster5_pairs = [
            ("Мой город комфортный для проживания", True),
            ("Мой город безопасный", True),
            ("Мой город экологически чистый", True),
            ("В моём городе живут самые красивые люди", True),
            ("Мне легко налаживать контакт с жителями нашего города", True),
        ]

        # Создание массивов пар для df_cluster6
        cluster6_pairs = [
            ("Я бы хотел работать в своём городе", True),
            ("В моём городе много безработных", False),
            ("В моём городе много учебных заведений", True),
            ("Мой город создаёт возможности для моего развития и творчества", True),
        ]

        # Создание массивов пар для df_cluster7
        cluster7_pairs = [
            ("В моём городе много исторических достопримечательностей", True),
            ("Мой город – это высокоразвитая культура его жителей", True),
            ("В моём городе большие пробки", False),
            (
                "В моём городе достаточно культурных центров, музеев, театров, кинотеатров",
                True,
            ),
            ("Я с гордостью осознаю, что живу в своём городе", True),
        ]
        cluster8_pairs = [
            ("Много зарабатывать", True),
            ("Работать не по специальности", True),
            ("Заниматься бизнесом", True),
            ("Работать на государственной службе", True),
            ("Заниматься волонтерством", True),
            ("Аспирантура и учёная степень", True),
            ("Приносить пользу обществу", True),
            ("Работать в СМИ", True),
        ]
        cluster9_pairs = [
            (
                "У меня в городе есть что посмотреть даже бывалым туристам и путешественникам",
                True,
            ),
            (
                "Я периодически устаю от своего города и хочется сменить обстановку",
                False,
            ),
            ("Я не рассматриваю вариантов переехать из моего города", True),
        ]

        all_clusters_pairs = [
            cluster1_pairs,
            cluster2_pairs,
            cluster3_pairs,
            cluster4_pairs,
            cluster5_pairs,
            cluster6_pairs,
            cluster7_pairs,
            cluster8_pairs,
            cluster9_pairs,
        ]
        if st.button("Удалить выступающие усы"):
            for clusters_pairs in all_clusters_pairs:
                questions, boolean_values = zip(*clusters_pairs)
                data = df[list(questions)]

                # Create a boxplot using Matplotlib
                fig, ax = plt.subplots()
                data.boxplot(ax=ax)
                plt.xticks(rotation=90)

                # Display the boxplot in Streamlit
                st.pyplot(fig)
                st.write("Гистограммы после удаления усов")

                # Calculate the quartiles and IQR
                Q1 = data.quantile(0.25)
                Q3 = data.quantile(0.75)
                IQR = Q3 - Q1

                # Define the lower and upper bounds for outlier detection
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                # Remove outliers from the dataset
                data = data.mask((data < lower_bound) | (data > upper_bound))

                # Forward fill missing values caused by removing outliers
                data = data.ffill().bfill()

                # Display the cleaned boxplot in Streamlit
                fig_cleaned, ax_cleaned = plt.subplots()
                data.boxplot(ax=ax_cleaned)
                plt.xticks(rotation=90)
                st.pyplot(fig_cleaned)
        all_features = []
        # Определение вопросов и булевых значений
        threshold = st.slider("Threshold", min_value=0.0, max_value=1.0, step=0.01)
        if st.button("Показать важность фичей:"):

            questions = [
                "Я подумываю переехать из моего города, когда это станет возможным",
                "Я не рассматриваю вариантов переехать из моего города",
            ]
            boolean_values = [False, True]

            # Фильтрация данных по условию, когда оба ответа выше 3 или ниже 3
            condition_data = df[
                (df[questions[0]] > 3) & (df[questions[1]] > 3)
                | (df[questions[0]] < 3) & (df[questions[1]] < 3)
            ]

            # Подсчет сочетаний ответов
            count_satisfy_condition = len(condition_data)

            # Подсчет количества тех, кто хочет уехать, не хочет уехать и сомневается
            count_want_to_leave = len(df[df[questions[0]] > 3])
            count_dont_want_to_leave = len(df[df[questions[1]] < 3])

            print(count_want_to_leave)
            print(count_dont_want_to_leave)
            print(count_satisfy_condition)

            # Построение круговой диаграммы
            labels = ["Хочет уехать", "Не хочет уехать", "Сомневается"]
            sizes = [
                count_want_to_leave,
                count_dont_want_to_leave,
                count_satisfy_condition,
            ]
            print(sizes)
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct="%1.1f%%")
            ax.axis("equal")
            st.pyplot(fig.figure)

            # Определение вопросов и булевых значений
            questions = [
                "Я подумываю переехать из моего города, когда это станет возможным",
                "Я не рассматриваю вариантов переехать из моего города",
            ]

            df["target"] = df[questions].apply(
                lambda x: 1 if x[0] > 3 and x[1] > 3 or x[0] < 3 and x[1] < 3 else 0,
                axis=1,
            )

            # Создание списка кластеров
            clusters = [
                df_cluster1,
                df_cluster2,
                df_cluster3,
                df_cluster4,
                df_cluster5,
                df_cluster6,
                df_cluster7,
                df_cluster8,
                df_cluster9,
            ]

            for i, X in enumerate(clusters):
                st.write(f"Гистограмма для кластера {i + 1}")
                y = df["target"]

                # Разделение данных на тренировочный и тестовый наборы
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, random_state=42
                )

                # Создание полиномиальных признаков
                polynomial_features = PolynomialFeatures(degree=degree)
                X_train_poly = polynomial_features.fit_transform(X_train)
                X_test_poly = polynomial_features.transform(X_test)

                # Создание и обучение модели
                model = LinearRegression()
                model.fit(X_train_poly, y_train)

                # Получение предсказаний модели на тестовых данных
                y_pred = model.predict(X_test_poly)

                # Оценка модели
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                # Округление значений
                mse_rounded = round(mse, 2)
                r2_rounded = round(r2, 2)
                # Вывод результатов
                st.write("Среднеквадратичная ошибка:", mse_rounded)
                st.write("Коэффициент детерминации:", r2_rounded)
                print("средняя ошибка")
                print(f"{mse_rounded}\n")
                print("Коэффициент детерминации:")
                print(f"{r2_rounded}\n")

                coefficients = model.coef_
                feature_names = polynomial_features.get_feature_names_out(X.columns)
                feature_importances = {
                    name: abs(coef)
                    for name, coef in zip(feature_names[1:], coefficients[1:])
                }

                # Создание гистограммы важности фичей с разными цветами для каждого вопроса
                fig, ax = plt.subplots(figsize=(20, 8))
                x_values = list(feature_importances.values())
                y_labels = list(feature_importances.keys())
                colors = ["blue", "green"]  # Цвета для каждого вопроса

                ax.barh(y_labels, x_values, color=colors, align="center")
                ax.set_xlabel("Важность", fontsize=12)  # Увеличение размера шрифта
                ax.set_ylabel("Фичи", fontsize=12)  # Увеличение размера шрифта
                ax.set_title(
                    "Важность фичей в предсказании о переезде", fontsize=12
                )  # Увеличение размера шрифта

                # Добавление ярлыков на график
                for t, v in enumerate(x_values):
                    ax.text(
                        v, t, str(round(v, 2)), color="black", va="center", fontsize=12
                    )  # Увеличение размера шрифта

                # Добавление подписей к цветам
                legend_elements = [
                    Patch(
                        facecolor="blue", edgecolor="black", label="Переезд возможен"
                    ),
                    Patch(
                        facecolor="green",
                        edgecolor="black",
                        label="Не рассматриваю переезд",
                    ),
                ]
                ax.legend(
                    handles=legend_elements, loc="lower right", fontsize=12
                )  # Увеличение размера шрифта

                # Рекомендации для кластера
                # print("важность фичей\n")
                # print(feature_importances)
                sorted_importances = sorted(
                    feature_importances.items(), key=lambda x: x[1], reverse=True
                )
                # print("важность с сортировкой фичей\n")
                # print(sorted_importances)
                all_features.append(sorted_importances)
                # Set the initial threshold value

                # Вывод важности фичей с сортировкой
                sorted_features = sorted(
                    feature_importances.items(), key=lambda x: x[1], reverse=True
                )
                influential_questions = []

                for feature, importance in sorted_features:
                    if importance > threshold:
                        feature_question = feature  # Фича является названием вопроса
                        influential_questions.append(feature_question)

                if influential_questions:
                    st.pyplot(fig)
                    st.write("Список влияющих вопросов:")
                    for question in influential_questions:
                        st.write(question)
                else:
                    st.write("Нет влияющих вопросов.")

                st.write("---")

                # print("важность с сортировкой фичей все\n")
                # print(all_features)


if __name__ == "__main__":
    main()
