#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# These create the temporary SQLite DB and static files
python manage.py collectstatic --no-input
python manage.py migrate