"""
Django settings for service_platform project.
"""

from pathlib import Path
import os

import dj_database_url
from decouple import config

# =========================
# 📁 BASE DIRECTORY
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# 🔐 SECURITY
# =========================
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-dev-key'
)

# ✅ PRODUCTION DEBUG
DEBUG = config(
    'DEBUG',
    default=False,
    cast=bool
)


#Resend OTP
RESEND_API_KEY = config('RESEND_API_KEY')


# ✅ ALLOWED HOSTS
ALLOWED_HOSTS = [

    '*',
]


# =========================
# 🔐 CSRF TRUSTED ORIGINS
# =========================
CSRF_TRUSTED_ORIGINS = [

    'https://*.onrender.com',

    'https://*.ngrok-free.app',
]


# =========================
# 📦 APPLICATIONS
# =========================
INSTALLED_APPS = [

    # DJANGO APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CLOUDINARY
    'cloudinary',
    'cloudinary_storage',

    # CUSTOM APPS
    'users',
    'services',
    'bookings',
    'providers',
    'admin_panel',
    'contact',
]


# =========================
# ⚙️ MIDDLEWARE
# =========================
MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    # ✅ WHITENOISE
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =========================
# 🔗 ROOT URL
# =========================
ROOT_URLCONF = 'service_platform.urls'


# =========================
# 🎨 TEMPLATES
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],

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


# =========================
# 🚀 WSGI
# =========================
WSGI_APPLICATION = 'service_platform.wsgi.application'


# =========================
# 🛢 DATABASE CONNECTION
# =========================
DATABASES = {

    'default': dj_database_url.parse(

        config('DATABASE_URL'),

        conn_max_age=0,

        ssl_require=True
    )

}

DATABASES['default']['OPTIONS'] = {

    'sslmode': 'require',

    'connect_timeout': 30,
}


# =========================
# 🔐 PASSWORD VALIDATION
# =========================
AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',

        'OPTIONS': {
            'min_length': 6,
        }
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =========================
# 🌍 INTERNATIONAL SETTINGS
# =========================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# =========================
# 📂 STATIC FILES
# =========================
STATIC_URL = '/static/'

STATICFILES_DIRS = [

    os.path.join(BASE_DIR, 'static')
]

# ✅ PRODUCTION STATIC ROOT
STATIC_ROOT = os.path.join(
    BASE_DIR,
    'staticfiles'
)

# ✅ WHITENOISE STORAGE
STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)


# =========================
# 📁 MEDIA FILES
# =========================
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(
    BASE_DIR,
    'media'
)


# =========================
# 👤 CUSTOM USER MODEL
# =========================
AUTH_USER_MODEL = 'users.User'


# =========================
# 🔐 LOGIN SETTINGS
# =========================
LOGIN_URL = '/users/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'


# =========================
# 📨 MESSAGE TAGS
# =========================
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {

    messages.DEBUG: 'secondary',

    messages.INFO: 'info',

    messages.SUCCESS: 'success',

    messages.WARNING: 'warning',

    messages.ERROR: 'danger',
}


# =========================
# 📧 EMAIL CONFIG
# =========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp-relay.brevo.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = config('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = config(
    'EMAIL_HOST_PASSWORD'
)

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')


# =========================
# 🔥 DEFAULT AUTO FIELD
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================
# 💳 RAZORPAY
# =========================
RAZORPAY_KEY_ID = config(
    'RAZORPAY_KEY_ID'
)

RAZORPAY_KEY_SECRET = config(
    'RAZORPAY_KEY_SECRET'
)


# =========================
# 👨‍💼 ADMIN EMAIL
# =========================
ADMIN_EMAIL = config(
    'ADMIN_EMAIL'
)




# =========================
# ☁️ CLOUDINARY CONFIG
# =========================

CLOUDINARY_STORAGE = {

    'CLOUD_NAME': config(
        'CLOUDINARY_CLOUD_NAME'
    ),

    'API_KEY': config(
        'CLOUDINARY_API_KEY'
    ),

    'API_SECRET': config(
        'CLOUDINARY_API_SECRET'
    ),
}

# ✅ DEFAULT FILE STORAGE
DEFAULT_FILE_STORAGE = (
    'cloudinary_storage.storage.MediaCloudinaryStorage'
)




