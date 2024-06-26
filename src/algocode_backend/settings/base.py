"""
Django settings for algocode_backend project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

from datetime import timedelta
import environ

env = environ.Env()

# TODO Change the env type: .dev for development. .production for production
ENVIRONMENT_TYPE = ".production"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# this effectively pointing to the SRC dir where the manage.py file is located.
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
# print("root dir: ", ROOT_DIR)

# setup correct env path
env.read_env(Path(str(ROOT_DIR)) / f".envs/{ENVIRONMENT_TYPE}/.django")
env.read_env(Path(str(ROOT_DIR)) / f".envs/{ENVIRONMENT_TYPE}/.postgres")

# apps directory
APP_DIR = ROOT_DIR / "core_apps"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEGUB", False)


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


THIRD_PARTH_APPS = [
    "rest_framework",
    "django_filters",
    "django_countries",
    "phonenumber_field",
    "drf_yasg",
    "corsheaders",
    "djcelery_email",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "rest_framework.authtoken",
    "taggit",
]

LOCAL_APPS = [
    "core_apps.common",
    "core_apps.users",
    "core_apps.profiles",
]

# installed apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTH_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "algocode_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "algocode_backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


#  For Testing.
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": ROOT_DIR / "db.sqlite3",
#     }
# }

# TODO prod Database
#  PostgreSQL DB for User Management. 
# Check docker/production/django/entrypoint for definition. 
DATABASES = {"default": env.db("DATABASE_URL")}


# Password Hashers (argon2-cffi)
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]


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

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

SITE_ID = 1

# admin url
ADMIN_URL = env("ADMIN_URL")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# static files
STATIC_URL = "/staticfiles/"
STATIC_ROOT = str(ROOT_DIR / "staticfiles")

# mediafiles
MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = str(ROOT_DIR / "mediafiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

########################################################

############################ CELERY CONFIG
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTECT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND_MAX_RETRIES = 15
CELERY_TASK_SEND_SENT_EVENT = True

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

############################ Auth and DRF Settings
""" API and AUTH SETTINGS """

#   Rest Framework Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",  # JWTCookieAuthentication
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

# DRF Simple JWT Settings
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=43200),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "SIGNING_KEY": env("SIGNING_KEY"),
    "USER_ID_FIELD": "id",
    "USER_IF_CLAIM": "user_id",
}

# DJ Rest AUTH Settings
REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,  # to get refresh token. also client side JS will be able to access to cookie
    "JWT_AUTH_COOKIE": "algocode-backend-access-token",
    "JWT_AUTH_REFRESH_COOKIE": "algocode-backend-refresh-token",
    "REGISTER_SERIALIZER": "core_apps.users.serializers.CustomRegisterSerializer",
    "JWT_TOKEN_CLAIMS_SERIALIZER": "core_apps.users.serializers.CustomTokenObtainPairSerializer",
}

#  CustomTokenObtainPairSerializer

# Allauth Auth Settings
AUTHENTICATION_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
]


############################ Allauth Settings non email verification
# ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = "email"
# ACCOUNT_EMAIL_VERIFICATION = "none"

# with email verification
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"  # usernam field
ACCOUNT_USERNAME_REQUIRED = True  # username required at registration time.

############################ CORS And AUTH Packages Settings.

# Ff frontend is hosted on different domain, cors is needed. 
# All API endpoint must being with "api" prefix.
CORS_URLS_REGEX = r"^api/.*$"

AUTH_USER_MODEL = "users.CustomUser"

