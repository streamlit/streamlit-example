from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Footy Wire",
    page_icon="🏉",
)


# Initialisation
np.random.seed(42)
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({})


st.title('Footywire scraping tool')
team = st.text_input('Select team', '')
xx = st.text_input('Select xxx', '')

@st.cache_data()
def gen_random_data(nrows):
    data = np.random.random((nrows,3))
    data_frame = pd.DataFrame(data,columns = ['A','B','C'])
    return data_frame

button = st.button('Scrape!',key = 'scrape_button')


if button:
    data_load_state = st.text('Loading data...')
    st.session_state.data = gen_random_data(10)
    data_load_state.text('Loading data...Done!')
    st.session_state.button_pressed = True

gb = GridOptionsBuilder.from_dataframe(st.session_state.data)
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
gb.configure_grid_options(domLayout='normal')
st.session_state.gridOptions = gb.build()

grid_response = AgGrid(st.session_state.data,
                       gridOptions=st.session_state.gridOptions,
                       update_mode=GridUpdateMode.GRID_CHANGED,
                        height=300,
                        width='100%',
                        fit_columns_on_grid_load=False,
                        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
                        enable_enterprise_modules=False,
                        editable = True)

st.download_button("Download data",
                   data=grid_response['data'].to_csv(),
                   file_name='test_data.csv')
