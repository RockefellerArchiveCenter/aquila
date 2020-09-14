#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
./wait-for-it.sh db:5432 -- python manage.py migrate

# Create initial organizations and users
echo "Create initial user"
python manage.py shell < ./setup_user.py

#Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
