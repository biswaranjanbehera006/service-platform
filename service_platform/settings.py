"""
Django settings for service_platform project.
"""

from pathlib import Path
import os

import dj_database_url

from decouple import config

# 📁 BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent


# 🔐 SECURITY
SECRET_KEY = 'django-insecure-4!46zc&%vx(6pr)!b-pl&7d%i_#gx-r%w_jh*tp^vd^!o92k+5'

DEBUG = True

ALLOWED_HOSTS = []


# 📦 APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 🔥 CUSTOM APPS
    'users',
    'services',
    'bookings',
    'providers',
    'admin_panel',
]


# ⚙️ MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# 🔗 ROOT URL
ROOT_URLCONF = 'service_platform.urls'


# 🎨 TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # 🔥 GLOBAL TEMPLATE FOLDER
        'DIRS': [os.path.join(BASE_DIR, 'templates')],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',

                # 🔥 REQUIRED FOR YOUR BACK BUTTON FIX
                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# 🚀 WSGI
WSGI_APPLICATION = 'service_platform.wsgi.application'


#Database Connection


import dj_database_url

DATABASES = {
    'default': dj_database_url.parse(
        "postgresql://postgres.kpayxawprkjtzryehhbn:Biswaranjan@123@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres",
        conn_max_age=600,
        ssl_require=True
    )
}

# 🔐 Extra SSL Safety (recommended)
DATABASES['default']['OPTIONS'] = {
    'sslmode': 'require',
}





# 🔐 PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 🌍 INTERNATIONAL SETTINGS
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'   # 🔥 Changed for India

USE_I18N = True
USE_TZ = True


# 📂 STATIC FILES
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# 🔥 OPTIONAL (FOR PRODUCTION)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# 📁 MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# 👤 CUSTOM USER MODEL
AUTH_USER_MODEL = 'users.User'


# 🔐 LOGIN SETTINGS
LOGIN_URL = '/users/login/'

# 🔥 AFTER LOGIN DEFAULT (fallback)
LOGIN_REDIRECT_URL = '/'

# 🔥 LOGOUT REDIRECT
LOGOUT_REDIRECT_URL = '/'


# 📨 MESSAGE TAG STYLING (BOOTSTRAP FRIENDLY)
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')