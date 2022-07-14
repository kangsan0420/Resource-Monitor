FROM python:3.10.2-slim

RUN apt-get update \
    && apt-get install -y --allow-unauthenticated vim curl nginx supervisor

RUN pip3 install uvicorn fastapi fastapi_utils pyyaml paramiko tqdm numpy \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs

COPY ./config/server.conf /etc/nginx/conf.d/server.conf
COPY ./config/programs.conf /etc/supervisor/conf.d/programs.conf
COPY ./ /app

RUN rm -f /app/server_ids.conf \
    && cd /app/frontend \
    && npm install \
    && cd /app

ENTRYPOINT cd /app/frontend && npm run build && cd /app && supervisord -n
