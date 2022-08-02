from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

import plotly.express as px


import pandas as pd
import gspread

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True





def main_app():







    st.title('Overview of active products')
    st.caption('Change is defined as difference in average during the last month')

    with st.spinner('Loading data and sorting the scoring..'):
        gc = gspread.service_account(filename='Authentification\key_google.json')
        sps = gc.open('Product Portfolio Planning')
        product_feedback = sps.get_worksheet_by_id(1479889959)
        data = product_feedback.get_all_values()
        headers = data.pop(0)
        df = pd.DataFrame(data, columns=headers)

        df['Business value (k NOK) [MIN]'] = pd.to_numeric(df['Business value (k NOK) [MIN]'], errors='coerce')
        df['Business value (k NOK) [MAX]'] = pd.to_numeric(df['Business value (k NOK) [MAX]'], errors='coerce')

        # df.columns

        df_res = df.groupby(['Product']).mean().reset_index()
        df_res['count'] = df.groupby(['Product']).count().reset_index()['ID']


        df_res.sort_values(by=['count'])

        df_res





    # Logic for sorting by score here. 
    

    for filename in [1,2,3,4]: 
    
        st.subheader("PRODUCT NAME")


        cols = st.columns(4)
        cols[0].write(f'**Product Name**')
        cols[1].write(f'**Rule Type**')
        cols[2].write(f'**Min Value**')
        cols[3].write(f'**Max Value**')

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(f'{filename}', 5, -1)
        col2.metric("Wind", "9 mph", "-8%")
        col3.metric("Humidity", "86%", "4%")
        col4.metric("Humidity", "86%", "4%")

        st.write("---")
    

    
    df = px.data.gapminder()

    fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp",
                size="pop", color="continent",
                    hover_name="country", log_x=True, size_max=60)

    import base64
    img_file = "background_go_zone.png"
    background = base64.b64encode(open(img_file, 'rb').read())

    fig.update_layout(
                    images= [dict(
                        source='data:image/png;base64,{}'.format(background.decode()),
                        xref="paper", yref="paper",
                        x=0, y=1,
                        sizex=1, sizey=1,
                        xanchor="left",
                        yanchor="top",
                        sizing="stretch",
                        layer="above")])
 

    st.plotly_chart(fig)



    return None 

import pickle

def set_score():
    with st.form("set_score"):


        option_sort = st.selectbox('Sort list by', ['Avg Max', 'Avg Min', 'Count', 'Score'] )

        set_max_value = st.text_input('Max value', '', placeholder = 'write (numeric K NOK) value that yields 10')
        set_max_time  = st.text_input('Max time --> Above this yields 0', '', placeholder = 'write (numeric FTE months) value that yields 0')

        suby = st.form_submit_button("Submit")

        if suby:

            st.success("Feature added")


    return None 




if check_password():
    



    main_app()

    set_score()

    
