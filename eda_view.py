import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



def run(df):  
    col = st.columns((4,4), gap='medium')

    # Primera fila con una sola columna
    row1 = st.container()

    # Segunda fila con dos columnas
    col1, col2 = st.columns(2)

    # Tercera fila con dos columnas
    col3, col4 = st.columns(2)

    # Cuarta fila con una sola columna
    row2 = st.container()

    # Ahora puedes usar row1, col1, col2, col3, col4, y row2 para agregar contenido a tu dashboard
    # Por ejemplo:
    row1.header("Este es el encabezado de la primera fila")
    col1.write("Este es el contenido de la segunda fila, primera columna")
    col2.write("Este es el contenido de la segunda fila, segunda columna")
    col3.write("Este es el contenido de la tercera fila, primera columna")
    col4.write("Este es el contenido de la tercera fila, segunda columna")
    row2.header("Este es el encabezado de la cuarta fila")


    st.title('Gestión de incidencias - Overview')

    total_incidencias = df['task_id'].nunique()  # Mostrar el número total de incidencias
    st.write(f'Número total de incidencias: {total_incidencias}')

    # Insertar graficos
    variable = st.selectbox('Seleccione la variable para agrupar:', ['priority', 'has_breached', 'assignment_group', 'company', 'contact_type','impact'])

    incidencias_timeline(df, variable) # grafico de barras, analisis temporal
    tiempo_trabajado(df, variable) # priority vs time worked
    
    # contact_type(df)
    # pie_charts(df)
    # tabla(df) # summary table
    # pie_chart_menos_24h(df)
    # pie_chart_mas_24h(df)
    # pie_chart_reasigned(df)
    # pie_chart_not_reasigned(df)
    
    
    
# FUNCIONES GRAFICOS ---------------------------------------------------------------------------------
def incidencias_timeline(df, variable):
    df['end_time'] = pd.to_datetime(df['end_time'])  
    df.set_index('end_time', inplace=True) 
    
    grouped = df.groupby(variable).resample('M')['task_id'].nunique().reset_index()

    # Crear un gráfico de barras apilado con colores basados en la variable seleccionada
    incidencias_timeline_fig = px.bar(grouped, x='end_time', y='task_id', color=variable, title='Número de incidencias por mes', 
                 labels={'task_id':'Número de incidencias'}, height=400)
    incidencias_timeline_fig.update_layout(barmode='stack')
    incidencias_timeline_fig.update_xaxes(title_text='Mes y año de finalización')
    st.plotly_chart(incidencias_timeline_fig)
    return incidencias_timeline_fig

def tiempo_trabajado(df, variable):
    tiempo_trabajado_fig = px.bar(df, y='time_worked', x='priority', color=variable)
    tiempo_trabajado_fig.update_layout(
        title='Relación entre la prioridad y el tiempo trabajado',
        yaxis_title='Tiempo trabajado',
        xaxis_title='Prioridad'
    )
    #st.plotly_chart(tiempo_trabajado_fig)   
    return tiempo_trabajado_fig 

def tabla(df):
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

def contact_type(df):
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

def pie_charts(df):
    selection_variable = st.selectbox('Seleccione la variable para agrupar:', ['reassingment_count_bool','u_24_7'])
    contact_types = df['contact_type'].unique()
    
    fig6 = make_subplots(rows=1, cols=len(contact_types), subplot_titles=contact_types, specs=[[{'type':'domain'}]*len(contact_types)])

    for i, contact_type in enumerate(contact_types):
        data = df[df['contact_type'] == contact_type][selection_variable].value_counts()
        fig6.add_trace(go.Pie(labels=data.index, values=data, name=contact_type), 1, i+1)

    fig6.update_layout(height=600, width=900, title_text=f'Tipo de contacto vs {selection_variable}',
                       legend_title_text=f'{selection_variable}', title_x=0.5, title_y=0.95)
    st.plotly_chart(fig6)

def pie_chart_menos_24h(df):
    
    df['less_24h'] = df['u_24_7'].apply(lambda x: 1 if x == True else 0) # 1 si ha sido resuelta en menos de 24h

    # guardar en una variable el % de incidencias que han sido resueltas en menos de 24h
    porcentaje_less = df['less_24h'].sum() / df['less_24h'].count() * 100
    
    df_filtered = df[df['less_24h'] == 1] # solo aquellas incidencias que han sido resueltas en menos de 24h 

    # un único pie chart coloreado por tipo de contacto, indicando el % de incidencias que han sido resueltas en menos de 24h
    pie = px.pie(df_filtered, names='contact_type', title=f'Incidencias resueltas en menos de 24h - {porcentaje_less:.2f}%', 
                 labels={'contact_type':'Tipo de contacto'}, height=400)

    st.plotly_chart(pie)

def pie_chart_mas_24h(df):
    
    df['more_24h'] = df['u_24_7'].apply(lambda x: 1 if x == False else 0) # 1 si ha sido resuelta en menos de 24h

    # guardar en una variable el % de incidencias que han sido resueltas en menos de 24h
    porcentaje_more = df['more_24h'].sum() / df['less_24h'].count() * 100
    
    df_filtered = df[df['more_24h'] == 1] # solo aquellas incidencias que han sido resueltas en menos de 24h 

    # un único pie chart coloreado por tipo de contacto, indicando el % de incidencias que han sido resueltas en menos de 24h
    pie = px.pie(df_filtered, names='contact_type', title=f'Incidencias resueltas en más de 24h - {porcentaje_more:.2f}%', 
                 labels={'contact_type':'Tipo de contacto'}, height=400)

    st.plotly_chart(pie)

def pie_chart_reasigned(df):
    
    
    # guardar en una variable el % de incidencias que han sido resueltas en menos de 24h
    porcentaje_reasigned = df['reassingment_count_bool'].sum() / df['reassingment_count_bool'].count() * 100
    
    df_filtered = df[df['reassingment_count_bool'] == 1] # solo aquellas incidencias que han sido resueltas en menos de 24h 

    # un único pie chart coloreado por tipo de contacto, indicando el % de incidencias que han sido resueltas en menos de 24h
    pie = px.pie(df_filtered, names='contact_type', title=f'Incidencias reasignadas - {porcentaje_reasigned:.2f}%', 
                 labels={'contact_type':'Tipo de contacto'}, height=400)

    st.plotly_chart(pie)

def pie_chart_not_reasigned(df):
    # cambiar los 1 por 0 y los 0 por 1
    df['reassingment_count_bool'] = df['reassingment_count_bool'].apply(lambda x: 0 if x == 1 else 1)
    # guardar en una variable el % de incidencias que han sido resueltas en menos de 24h
    porcentaje_not_reasigned = df['reassingment_count_bool'].sum() / df['reassingment_count_bool'].count() * 100
    
    df_filtered = df[df['reassingment_count_bool'] == 1] # solo aquellas incidencias que han sido resueltas en menos de 24h 

    # un único pie chart coloreado por tipo de contacto, indicando el % de incidencias que han sido resueltas en menos de 24h
    pie = px.pie(df_filtered, names='contact_type', title=f'Incidencias no reasignadas - {porcentaje_not_reasigned:.2f}%', 
                 labels={'contact_type':'Tipo de contacto'}, height=400)

    st.plotly_chart(pie)



# FUNCIONES AUXILIARES ---------------------------------------------------------------------------------

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
