#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

import os
import logging

from datetime import timedelta

# SECRET KEY SECTION
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o6=iy(t5gbr*^w4^gktgh10u10r+yup+k9n1bfphp^$(u@*qmp'

# DEBUG SECTION
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# BASE DIR PATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ALLOWED HOSTS DEFINED HERE
ALLOWED_HOSTS = ['*']

# INSTALLED APPS MENTIONED HERE
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'invoice',
    'bulma',
    'axes',




]
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/var/backups/'}



# LANGUAGE COOKIE
LANGUAGE_COOKIE_AGE = None
LANGUAGE_COOKIE_HTTPONLY = False

# AUTHENTICATION BACKEND BY AXES
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# SESSION SETTINGS
SESSION_EXPIRE_SECONDS = 3000000000000  # seconds
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 60  # group by minute
SESSION_TIMEOUT_REDIRECT = 'login'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 5 * 60
SESSION_COOKIE_SECURE = True

# CSRF SETTINGS
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_NAME = 'apro'
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_PATH = '/'
CSRF_HEADER_NAME = 'django.views.csrf.csrf_failure'

# SECURE CONTENT TYPE
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
SIGNING_BACKEND = 'django.core.signing.TimestampSigner'
SESSION_FILE_PATH = '/'

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'axes.middleware.AxesMiddleware',
    'django_auto_logout.middleware.auto_logout',
]

# AUTO LOGOUT SETTINGS
AUTO_LOGOUT = {
    # 5 MINUTES DEFAULT IDLE TIME
    'IDLE_TIME': timedelta(minutes=50),
    # AUTO LOGOUT CUSTOM MESSAGE
    'MESSAGE': 'OOPS you are not login. '
               'Please login again to continue.',
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
}

# AXES CONFIGURATION
AXES_ENABLED = True
AXES_FAILURE_LIMIT = 13
AXES_COOLOFF_TIME = 0.2
AXES_LOCKOUT_CALLABLE = "invoice.views.lockout"

# TEMPLATE SECTION
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

# WSGI APPLICATION REGISTER
WSGI_APPLICATION = 'mysite.wsgi.application'

# DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'apro.sqlite3'),
    }
}

# PASSWORD VALIDATOR
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

# PASSWORD HASHERS
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ROOT URL CONFIGURATION
ROOT_URLCONF = 'mysite.urls'

# STATIC FILES AND MEDIA FILES SETTINGS AND PATH CONFIGURATION
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), '/var/www/static/', ]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_cdn')

