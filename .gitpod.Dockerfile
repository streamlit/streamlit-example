FROM gitpod/workspace-full

RUN pip install pandas snowflake-connector-python snowflake-snowpark-python streamlit
