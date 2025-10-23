import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-secret')
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

# ✅ Always allow vercel domains and localhost
ALLOWED_HOSTS = ['.vercel.app', '127.0.0.1', 'localhost']

# ---------------- DATABASE ---------------- #
# You can set SUPABASE_DB_URL in Vercel as:
# postgresql://postgres:<PASSWORD>@<HOST>:5432/postgres

SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")
if SUPABASE_DB_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            SUPABASE_DB_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ---------------- STATIC FILES ---------------- #
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------- MEDIA FILES ---------------- #
MEDIA_URL = '/media/'
if os.environ.get("VERCEL"):
    MEDIA_ROOT = "/tmp/media"  # ✅ Vercel writable dir
else:
    MEDIA_ROOT = BASE_DIR / "media"

# ---------------- OPENAI + OUTLOOK ---------------- #
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OUTLOOK_TENANT_ID = os.getenv("OUTLOOK_TENANT_ID")
OUTLOOK_CLIENT_ID = os.getenv("OUTLOOK_CLIENT_ID")
OUTLOOK_CLIENT_SECRET = os.getenv("OUTLOOK_CLIENT_SECRET")
OUTLOOK_SENDER_EMAIL = os.getenv("OUTLOOK_SENDER_EMAIL")

# ---------------- AUTH ---------------- #
AUTH_USER_MODEL = 'main_app.CustomUser'
LOGIN_URL = '/auth/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
