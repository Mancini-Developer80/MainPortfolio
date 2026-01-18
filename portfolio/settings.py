import os
import sys
import re
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

TESTING = 'test' in sys.argv or 'test_coverage' in sys.argv

# Parse Cloudinary URL and configure
cloudinary_url = os.environ.get('CLOUDINARY_URL', '')
if TESTING:
    # Configurazione dummy per i test: così il test non si blocca mai
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': 'test_cloud',
        'API_KEY': '12345',
        'API_SECRET': 'abcde',
    }
    print("ℹ️ Running in TEST mode: Cloudinary dummy config loaded.")

elif cloudinary_url:
    # Tua logica originale per produzione/sviluppo reale
    match = re.match(r'cloudinary://(\d+):([^@]+)@(.+)', cloudinary_url)
    if match:
        api_key, api_secret, cloud_name = match.groups()
        CLOUDINARY_STORAGE = {
            'CLOUD_NAME': cloud_name,
            'API_KEY': api_key,
            'API_SECRET': api_secret,
        }
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
else:
    # Fallback originale
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY', ''),
        'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
    }

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

#SE CURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "sviluppo-chiave-segreta-1234567890")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "giuseppemancini.dev",
    "www.giuseppemancini.dev",
    "giuseppemancini.onrender.com",
    "portfolio-j2jx.onrender.com",
    "localhost",
    "127.0.0.1",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'ckeditor',
    'blog',
    'pages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Enable WhiteNoise only in production; in dev, Django serves static
    *([] if DEBUG else ['whitenoise.middleware.WhiteNoiseMiddleware']),
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# For production, require SSL
if not DEBUG and 'sqlite' not in DATABASES['default']['ENGINE']:
    DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'css',
    BASE_DIR / 'js',
    BASE_DIR / 'img',
    BASE_DIR / 'resume',
    
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
if DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    WHITENOISE_USE_FINDERS = True
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKEditor Configuration
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['Link', 'Unlink', 'Image'],
            ['Format', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['CodeSnippet'],
            ['RemoveFormat', 'Source']
        ],
        'height': 400,
        'width': '100%',
        'extraPlugins': ','.join(['codesnippet']),
    }
}

CKEDITOR_UPLOAD_PATH = "uploads/"

# Email Configuration
# In development (DEBUG=True), emails are printed to console
# In production (DEBUG=False), use SMTP with Zoho EU
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtppro.zoho.eu'
    EMAIL_PORT = 465  
    EMAIL_USE_SSL = True  
    EMAIL_USE_TLS = False 
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'info@giuseppemancini.dev')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    EMAIL_TIMEOUT = 10

# Email addresses - must match the authenticated email
DEFAULT_FROM_EMAIL = 'info@giuseppemancini.dev'
CONTACT_EMAIL = 'info@giuseppemancini.dev'




# Cloudinary configuration using CLOUDINARY_URL
# Format: cloudinary://api_key:api_secret@cloud_name
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')

if not DEBUG and CLOUDINARY_URL:
    # django-cloudinary-storage will automatically use CLOUDINARY_URL
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # In sviluppo locale o se Cloudinary non è configurato, usa lo storage locale
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
