#!/bin/bash

set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

rm -rf /data/static-files/*
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
gunicorn -c gunicorn.conf.py GroupPlus.wsgi:application
