FROM gitpod/workspace-full

# USER gitpod

RUN pip install pandas snowflake-connector-python snowflake-snowpark-python streamlit

# WORKDIR /snow/tmp

ENV SNOWSQL_LOGIN_SHELL=/home/gitpod/.profile
ENV SNOWSQL_DEST=/bin

RUN { mkdir -p ~/utils/snowsql ; cd ~/utils/snowsql ; curl -LJOf https://sfc-repo.snowflakecomputing.com/snowsql/bootstrap/1.2/linux_x86_64/snowsql-1.2.22-linux_x86_64.bash ; \
      chmod +x ~/utils/snowsql/snowsql-1.2.22-linux_x86_64.bash ; \
      # sudo ~/utils/snowsql/snowsql-1.2.22-linux_x86_64.bash ; \
}

# USER root
