"""
Django settings for stokee_proj project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
# .envに環境変数をかいて、それを読み込むために追記
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g8q-g(o7zftk@o4wa@k=r$(kzyr+fo+*=un+6n_k_^nrjvk+gq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
#デプロイ時はこちらに変更→ALLOWED_HOSTS = ["13.113.139.112", "stokee.techpreneur.jp"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stokee',
    'bootstrap4',
    'mathfilters',
    'user_auth',
    'social_django',
    'stripe',
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

ROOT_URLCONF = 'stokee_proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'django.template.context_processors.media',
            ],
            'builtins':[ 
                'bootstrap4.templatetags.bootstrap4' #bootstrap4の導入
            ],
        },
    },
]

WSGI_APPLICATION = 'stokee_proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    [
        os.path.join(BASE_DIR, "static"),
    ]
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL='/accounts/login'
LOGIN_REDIRECT_URL='/'
LOGOUT_REDIRECT_URL='/'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',

]

SOCIAL_AUTH_TWITTER_KEY = 'NETcQsWMS4hLQnS6hTGgfAdya' # Consumer Key (API Key)
SOCIAL_AUTH_TWITTER_SECRET = 'HXckGBM7c3HD86RZFutLBqxJjSH538vBdhFsXDESgtOJQ7e7a8' #Consumer Secret (API Secret)
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/' # リダイレクトURL


STRIPE_PUBLISHABLE_KEY = 'pk_test_51JSsEIFHEQ8jpLAoaplG1M3ku0hb12xdVDaGSZ1FUth16HXnXtt4LDUlOnbLdukmFRmb5NNEzcP7GJpjlcVmS9PY00kLJWs58V'
STRIPE_SECRET_KEY = 'sk_test_51JSsEIFHEQ8jpLAoL6sjCZ9zwUJQa6rSlx24lUlsWMAywzEYjRIPBT4PTSMkfTAZKUZelnII9NKAxGnrXMPxim2S00Qh2eBpl4'

# 実際にはメールを送らずに、コンソールに表示してくれる
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 実際にメールを送る設定
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# メールの設定
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER") 
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD") 
EMAIL_USE_TLS = True