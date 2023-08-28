# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from decouple import config
from unipath import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_1122')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# load production server from .env
ALLOWED_HOSTS = [('*')]
CSRF_TRUSTED_ORIGINS = ['https://f7f5-200-211-62-61.ngrok-free.app']




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.home',
    'apps.banco',
    'apps.boletim',
    'rest_framework',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

HOST_DEFAULT_IP       = config('HOST_DEFAULT_IP')
HOST_DEFAULT_USER     = config('HOST_DEFAULT_USER')
HOST_DEFAULT_PASSWORD = config('HOST_DEFAULT_PASSWORD')
HOST_DEFAULT_NAME     = config('HOST_DEFAULT_NAME')
HOST_DEFAULT_PORT     = config('HOST_DEFAULT_PORT')

HOST_SECOND_IP       = config('HOST_SECOND_IP')
HOST_SECOND_USER     = config('HOST_SECOND_USER')
HOST_SECOND_PASSWORD = config('HOST_SECOND_PASSWORD')
HOST_SECOND_NAME     = config('HOST_SECOND_NAME')
HOST_SECOND_PORT    = config('HOST_SECOND_PORT')

# DATABASE_ROUTERS = ['apps.banco.dbrouters.DefaultDbRouter', 'apps.banco.dbrouters.SqlServerDbRouter']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': HOST_DEFAULT_NAME,
        'USER': HOST_DEFAULT_USER,
        'PASSWORD': HOST_DEFAULT_PASSWORD,
        'HOST': HOST_DEFAULT_IP,
        'PORT': HOST_DEFAULT_PORT,
        'OPTIONS': {
            'options': '-c search_path=4fluid-iot'
        }
    },
    'sql_server': {
        'ENGINE': 'mssql',
        'NAME': HOST_SECOND_NAME,
        'USER': HOST_SECOND_USER,
        'PASSWORD': HOST_SECOND_PASSWORD,
        'HOST': HOST_SECOND_IP,
        'PORT': HOST_SECOND_PORT,
        'OPTIONS': {
            'driver': "SQL Server Native Client 11.0",
            'options': '-c search_path=dbo',
        },
    }
}

DATABASE_CONNECTION_POOLING = False


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)


#############################################################
#############################################################
