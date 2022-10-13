FROM gitpod/workspace-full

USER gitpod

RUN pip install pandas snowflake-connector-python snowflake-snowpark-python streamlit

# WORKDIR /snow/tmp
RUN curl -LJOf https://sfc-repo.snowflakecomputing.com/snowsql/bootstrap/1.2/linux_x86_64/snowsql-1.2.22-linux_x86_64.bash

RUN { mkdir -p ~/utils/snowsql ; cd ~/utils/snowsql ;  \
      cp snowsql-1.2.22-linux_x86_64.bash ~/utils/snowsql/ ; chmod +x ~/utils/snowsql/snowsql-1.2.22-linux_x86_64.bash ; \
      bash ~/utils/snowsql/snowsql-1.2.22-linux_x86_64.bash ; \
}

USER root
