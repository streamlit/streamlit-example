# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.241.1/containers/python-3/.devcontainer/base.Dockerfile
# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT="3.8-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}
# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi
# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp
# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>
# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1
RUN sudo apt-get update
RUN sudo apt-get install unzip
# RUN apt-get install -y libpq-dev zlib1g-dev build-essential shared-mime-info libaio1 libaio-dev unzip wget --no-install-recommends
# RUN mkdir -p /opt/oracle
# WORKDIR /opt/oracle
# RUN wget https://download.oracle.com/otn_software/linux/instantclient/19800/instantclient-basic-linux.x64-19.8.0.0.0dbru.zip
# RUN unzip instantclient-basic-linux.x64-19.8.0.0.0dbru.zip
# ENV PATH="$PATH:/opt/oracle/instantclient_19_8"
# ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/opt/oracle/instantclient_19_8"
RUN mkdir -p /opt/oracle
WORKDIR /opt/oracle
RUN wget http://ftp.cn.debian.org/debian/pool/main/liba/libaio/libaio1_0.3.112-3_amd64.deb && \
    apt install ./libaio1_0.3.112-3_amd64.deb && \
    export LD_LIBRARY_PATH=/opt/oracle/instantclient_19_6:$LD_LIBRARY_PATH
RUN wget --user=mavenjio --password='mavenjio' http://10.141.51.157:9081/repository/maven-jiocom/python/instantclient/1.0/instantclient-1.0.zip && \
    unzip instantclient-1.0.zip && \
    rm -f instantclient-1.0.zip && \
    cd instantclient* && \
    rm -f *jdbc* *occi* *mysql* *jar uidrvci genezi adrci && \
    echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig
# RUN wget "https://github.com/GitCredentialManager/git-credential-manager/releases/download/v2.0.696/gcmcore-linux_amd64.2.0.696.deb" -O /tmp/gcmcore.deb
# RUN dpkg -i /tmp/gcmcore.deb
# RUN git-credential-manager-core configure
# RUN git config --global credential.credentialStore cache
# RUN git config --global credential.cacheoptions "--timeout 72000"
# ENV key="laas_encryption"
# ENV iv="laaskey_database"
# ENV salt="laas_AesEncryptionVec"
ENV iv="hcmpkey_database"
ENV key="hcmp_encryption"
ENV salt="hcmp_AesEncryptionVec"