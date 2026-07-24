"""
Настройки проекта «Робот-Забота».
Каркас рассчитан на расширение: приложения catalog, cart, blog, users
уже подключены как заготовки и не требуют переписывания при росте проекта.
"""
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
# ВНИМАНИЕ: сгенерированный ключ для разработки. Перед продакшеном заменить
# и вынести в переменные окружения.
SECRET_KEY = 'django-insecure-change-me-before-deploy-robot-zabota'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Приложения проекта
    'core',
    'catalog',
    'cart',
    'blog',
    'users',
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
ROOT_URLCONF = 'robot_zabota.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Каждое приложение хранит шаблоны в своей папке templates/<app>/,
        # поэтому глобальную папку DIRS можно оставить пустой и расширять
        # список при необходимости (например, templates/ в корне проекта).
        'DIRS': [BASE_DIR / 'templates'],
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
WSGI_APPLICATION = 'robot_zabota.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Аутентификация ---
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'users:profile'
LOGOUT_REDIRECT_URL = 'core:index'

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True
# --- Static files ---
STATIC_URL = 'static/'
# core/static/core/... подхватывается автоматически через APP_DIRS,
# здесь дополнительно объявляем общую папку static/ в корне проекта
# на случай общих (не привязанных к приложению) ресурсов в будущем.
STATICFILES_DIRS = [
    BASE_DIR / 'static',
] if (BASE_DIR / 'static').exists() else []

# --- Media files (загружаемые изображения роботов) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
