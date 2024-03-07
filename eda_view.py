import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import plotly.express as px



def run():  

    set_page_layout('80%', 'center')


    #df = pd.read_excel('/Users/carlotapersonal/Library/CloudStorage/OneDrive-UFV/CURSO_5/PFG/Code/proyecto-fin-de-grado-2024-2-carlotagomezr/data-analysis/eda/dataset_post_EDA.xlsx')
    df = pd.read_excel('/Users/carlotro/Desktop/Escritorio/Personal-Carlota/UFV/PFG/APP-REPO/dataset_post_EDA.xlsx')
    print(df.columns.tolist())
    
    # 1) TITULO -----------------------------------------------------------------------------------
    st.title('Gestión de incidencias - EDA')

    total_incidencias = df['task_id'].nunique()  # Mostrar el número total de incidencias
    st.write(f'Número total de incidencias: {total_incidencias}')


    # 2) GRAFICO DE BARRAS, ANALISIS TEMPORAL ---------------------------------------------------------------------------------
    df['end_time'] = pd.to_datetime(df['end_time'])  
    df.set_index('end_time', inplace=True) 
    variable = st.selectbox('Seleccione la variable para agrupar:', ['priority', 'has_breached', 'assignment_group', 'company', 'contact_type','impact'])

    # Agrupar por la variable seleccionada y resample por mes
    grouped = df.groupby(variable).resample('M')['task_id'].nunique().reset_index()

    # Crear un gráfico de barras apilado con colores basados en la variable seleccionada
    fig = px.bar(grouped, x='end_time', y='task_id', color=variable, title='Número de incidencias por mes', 
                 labels={'task_id':'Número de incidencias'}, height=400)
    fig.update_layout(barmode='stack')
    fig.update_xaxes(title_text='Mes y año de finalización')
    st.plotly_chart(fig)

  


    # 3) GRAFICO DE BARRAS CON PRIORITY VS TIME_WORKED ---------------------------------------------------------------------------
    fig2 = px.bar(df, x='time_worked', y='priority', color=variable)
    fig2.update_layout(
        title='Relación entre la prioridad y el tiempo trabajado',
        xaxis_title='Tiempo trabajado',
        yaxis_title='Prioridad'
    )
    st.plotly_chart(fig2)
    
    # 4) TABLA FORMAS DE CONTACTO -------------------------------------------------------------------------------------------
    var_select = st.selectbox('Seleccione la variable para agrupar:', ['assignment_group', 'company', 'priority'])
    fig3 = px.bar(df, x=var_select, y='task_id', color='contact_type', labels={'task_id':'Número de incidencias'})
    fig3.update_layout(
        title= f'{var_select} vs tipo de contacto',
        xaxis_title=var_select,
        yaxis_title='Número de incidencias'
    )
    ax = plt.gca()  # get current axes
    ax.set_yticklabels([]) 
    fig3.update_layout(barmode='stack')
    st.plotly_chart(fig3)


    # 5) TABLA SUMMARY BY GROUP, COMPANY AND USER TYPE ---------------------------------------------------------------------------
    variable_select = st.selectbox('Seleccione la variable para agrupar:', ['assignment_group', 'company', 'contact_type'])
   
    priority_counts = df.groupby([variable_select, 'priority']).size().reset_index(name='counts')
    total_counts = df.groupby(variable_select).size()
    priority_counts['percentage'] = priority_counts.apply(lambda row: (row['counts'] / total_counts[row[variable_select]]) * 100, axis=1)
    priority_counts['percentage'] = priority_counts['percentage'].round(2)
    priority_counts['percentage'] = priority_counts['percentage'].astype(str) + '%' 
    pivot_table = priority_counts.pivot(index=variable_select, columns='priority', values='percentage')
    #pivot_columns = pivot_table.columns.tolist()

    print(pivot_table)
    column_names = [variable_select, '% de incidencias', 'Media business duration', 
                    '% incumplimiento SLA', 'Critical', 'High', 'Moderate', 'Low','Planning'] #+ pivot_columns    

    # column_names = pd.MultiIndex.from_tuples([(None, variable_select),
    #                                         (None,'% de incidencias'),
    #                                         (None, 'Media business duration'),
    #                                         (None, '% infracción SLA'),
    #                                         ('Priority', 'Critical'), ('Priority', 'High'), 
    #                                         ('Priority', 'Moderate'), ('Priority', 'Low'), ('Priority', 'Planning')])


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
    grouped_table['% incumplimiento SLA'] = grouped_table['% incumplimiento SLA'].apply(add_warning_icon)
    grouped_table = grouped_table.fillna('0%') # if  'Critical', 'High', 'Moderate', 'Low','Planning' == nana -> 0%

    # apply styles
    grouped_table = grouped_table.style.applymap(color_cell_priority).set_properties(**{'text-align': 'center'}).set_table_styles([dict(selector='th', props=[('background', '#54B4CE'), ('color', 'white')])])
    st.table(grouped_table)


    
    
    
    # 6) GRAFICO RELACION ---------------------------------------------------------------------------------
    # quiero hacer un grafico --> Reassignment Count, 24_7, and Contact Type'
    # plt.figure(figsize=(10, 6))
    # sns.scatterplot(x='reassignment_count', y='u_24_7', hue='contact_type', data=df)
    # plt.title('Relationship between Reassignment Count, Resolution Time, and Contact Type')
    # plt.show()



   
  

    
# FUNCIONES ---------------------------------------------------------------------------------

def add_warning_icon(val):
    if isinstance(val, str) and val.endswith('%'):
        percentage = float(val.rstrip('%'))
        if percentage > 10:
            return f'{val} ⚠️'
    return val

def color_cell_priority(val):
    priority = ['Critical', 'High', 'Moderate', 'Low', 'Planning']
    if isinstance(val, str):
        if val in priority:
            percentage = float(val.rstrip('%'))
            if percentage > 50:
                return 'background-color: yellow'
    return ''

def set_page_layout(page_width='70%', page_align='center'):
    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container{{
                max-width: {page_width};
                padding-top: 1rem;
                padding-right: 1rem;
                padding-left: 1rem;
                margin-{page_align}-auto;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
