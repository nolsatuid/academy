#!/bin/bash dev academy

cd /var/www/html/academy/
git pull origin master &&
source env/bin/activate
pip install -r requirements.txt
./manage.py collectstatic --noinput
./manage.py compress --force
./manage.py migrate
./manage.py test tests
systemctl restart academy