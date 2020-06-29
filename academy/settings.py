"""
Django settings for academy project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sentry_sdk

from datetime import timedelta
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(SETTINGS_DIR)
PROJECT_NAME = os.path.basename(PROJECT_ROOT)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n-@n7d!%na!&^cd4^%al(z4%2vq0umr+fy_m6gmc(0_4uxbuwx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# do not mark / at the end of the host
HOST = 'http://academy.btech.id'
MEDIA_HOST = HOST
NOLSATU_COURSE_HOST = 'https://course.nolsatu.id'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',

    'academy.core',
    'academy.apps.accounts',
    'academy.apps.students',
    'academy.apps.logs',
    'academy.apps.graduates',
    'academy.apps.surveys',
    'academy.apps.offices',
    'academy.apps.campuses',
    'academy.apps.broadcasts',

    'post_office',
    'django_extensions',
    'qr_code',
    'rest_framework',
    'compressor',
    'ckeditor',
    'ckeditor_uploader',
    'multiselectfield',
    'django_rq',
    'fcm_django',
    'taggit',
    "meta",
    "django_keycloak.apps.KeycloakAppConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_keycloak.middleware.BaseKeycloakMiddleware',
]

SESSION_ENGINE = 'redis_sessions.session'

ROOT_URLCONF = 'academy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'academy.core.context_processors.nolsatu_context',
            ],
        },
    },
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'academy.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = (
    'academy.core.custom_auth.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
    'django_keycloak.auth.backends.KeycloakAuthorizationCodeBackend',
)

# other app
EMAIL_BACKEND = 'post_office.EmailBackend'

POST_OFFICE = {
    'BATCH_SIZE': 50,
    'THREADS_PER_PROCESS': 10,
    'BACKENDS': {
        'default': 'academy.core.email.backends.AcademySMTPEmailBackend'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'id'
# LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True

COUNTRY = 'ID'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static_files'),
)
STATIC_ROOT = os.path.join(SETTINGS_DIR, 'static')

INDICATOR_GRADUATED = 6
INDICATOR_REPEATED = 3

# JWT Config
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# django redis coockies
SESSION_COOKIE_DOMAIN = '.nolsatu.id'

# django cache using redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'TIMEOUT': 3699 * 24 * 3,  # 3 day
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        }
    }
}

# django compressor
COMPRESS_ENABLED = True
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

# ckeditor
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'width': '100%',
    },
    'basic_ckeditor': {
        'toolbar': 'Basic',
        'width': '100%',
    },
}

# django_rq
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
    'high': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 500,
    },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    }
}

FCM_DJANGO_SETTINGS = {
    "APP_VERBOSE_NAME": "NolSatu",
    "FCM_SERVER_KEY": "--ENTER_YOUR_SERVER_KEY",
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
}


API_GATEWAY = [
    ('course', 'https://course.nolsatu.id/api/')
]

SERVER_KEY = "serverToServerAuthKeyKeepItVerySecret"

# Keycloack
KEYCLOAK_OIDC_PROFILE_MODEL = 'django_keycloak.OpenIdConnectProfile'
KEYCLOAK_USE_PREFERRED_USERNAME = True
KEYCLOAK_USE_EMAIL_AS_USER_KEY = True
KEYCLOAK_SYNC_USER_MODEL_HANDLER = 'academy.core.utils.sync_keycloak_user'

try:
    from .local_settings import *
except ImportError:
    pass
