# coding:utf-8 
"""
Django settings for phxweb project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""用户模块扩展部分"""
AUTH_PROFILE_MODULE = 'djangoadmin.myadmin.UserProfile'
"""用户模块扩展完成"""

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm1!&%(kha(g04bl7ek*hh@ly$ibnm8@2zrnkmxxkzcf6jjc4d@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/accounts/login'

#telegram api
TG_API = {
    'url': 'https://api.telegram.org/bot471691674:AAFx1MQ3VwXdWUYyh4CaErzwoUNswG9XDsU',
    'chat_id': {
        'salt_minion_alert': '-275535278',
    }
}

#saltstack api
SALT_API = {
    'url':"https://58.64.145.50:8000/",
    #'url_glb':"https://172.20.10.109:8000/",
    'user':"api",
    'password':"phexus666",
}

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'monitor',
    'saltstack',
    'cfapi',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'phxweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'phxweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'phxweb',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'phxweb',
        'PASSWORD': 'phexus666',
        'HOST': '58.64.145.50',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',                      # Set to empty string for default.
        'OPTIONS': {
            #'init_command': 'SET sql_mode=STRICT_TRANS_TABLES',
            'charset': 'utf8',
        },
    }
}

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(filename)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        #'mail_admins': {
        #    'level': 'ERROR',
        #    'class': 'django.utils.log.AdminEmailHandler',
        #    'include_html': True,
        #},
        'default': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logs/','access.log'),
            'maxBytes': 1024*1024*50, # 5 MB
            'backupCount': 10,
            'formatter':'standard',
        },
        #'console':{
        #    'level': 'DEBUG',
        #    'class': 'logging.StreamHandler',
        #    'formatter': 'standard'
        #},
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logs/','debug.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 10,
            'formatter':'standard',
        },
        'error': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logs/','error.log'), 
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 10,
            'formatter':'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'error', 'request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        #'django.request': {
        #    'handlers': ['request_handler'],
        #    'level': 'DEBUG',
        #    'propagate': False
        #},
    }
}     
