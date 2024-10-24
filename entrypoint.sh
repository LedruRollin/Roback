#!/bin/sh

set -e

echo "${0}: Running migrations"
python3 src/manage.py flush --no-input
python3 src/manage.py makemigrations --merge
python3 src/manage.py migrate --noinput

echo "${0}: Populating seed data"
python3 src/manage.py seeder

echo "${0}: Create users"
# Note that in a real environment these info should never been saved here
DJANGO_SUPERUSER_PASSWORD=pwd python3 src/manage.py createsuperuser --username=admin --email=admin@example.com --noinput

echo "${0}: Running server"
python3 src/manage.py runserver 0.0.0.0:8000
