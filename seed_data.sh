#!/bin/bash

rm -rf practiceplanapi/migrations
rm db.sqlite3
python manage.py makemigrations practiceplanapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata players
python manage.py loaddata categories
python manage.py loaddata exercises
python manage.py loaddata practiceplans
python manage.py loaddata sessions
