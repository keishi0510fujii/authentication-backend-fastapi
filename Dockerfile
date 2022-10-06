FROM pypy:3.9-slim-buster as base
COPY ./app/requirements.txt /opt/app/requirements.txt
RUN apt-get update  && \
    pip install --no-cache-dir --upgrade -r /opt/app/requirements.txt
COPY ./app/* /opt/app/
RUN apt-get -y install tini && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

FROM pypy:3.9-slim-buster as dev
ARG USERNAME="fastapi"
ARG GROUPNAME="fastapi"
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID $GROUPNAME && \
    useradd -l -m -s /bin/bash -u $UID -g $GID $USERNAME
COPY --from=base --chown=$USERNAME:$GROUPNAME /opt/app /opt/app
COPY --from=base --chown=$USERNAME:$GROUPNAME /usr/bin/tini /usr/bin/tini
COPY --from=base --chown=$USERNAME:$GROUPNAME /opt/pypy/lib/pypy3.9/site-packages /opt/pypy/lib/pypy3.9/site-packages
COPY --from=base --chown=$USERNAME:GROUPNAME /opt/pypy/bin/uvicorn /opt/pypy/bin/uvicorn
ENV PYTHONPATH "${PYTHONPATH}:/opt/app"
EXPOSE 8008
WORKDIR /opt/app
USER $USERNAME