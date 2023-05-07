FROM python:3.11-slim-bullseye

RUN apt update && \
    apt install gcc libmariadb3 libmariadb-dev -y && \
    python3 -m pip install --upgrade pip

COPY docker-entrypoint.sh /tmp/docker-entrypoint.sh

RUN mv /tmp/docker-entrypoint.sh /docker-entrypoint.sh && chmod +x docker-entrypoint.sh

WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt



ENTRYPOINT [ "/docker-entrypoint.sh" ]

# COPY ./code /code/ # Solo para empaquetado y distribucion de la app
