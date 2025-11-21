#!/bin/sh

set -e

# run app migrations
python ./manage.py migrate
# collect static assets
python ./manage.py collectstatic --no-input

# start Apache
httpd -D FOREGROUND