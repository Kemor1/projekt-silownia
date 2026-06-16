#!/bin/sh
python manage.py migrate --noinput
python create_admin.py
python manage.py runserver 0.0.0.0:8000