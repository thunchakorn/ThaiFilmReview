#!/usr/bin/env bash
set -o errexit

# Convert static asset files (run automatically when deploy on Heroku)
# python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate --no-input

# load initial data
python manage.py loaddata initial

# create moderator group
python manage.py create_moderator_group

# compile messages
python manage.py compilemessages

# uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload --reload-include '*.html'

# if [[ $CREATE_SUPERUSER ]];
# then
#   python manage.py createsuperuser --no-input
# fi
