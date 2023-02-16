import streamlit as st
from snowflake.snowpark import Session
import pandas as pd

@st.experimental_singleton # magic to cache db connection
def create_connection() -> Session:
    connection_parameters = {
        "account": st.secrets["account"],
        "user": st.secrets["user"],
        "password": st.secrets["password"],
        "role": st.secrets["role"],
        "warehouse": st.secrets["warehouse"],
        "database": st.secrets["database"],
        "schema": st.secrets["schema"]
        }

    session = Session.builder.configs(connection_parameters).create()
    return session

def validate_session():
    try:
        session = st.session_state['snowpark_session']
        session.sql('select 1;')
    except:
        return False
    return True

def get_session() -> Session:
    if "snowpark_session" not in st.session_state:
        session = create_connection()
        st.session_state['snowpark_session'] = session
    else:
        if validate_session():
            session = st.session_state['snowpark_session']
        else:
            session = create_connection()
            st.session_state['snowpark_session'] = session
    return session


def check_password() -> bool:
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["admin_password"] == st.secrets["admin_password"]:
            st.session_state["password_correct"] = True
            del st.session_state["admin_password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="admin_password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="admin_password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True