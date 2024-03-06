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
    fig2 = px.bar(df, x='time_worked', y='priority', color=variable)
    fig2.update_layout(
        title='Relación entre la prioridad y el tiempo trabajado',
        xaxis_title='Tiempo trabajado',
        yaxis_title='Prioridad'
    )
    st.plotly_chart(fig2)

    # TABLA SUMMARY BY GROUP, COMPANY AND USER TYPE ---------------------------------------------------------------------------
    variable_select = st.selectbox('Seleccione la variable para agrupar:', ['assignment_group', 'company', 'contact_type'])
   
    priority_counts = df.groupby([variable_select, 'priority']).size().reset_index(name='counts')
    total_counts = df.groupby(variable_select).size()
    priority_counts['percentage'] = priority_counts.apply(lambda row: (row['counts'] / total_counts[row[variable_select]]) * 100, axis=1)
    priority_counts['percentage'] = priority_counts['percentage'].round(2)
    priority_counts['percentage'] = priority_counts['percentage'].astype(str) + '%' 
    pivot_table = priority_counts.pivot(index=variable_select, columns='priority', values='percentage')
    pivot_columns = pivot_table.columns.tolist()

    print(pivot_table)
    column_names = [variable_select, '% de incidencias', 'Media business duration', 
                    '% de incumplimiento SLA', 'Critical', 'High', 'Moderate', 'Low','Planning'] #+ pivot_columns    

    # tabla para representar la info
    grouped_table = df.groupby(variable_select).agg({'task_id': lambda x: x.count() / df['task_id'].count() * 100,
                                                    'business_duration': 'mean',
                                                    'has_breached': lambda x: x.sum() / x.count() * 100})
    grouped_table = pd.merge(grouped_table, pivot_table, on=variable_select, how='left')
   
    # has_brached = yes -> % de incidencias que han incumplido el SLA
    grouped_table['task_id'] = grouped_table['task_id'].round(2)
    grouped_table['task_id']  = grouped_table['task_id'].astype(str) + '%'
    grouped_table['business_duration'] = grouped_table['business_duration'].round(0).astype(int)
    grouped_table['has_breached'] = grouped_table['has_breached'].round(2)
    grouped_table['has_breached'] = grouped_table['has_breached'].astype(str) + '%' # ponerlo en modo de barra si se puede

    


    grouped_table = grouped_table.reset_index()
    grouped_table.columns = column_names

    grouped_table.set_index(variable_select, inplace=True)
    grouped_table['% de incumplimiento SLA'] = grouped_table['% de incumplimiento SLA'].apply(add_warning_icon)
   
    
    grouped_table = grouped_table.style.set_properties(**{'text-align': 'center'}).set_table_styles([dict(selector='th',
                                                                                                           props=[('background', '#54B4CE'), 
                                                                                                                  ('color', 'white')])])
    st.table(grouped_table)

   
  

    


def add_warning_icon(val):
    if isinstance(val, str) and val.endswith('%'):
        percentage = float(val.rstrip('%'))
        if percentage > 10:
            return f'{val} ⚠️'
    return val

