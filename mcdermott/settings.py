"""
Django settings for mcdermott project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import json
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
# Config options for production vs development
try:
  import config
except ImportError:
  import example_config as config

#GitHub auth
GITHUB_USERNAME = config.GITHUB_USERNAME
GITHUB_PASSWORD = config.GITHUB_PASSWORD

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = config.DEBUG

ALLOWED_HOSTS = config.ALLOWED_HOSTS

use_postgres = config.USE_POSTGRES
db_password = config.DB_PASSWORD


# Application definition

INSTALLED_APPS = (
  'login',
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'localflavor',
  'floppyforms',
  'rest_framework',
  'rolepermissions',
  'sorl.thumbnail',
  'watson',
  'widget_tweaks',
  'core',
  'mccalendar',
  'documents',
  'issues',
  'feedback',
)

MIDDLEWARE_CLASSES = (
  'django.contrib.sessions.middleware.SessionMiddleware',
  'unslashed.middleware.RemoveSlashMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'django.middleware.security.SecurityMiddleware',
  'watson.middleware.SearchContextMiddleware',
)

ROOT_URLCONF = 'mcdermott.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.contrib.auth.context_processors.auth',
        'django.template.context_processors.debug',
        'django.template.context_processors.i18n',
        'django.template.context_processors.media',
        'django.template.context_processors.static',
        'django.template.context_processors.tz',
        'django.core.context_processors.request',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]


WSGI_APPLICATION = 'mcdermott.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
sqlite_settings = {
  'ENGINE': 'django.db.backends.sqlite3',
  'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}

postgres_settings = {
  'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
  'NAME': 'mcdermott',                      # Or path to database file if using sqlite3.
  'USER': 'postgres',
  'PASSWORD': db_password,
  'HOST': 'localhost',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
  'PORT': '',                      # Set to empty string for default.
}

DATABASES = {
  'default': postgres_settings if use_postgres else sqlite_settings
}

# Caches
# https://docs.djangoproject.com/en/dev/topics/cache/

CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION': '127.0.0.1:11211',
  }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# User uploaded files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'media'))

# Default redirect after logging in successfully
LOGIN_REDIRECT_URL = '/'

# Default login url
LOGIN_URL = '/login'

# Django Rest Framework configuration
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

THUMBNAIL_DEBUG = config.DEBUG

ROLEPERMISSIONS_MODULE = 'mcdermott.roles'

# Removes trailing slash and tries URL again if it fails with the slash
APPEND_SLASH = False
REMOVE_SLASH = True

EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtpauth.utdallas.edu'
EMAIL_HOST_USER = config.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = config.DEFAULT_FROM_EMAIL
SERVER_EMAIL = DEFAULT_FROM_EMAIL

admin_email = config.ADMIN_EMAIL

ADMINS = (('Josh', admin_email))
