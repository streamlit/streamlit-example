from sqlalchemy import create_engine
import streamlit as st
import pandas as pd

conn = create_engine("mssql+pyodbc://dbadmin:Barcelona2020@bdigital.database.windows.net/[dbo]?charset=utf8mb4")

#Databases/DemoBudget

SQL_Query = pd.read_sql('SELECT [Customer Group],[Importe] FROM [dbo].[FGastosCliente]', conn)

st.write("My First App")
df = pd.DataFrame(SQL_Query, columns=['[Customer Group]','[Importe]'])
st.line_chart(df)
