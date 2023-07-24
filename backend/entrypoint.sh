#!/bin/sh

python manage.py migrate
python manage.py load_csv
python manage.py collectstatic
backend cp -r /app/static/. /static/
gunicorn --bind 0.0.0.0:8000 backend.wsgi

exec "$@"