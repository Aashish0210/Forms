from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import os
# In settings.py
from django.contrib.messages import constants as message_constants

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Optionally customize message levels
MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email settings
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=465, cast=int)  # Port 465 is for SSL
EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=True, cast=bool)  # SSL for port 465
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, cast=bool)  # TLS should be False for SSL
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="example@gmail.com")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="1234")
EMAIL_FROM_ADDRESS = config("EMAIL_FROM_ADDRESS", default="supercompiler0210@gmail.com")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="dnj3n4ri03jejbfhebhf314392")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'phonenumber_field',
    'usermanagement',
    'jazzmin',
    "django_filters",
    "import_export",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'UserManagementSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'UserManagementSystem.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_USER_MODEL = 'usermanagement.User'  # Replace with your app's model if needed

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Session settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Expire session when the browser is closed
SESSION_COOKIE_AGE = 900  # Session expiry time in seconds (15 minutes)
SESSION_SAVE_EVERY_REQUEST = True  # Save session data on every request
SESSION_COOKIE_SECURE = True  # Ensure the session cookie is transmitted over HTTPS only (for production)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Use database-backed sessions

# Login settings
LOGIN_URL = '/login/'  # Redirect to login page if the user is not authenticated
LOGOUT_REDIRECT_URL = '/'
  # Redirect to home page after logout

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
