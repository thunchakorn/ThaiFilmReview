#!/usr/bin/env bash
set -o errexit

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# load initial data
python manage.py loaddata initial

if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input
fi