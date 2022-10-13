FROM gitpod/workspace-full

RUN pip install pandas snowflake-connector-python snowflake-snowpark-python streamlit

WORKDIR /snow/tmp

RUN { curl -LJO https://sfc-repo.snowflakecomputing.com/snowsql/bootstrap/1.2/linux_x86_64/snowsql-1.2.22-linux_x86_64.bash ; \
      chmod +x snowsql-linux_x86_64.bash ; \
      bash snowsql-linux_x86_64.bash ; \
}
