#!/bin/sh
cd webapps/smartrec
ls
git pull https://sinchanakram:26081995@bitbucket.org/ManjuShankar/smartrec.git
python manage.py migrate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py setup
python manage.py runserver

