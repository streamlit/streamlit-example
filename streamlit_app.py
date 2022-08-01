from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

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

    with st.expander("Overview of product scoring rules"):
        cols = st.columns(4)
        cols[0].write(f'**Layer name**')
        cols[1].write(f'**Rule Type**')
        cols[2].write(f'**Min Value**')
        cols[3].write(f'**Max Value**')

        for filename in filenames: 

            



            if activated_layers_dict[filename]['active']:

                cols = st.columns(4)
                cols[0].write(f'{filename}')
                cols[1].write(f'{ activated_layers_dict[filename]["type of analysis"] }')


                # st.write('For: ', activated_layers_dict[filename]['name'])
                # st.write('Type of analysis selected: ', activated_layers_dict[filename]['type of analysis'])

                for key,value in activated_layers_dict[filename]['parameters'].items():
                    # st.write(key, value)
                    if key == "min_val":
                        cols[2].write(f'{value}')

                    elif key == 'max_val':
                        cols[3].write(f'{value}')

    return None 





if check_password():


    st.write("Here goes your normal Streamlit app...")'
    main_app()
