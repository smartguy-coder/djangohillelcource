import os
from pathlib import Path
import environ

env = environ.Env()  # Ініціалізація об'єкту env
env.read_env()  # читає файл .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-d+!tp-mk6vch*o7re$lh1j8ihfcu+wupl1433i-nmdru$rp5&c"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', 'https://fbf7-188-130-177-189.ngrok-free.app']
CSRF_TRUSTED_ORIGINS = ['https://fbf7-188-130-177-189.ngrok-free.app']

import sentry_sdk

sentry_sdk.init(
    dsn="https://783bd5e7e080f74e2a5b70638f15bf37@o4505229726318592.ingest.us.sentry.io/4507760919511040",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'retail',
    'debug_toolbar',
    'silk',
    'cacheops',
    'rest_framework',
    'drf_spectacular',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'middleware.sql_middleware.QueryCountMiddleware',
    # 'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = "shop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "shop.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.str("POSTGRES_HOST"),
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "PORT": env.int("POSTGRES_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = [
    '127.0.0.1',
]

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#         },
#         "file": {
#             "class": "logging.FileHandler",
#             "filename": "debug.log",
#         },
#         "filesql": {
#             "class": "logging.FileHandler",
#             "filename": "debug_sql.log",
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console', 'file'],
#             'level': 'DEBUG'
#
#         },
#         "middleware.sql_middleware": {
#             "handlers": ["console", 'filesql'],
#             "level": "DEBUG",
#             "propagate": False,
#         },
#     },
# }

STRIPE_KEY = 'sk_test_51PeNkLRvJkC5nYiu1Zs3yfGgP5WDXcfKoiTYfKOZmlqJohLgZYdiTFRs6CicWZiBqviNyhjrGmAnNGeDxCeondJU00wmi46jWK'

# CACHING
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/",
        "KEY_PREFIX": "imdb",
        "TIMEOUT": 60 * 15,  # in seconds: 60 * 15 (15 minutes)
    }
}

CACHEOPS_ENABLED = True
CACHEOPS_REDIS = {
    'host': 'redis',  # redis-server is on same machine
    'port': 6379,        # default redis port
    'db': 1,             # SELECT non-default redis database
                         # using separate redis db or redis instance
                         # is highly recommended

    'socket_timeout': 3,   # connection timeout in seconds, optional
}
CACHEOPS = {
    # recommended by authors
    'auth.user': {'ops': 'get', 'timeout': 15},
    'auth.*': {'ops': ('fetch', 'get'), 'timeout': 15},
    'auth.permission': {'ops': 'all', 'timeout': 15},

    # our models
    'retail.producer': {'ops': 'all', 'timeout': 15},
    'retail.product': {'ops': 'all', 'timeout': 15},
    'retail.productcategory': {'ops': 'all', 'timeout': 15},
}


REST_FRAMEWORK = {
    # YOUR SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Hillel Django course Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}