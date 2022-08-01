from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

import plotly.express as px

"""
Overview of PM priotitization 
"""


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
    st.subheader('Overview of active rules')

    cols = st.columns(4)
    cols[0].write(f'**Layer name**')
    cols[1].write(f'**Rule Type**')
    cols[2].write(f'**Min Value**')
    cols[3].write(f'**Max Value**')

    for filename in [1,2,3,4]: 



        cols = st.columns(3)

        col1, col2, col3 = st.columns(3)
        col1.metric(f'{filename}', 5, -1)
        col2.metric("Wind", "9 mph", "-8%")
        col3.metric("Humidity", "86%", "4%")

        cols[0].write(f'{filename}')
        
        cols[1].write(f'{ filename **2 }')
        cols[2].write(f'{ filename **3 }')



        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", "70 °F", "1.2 °F")
        col2.metric("Wind", "9 mph", "-8%")
        col3.metric("Humidity", "86%", "4%")

        st.write("---")
    

    
    df = px.data.gapminder()

    fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp",
                size="pop", color="continent",
                    hover_name="country", log_x=True, size_max=60)
    fig.show()



    return None 





if check_password():


    st.write("Here goes your normal Streamlit app...")
    main_app()
