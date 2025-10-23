import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'b+e10h^38@qa==t!rgom2*)av@rbudw)8rxjfg!dwoc_av2_kt'

# Set DEBUG to False for production
# You can use an environment variable to keep it True for local development
# e.g., DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main_app',
    # 'crispy_forms',
    # 'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware','django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
# settings.py

X_FRAME_OPTIONS = 'ALLOWALL'
# settings.py

X_FRAME_OPTIONS = 'SAMEORIGIN'

  # Allows embedding only from the same origin.


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default Django backend (used for other cases)
    'main_app.backends.EmailBackend',  # Custom backend for email login
]

AUTH_USER_MODEL = 'main_app.CustomUser'


ROOT_URLCONF = 'career_cast.urls'
LOGIN_REDIRECT_URL = '/dashboard/'  # Redirect to the dashboard after login


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
import os

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

WSGI_APPLICATION = 'career_cast.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'Applywizz@123',
#         'HOST': 'db.jittzzsretkoldpyyvjy.supabase.co',
#         'PORT': '5432',
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',  # Use SQLite as the default database
#         'NAME': BASE_DIR / 'db.sqlite3',  # SQLite database file
#     }
# }
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

DATABASES = {
    'default': dj_database_url.parse(
        os.getenv('SUPABASE_DB_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}



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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
# This is where Django will look for static files in development
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# This is where `collectstatic` will gather all static files for production
STATIC_ROOT = BASE_DIR / "staticfiles"

# Configure Media files for Vercel's temporary storage
MEDIA_URL = '/media/'
if DEBUG:
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    MEDIA_ROOT = '/tmp/media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# settings.py

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Outlook Email Configuration
OUTLOOK_TENANT_ID = os.getenv('OUTLOOK_TENANT_ID')
OUTLOOK_CLIENT_ID = os.getenv('OUTLOOK_CLIENT_ID')
OUTLOOK_CLIENT_SECRET = os.getenv('OUTLOOK_CLIENT_SECRET')
OUTLOOK_SENDER_EMAIL = os.getenv('OUTLOOK_SENDER_EMAIL')




# Gemini AI Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Supabase Configuration
# SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://jittzzsretkoldpyyvjy.supabase.co')
# SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImppdHR6enNyZXRrb2xkcHl5dmp5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAzNTYwODEsImV4cCI6MjA3NTkzMjA4MX0.8BEWr9vs21yRk45W0DIfYshpE-0ThNtz9pnEkkKiZz0')

LOGIN_URL = '/auth/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
SENDFILE_BACKEND = 'sendfile.backends.development'

# import os
# from pathlib import Path
# from dotenv import load_dotenv

# load_dotenv()

# BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = 'b+e10h^38@qa==t!rgom2*)av@rbudw)8rxjfg!dwoc_av2_kt'

# DEBUG = True

# ALLOWED_HOSTS = ['*']

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'main_app',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'career_cast.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'career_cast.wsgi.application'

# # SQLite Database (No compilation required)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / "main_app/static"]

# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # Gemini AI Configuration
# GEMINI_API_KEY = 'AIzaSyCXnp4pS7SnWt9aHOyqjtoKBA0kfdi15mg'

# LOGIN_URL = '/auth/'
# LOGIN_REDIRECT_URL = '/dashboard/'
# LOGOUT_REDIRECT_URL = '/'

# AUTH_USER_MODEL = 'main_app.CustomUser'