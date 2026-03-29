import os
import sys
import re
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pathlib import Path
import environ

# --- 1. PATHS & ENV CONFIG ---
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
# Carica il file .env se esiste
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

TESTING = 'test' in sys.argv or 'test_coverage' in sys.argv

# --- 2. SECURITY CONFIG ---
# Ripristiniamo la logica dinamica per Cloud Run
DEBUG = env.bool('DEBUG', default=False) 

# AGGIUNGI QUESTE RIGHE DI STAMPA PER VEDERE COSA SUCCEDE NEL TERMINALE
print("--- DIAGNOSTICA AVVIO ---")
print(f"Directory di base: {BASE_DIR}")
print(f"File .env trovato: {os.path.exists(os.path.join(BASE_DIR, '.env'))}")
print(f"Valore DEBUG caricato: {DEBUG}")
print("--------------------------")

# Solo per debug nel terminale locale, puoi decommentare la riga sotto se serve
# print(f"--- DEBUG MODE: {DEBUG} ---")

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-local-dev-key-12345")

# --- 3. DOMAIN CONFIG (NO RENDER) ---
ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    'giuseppemancini.dev', 
    'www.giuseppemancini.dev',
    '.run.app', 
]

env_hosts = os.environ.get("ALLOWED_HOSTS", "").split(",")
if env_hosts and env_hosts[0]:
    ALLOWED_HOSTS.extend(env_hosts)

CSRF_TRUSTED_ORIGINS = [
    'https://giuseppemancini.dev',
    'https://www.giuseppemancini.dev',
    'https://*.run.app'
]

# --- 4. SSL & PROXY LOGIC ---
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    # Disattiva tutto in locale per evitare il blocco che stai vedendo
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# --- 5. APP & MIDDLEWARE ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'cloudinary_storage',
    'ckeditor',
    'blog',
    'pages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', # REINSERITO
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

# --- 6. DATABASE ---
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

if not DEBUG and 'sqlite' not in DATABASES['default']['ENGINE']:
    DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}

# --- 7. STATIC & MEDIA ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'css', BASE_DIR / 'js', BASE_DIR / 'img', BASE_DIR / 'resume']
STATIC_ROOT = BASE_DIR / 'staticfiles'

if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Cloudinary
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')
if not DEBUG and CLOUDINARY_URL:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# --- 8. EMAIL (ZOHO EU) ---
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtppro.zoho.eu'
    EMAIL_PORT = 465
    EMAIL_USE_SSL = True
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'info@giuseppemancini.dev')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = 'info@giuseppemancini.dev'

# --- 9. EXTRA (CKEDITOR & TURNSTILE) ---
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

TURNSTILE_SITE_KEY = os.environ.get('TURNSTILE_SITE_KEY', '')
TURNSTILE_SECRET_KEY = os.environ.get('TURNSTILE_SECRET_KEY', '')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'