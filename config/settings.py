from typing import Optional
from pathlib import Path
import os

# -----------------------------------------------------------------------------
# Base
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Мини-парсер .env (без зависимостей).
# Загружает пары KEY=VALUE в os.environ, если файл существует.
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip())

def env(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(name, default)
    """Короткий помощник для чтения переменных окружения."""


# -----------------------------------------------------------------------------
# Security
# -----------------------------------------------------------------------------
SECRET_KEY = env("SECRET_KEY", "dev-only-change-me")  # в .env заменить настоящим ключом
DEBUG = env("DEBUG", "true").lower() == "true"

# Список хостов через запятую: "127.0.0.1,localhost,example.com"
ALLOWED_HOSTS = [h.strip() for h in env("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]

# Полные origin-ы через запятую: "https://example.com,https://sub.example.com"
_csrf = [o.strip() for o in env("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]
CSRF_TRUSTED_ORIGINS = _csrf if _csrf else []

# -----------------------------------------------------------------------------
# Applications
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "enrollments",

    # Third-party
    "rest_framework",

    # Local apps
    "courses",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# -----------------------------------------------------------------------------
# Templates
# -----------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # при необходимости создай папку templates/
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

# -----------------------------------------------------------------------------
# Database
# По умолчанию SQLite. Для Postgres задайте:
# DB_ENGINE=postgres, DB_NAME=..., DB_USER=..., DB_PASSWORD=..., DB_HOST=..., DB_PORT=5432
# -----------------------------------------------------------------------------
DB_ENGINE = env("DB_ENGINE", "sqlite").lower()

if DB_ENGINE == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
elif DB_ENGINE == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME", ""),
            "USER": env("DB_USER", ""),
            "PASSWORD": env("DB_PASSWORD", ""),
            "HOST": env("DB_HOST", "localhost"),
            "PORT": env("DB_PORT", "5432"),
        }
    }
else:
    raise RuntimeError(f"Unsupported DB_ENGINE: {DB_ENGINE}")

# -----------------------------------------------------------------------------
# Password validation
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------------------------------------
# Internationalization / Time
# -----------------------------------------------------------------------------
LANGUAGE_CODE = "en-gb"  # можно поменять на 'ru-ru'
TIME_ZONE = env("TIME_ZONE", "Europe/London")
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------------------
# Static & Media
# -----------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"   # сюда кладёт collectstatic (игнорим в git)
# Если нужны дополнительные локальные статические файлы:
# STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"          # для загружаемых пользователями файлов

# -----------------------------------------------------------------------------
# Django REST Framework
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        # Включить Browsable API только при DEBUG:
        *(["rest_framework.renderers.BrowsableAPIRenderer"] if DEBUG else []),
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
}

# -----------------------------------------------------------------------------
# Logging (к консоли)
# -----------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO" if not DEBUG else "DEBUG",
    },
}

# -----------------------------------------------------------------------------
# Auto field
# -----------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------------------------------------------------
# Security hints for production (включайте при DEBUG=False)
# -----------------------------------------------------------------------------
if not DEBUG:
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30  # 30 дней
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
