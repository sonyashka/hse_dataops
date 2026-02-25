FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g configurable-http-proxy

WORKDIR /srv/jupyterhub

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    jupyterhub \
    jupyterlab \
    notebook \
    psycopg2-binary \
    sqlalchemy \
    alembic

RUN groupadd -r jupyterhub && useradd -r -g jupyterhub jupyterhub

RUN mkdir -p /srv/jupyterhub/data /srv/jupyterhub/log && \
    chown -R jupyterhub:jupyterhub /srv/jupyterhub

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
RUN chown jupyterhub:jupyterhub /srv/jupyterhub/jupyterhub_config.py

EXPOSE 8000

USER jupyterhub

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]