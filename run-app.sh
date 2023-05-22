#!/bin/bash

docker-compose up -d

docker exec hairdresserapp_web bash -c "python manage.py loaddata populate.json"
docker exec hairdresserapp_web bash -c "python manage.py crontab add"
