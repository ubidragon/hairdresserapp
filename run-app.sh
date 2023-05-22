#!/bin/bash

docker-compose up -d

docker exec hairdresserapp_web bash -c "python manage.py loaddata populate.json"
