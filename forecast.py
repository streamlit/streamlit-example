import streamlit as st
import pandas as pd
from prophet import Prophet
import pmdarima as pmd
import statsmodels.api as sm
from datetime import datetime, date
import matplotlib.pyplot as plt

###################################
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode

###################################
import model as md
from functionforDownloadButtons import download_button
import footer as footer
###################################

def _max_width_():
    max_width_str = f"max-width: 2400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_icon="📊", page_title="Forecast",layout="wide")








###################################

with st.sidebar:
    st.image(
    "https://www.duytan.com/Data/Sites/1/media/home/logo_duytan_scgp-endorsement_full-color-01.png",
    width=300,
    )    
    st.title("TIME SERIES FORECAST")
    st.title("1. Select Data")
    uploaded_file = st.file_uploader("Choose a Excel file")
    
    
    #####
    footer.footer()
    
    #####

     
    if uploaded_file is not None:
        shows = pd.read_excel(uploaded_file, sheet_name = "Sheet1")
        shows = shows.fillna(0)
        #uploaded_file.seek(0)
        #st.write(shows)
        #unpivot & pivot to WIDE-FORMAT
        shows = pd.melt(shows, id_vars=shows.columns[0])
        #shows.sort_values(by=['Date'],inplace=True)
        shows["Date"] = shows["Date"].apply(lambda x: x.date())
        shows2 = shows.copy(deep=True)
        shows2["Date"] = shows2["Date"].apply(lambda x: x.strftime("%m-%Y"))
        #shows.set_index(['Date', 'variable'],inplace=True)
        #shows = shows.unstack('Date').reset_index()
        shows = pd.pivot_table(shows, values="value",index="variable",columns="Date").reset_index()
        shows.rename({'variable': 'Material'}, axis=1, inplace=True)
        shows2 = pd.pivot_table(shows2, values="value",index="variable",columns="Date").reset_index()
        shows2.rename({'variable': 'Material'}, axis=1, inplace=True)
        st.info(
            f"""
                👆 Upload your .xlsx file to make forecast. Here's a sample file: [Actual Sales](https://duytan-my.sharepoint.com/:x:/g/personal/phamgiaphu_duytan_com1/EYe1ArKWaulDhLa1G9mPrnMB7C3G_F_mkvJ-7c93u6c9kw?e=j3HVCj)
                """)
        
        
    else:
        st.info(
            f"""
                👆 Upload your .xlsx file to make forecast. Here's a sample file: [Actual Sales](https://duytan-my.sharepoint.com/:x:/g/personal/phamgiaphu_duytan_com1/EYe1ArKWaulDhLa1G9mPrnMB7C3G_F_mkvJ-7c93u6c9kw?e=j3HVCj)
                """)
        st.stop()

###################################





st.subheader('2. Data loading 📋')
st.write("Your raw data will show here.")
st.write(shows)



from st_aggrid import GridUpdateMode, DataReturnMode

st.subheader('3. Forecast')
col1, col2 = st.columns([1,1])
with col1:
    with st.container():
        gb = GridOptionsBuilder.from_dataframe(shows2)
        gb.configure_default_column(enablePivot=False, enableValue=False, enableRowGroup=False)
        gb.configure_selection(selection_mode="single",use_checkbox=True)
        gb.configure_column(shows2.columns[0],headerCheckboxSelection=False)
        gb.configure_side_bar()
        gridOptions = gb.build()
  
        response = AgGrid(
            shows2,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            fit_columns_on_grid_load=False,
        )

with col2:
    model = st.multiselect(
    'Choose your forecast model',
    ['UCM', 'SARIMAX', 'Prophet', 'Holt-Winter'],
    ['Holt-Winter'])


    df = pd.DataFrame(response["selected_rows"])
    df = pd.melt(df,id_vars=shows.columns[0])
    df.rename({'variable': 'Date'}, axis=1, inplace=True)
    df['Date'] = df['Date'].apply(lambda x: datetime.strptime("01-{}".format(x),"%d-%m-%Y").date())
    df = pd.DataFrame(df.pivot('Date','Material','value'))
    df.index = pd.to_datetime(df.index)
    if 'Holt-Winter' in model:
        df_HW = md.HoltWinter(df)
        df = df.merge(df_HW,left_index=True,right_index=True,how='outer',indicator=True)
    if 'SARIMAX' in model:
        df_SARIMAX = md.SARIMAX(df)
        df = df.merge(df_SARIMAX,left_index=True,right_index=True,how='outer',indicator=True)
    if 'UCM' in model:
        df_UCM = md.UCM(df)
        df = df.merge(df_UCM,left_index=True,right_index=True,how='outer',indicator=True)
    
    
    df.drop(['_merge'],axis=1,inplace=True)
    
    #df.sort_values(by=['Material','Date'],inplace=True)
    
    st.line_chart(df)
    
    

st.subheader("Filtered data will appear below 👇 ")
st.text("")

st.table(df)

st.text("")



import xlsxwriter
from io import BytesIO
buffer = BytesIO()

with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file to the buffer
    writer.save()

    st.download_button(
        label="Download Excel worksheets",
        data=buffer,
        file_name="forecast.xlsx",
        mime="application/vnd.ms-excel"
    )
