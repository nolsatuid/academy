# Nolsatu Academy

## Prerequisite
  - Python 3.6.x already installed on system or using virtualenv
  - Postgresql 9.6.x
  - wkhtmltopdf 0.12.3
  - Redis Server 3.0 or latter

## Development Setup
Install dependencies

```
$ pip install -r requirements.txt
```

Create your own settings and modify as your preference

```
$ cp academy/local_settings.py.sample academy/local_settings.py
```

Configure database connection in `local_settings.py` with the database, database user, redis cookies domain and database password you configure in postgreSQL.

Migrate database

```
$ python manage.py migrate
```

Run this command to seeding initial data settings

```
$ python manage.py seeding_initial_settings
```

Collect Static

```
$ python manage.py collectstatic
```

Compress Static File

```
$ python manage.py compress --force
```

Create superuser

```
$ python manage.py createsuperuser
Username (leave blank to use 'btech'):
Email address: contact@btech,id
Password:
Password (again):
Superuser created successfully.
```

Runing the service

```
python manage.py runserver
```

Then open your browser http://localhost:8000 and voila your web apps is already running !


## Server Installation And Configuration

### Pre-Installation

You need to install the following apps:

- python3.6
- Nginx
- PostgreSQL
- virtualenv

### Application Setup


Clone the latest source code from the repository, and I assume you put it to `/var/www/html/`

```
$ cd /var/www/html/
$ git clone {repository}
$ cd academy
```

Then create virtualenv with python3

```
$ virtualenv --python=python3.6
$ source/env/bin/activate
$ pip install -r requirements.txt
$ pip install gunicorn
```

Then create a configuration file, just copy from sample file and modify as your preference

```
$ cp academy/local_settings.py.sample academy/local_settings.py
```


Then run the database migration

```
$ python manage.py migrate
```

Then create first superuser

```
$ python manage.py createsuperuser
Username (leave blank to use 'btech'):
Email address:
Password:
Password (again):
Superuser created successfully.
```

Then create systemd file, just copy sample file and modify as your preference

```
$ sudo cp scripts/etc/systemd/system/academy.service /etc/systemd/system/
$ sudo cp scripts/etc/systemd/system/rqworker.service /etc/systemd/system/
```


Then configure nginx, just copy sample file and modify as your preference

```
$ sudo cp scripts/etc/nginx/sites-available/sample.conf /etc/nginx/sites-available/academy.conf
$ sudo ln -s /etc/nginx/sites-available/academy.conf /etc/nginx/sites-enabled/academy.conf
```

Then generate static files

```
$ python manage.py collectstatic
```

Create logs directory

```
$ mkdir logs
```

Then start the service

```
$ sudo systemctl enable academy
$ sudo systemctl start academy
$ sudo systemctl enable rqworker
$ sudo systemctl start rqworker
$ sudo systemctl restart nginx
```


### Cronjob Settings


## Sysadmin daily operation

- Deploy the latest update

```
$ source env/bin/activate
$ git pull origin master
$ python manage.py migrate
$ python manage.py collectstatic
$ update_setting.sh dev/prod
$ sudo systemctl restart academy
```

- Start Service

```
$ sudo systemctl start academy
```

- Stop Service

```
$ sudo systemctl stop academy
```

- Restart Service

```
$ sudo systemctl restart academy
```
