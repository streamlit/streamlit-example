import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import plotly.express as px

def run():  
    df = pd.read_excel('/Users/carlotapersonal/Library/CloudStorage/OneDrive-UFV/CURSO_5/PFG/Code/proyecto-fin-de-grado-2024-2-carlotagomezr/data-analysis/eda/dataset_post_EDA.xlsx')

    # TITULO -----------------------------------------------------------------------------------
    st.title('Gestión de incidencias - EDA')
    # Mostrar el número total de incidencias
    total_incidencias = df['task_id'].nunique()  
    st.write(f'Número total de incidencias: {total_incidencias}')

    # GRAFICO DE BARRAS, ANALISIS TEMPORAL ---------------------------------------------------------------------------------
    df['end_time'] = pd.to_datetime(df['end_time'])  
    df.set_index('end_time', inplace=True) 
    variable = st.selectbox('Seleccione la variable para agrupar:', ['priority', 'has_breached', 'assignment_group', 'company', 'contact_type'])

    # Agrupar por la variable seleccionada y resample por mes
    grouped = df.groupby(variable).resample('M')['task_id'].nunique().reset_index()

    # Crear un gráfico de barras apilado con colores basados en la variable seleccionada
    fig = px.bar(grouped, x='end_time', y='task_id', color=variable, title='Número de incidencias por mes', labels={'task_id':'Número de incidencias'}, height=400)
    fig.update_layout(barmode='stack')
    fig.update_xaxes(title_text='Mes y año de finalización')
    st.plotly_chart(fig)


    # GRAFICO DE BARRAS CON PRIORITY VS TIME_WORKED ---------------------------------------------------------------------------
    fig2 = px.bar(x='time_worked', y='priority', color=variable)
    fig2.set_title('Relación entre la prioridad y el tiempo trabajado')
    fig2.set_ylabel('Prioridad')
    fig2.set_xlabel('Tiempo trabajado')
    st.pyplot(fig2)