FROM python:3.11-slim-bullseye

RUN apt update && \
    apt install gcc cron libmariadb3 libmariadb-dev -y && \
    python3 -m pip install --upgrade pip

COPY docker-entrypoint.sh /tmp/docker-entrypoint.sh

RUN mv /tmp/docker-entrypoint.sh /docker-entrypoint.sh && chmod +x docker-entrypoint.sh

COPY ./code/hairdresser /hairdresser

WORKDIR /hairdresser
COPY requirements.txt /hairdresser/
RUN pip install -r requirements.txt \
	&& rm -rf /hairdresser/requirements.txt

ENTRYPOINT [ "/docker-entrypoint.sh" ]
