import streamlit as st
from namelist_validator import NamelistValidator
import pandas as pd


st.title("AceCast Namelist Advisor v0.7")

namelist_file = st.file_uploader("Upload namelist file (FORTRAN namelist format)", type=["nml", "txt", "input"])


if namelist_file:
    validator = NamelistValidator("registry-v3.0.1.json", namelist_file)


    errors = validator.validate()
    if not errors:
        st.success("Namelist validation success!")
    else:
        st.error("Namelist validation failure. One or more unsupported options found!")
        if errors:
            error_df = pd.DataFrame(errors)
            st.table(error_df)


else:
    st.warning("Please upload your namelist file")
