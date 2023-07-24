#!/bin/sh

echo "migrate"
python manage.py migrate
echo "collectstatic"
python manage.py collectstatic
@echo "copy static"
backend cp -r /app/static/. /static/

exec "$@"
