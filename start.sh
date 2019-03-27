#!/bin/bash

file=.first_run
if [ ! -e "$file" ]; then
    echo "Performin first time setup"
    python manage.py makemigrations miniipip
    python manage.py migrate
    python manage.py loaddata db.json
    touch "$file"
    echo "Done"
fi 

# Start Gunicorn processes
echo "Starting Gunicorn"

exec gunicorn myproject.wsgi:application \
    --bind 0.0.0.0:8000 \
    --threads=2
