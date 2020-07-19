#!/bin/bash dev academy

cd /var/www/html/academy/
git pull origin master &&
pip install -r requirements.txt
./manage.py collecstatic --noinput
./manage.py compress --force
./manage.py migrate
./manage.py test tests
systemctl restart academy