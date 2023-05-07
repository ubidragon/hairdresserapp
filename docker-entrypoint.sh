#!/bin/bash

    
django-admin startproject hairdresser
django-admin startapp hairdresserapp

python manage.py runserver 0.0.0.0:80

tail -f /dev/null