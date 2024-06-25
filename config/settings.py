from datetime import timedelta
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i*62ti7vrwom)*%^s_2g4q%)uyzh8%xz#4ks45cu4i%v&u(c+)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['172.20.16.3', '*', '127.0.0.1']

# Application definition

INSTALLED_APPS = [

    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'django_extensions',
    'drf_yasg',
    'corsheaders',
    # 'django_elasticsearch_dsl',
    # 'django_elasticsearch_dsl_drf',
    'django_filters',
    'rosetta',

    'apps.outside',
    # 'apps.PaYme.apps.PaymentConfig',
    'apps.user_profile',
    'apps.products',
    'apps.cart',
    'apps.checkout',
    'apps.dashboard_api',
    # 'apps.search',
    # 'apps.payme',

    'apps.paycomuz',

    'ckeditor',
    'ckeditor_uploader',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
                'django.template.context_processors.media',

            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=31),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'giper_db1',
#         'USER': 'giper_us1',
#         'PASSWORD': 'giper_pass1',
#         'HOST': 'localhost',
#         'PORT': 5432,
#     }
# }

AUTH_USER_MODEL = 'user_profile.User'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru'

LANGUAGES = (
    ('uz', _('Uzbek')),
    ('ru', _('Russian')),
    ('en', _('English')),
)

LOCALE_PATHS = BASE_DIR / 'locale',

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ORIGIN_ALLOW_ALL = True

# **********************************   Django JWT Configration    **********************************
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),

}


ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200',
        'timeout': 60,
    },
}

ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = 'django_elasticsearch_dsl.signals.RealTimeSignalProcessor'

CKEDITOR_UPLOAD_PATH = 'ck-uploads/'
CKEDITOR_ALLOW_NONIMAGE_FILES = False

JAZZMIN_SETTINGS = {
    "site_header": "Gipermart.uz", "site_brand": "Gipermart.uz",
    "site_logo": "logo3.png", "login_logo": "logoo.svg", "login_logo_dark": None,
    "site_icon": "logoo.svg", "welcome_sign": "Gipermart.uz", "copyright": "Gipermart.uz", "user_avatar": None,
    "show_ui_builder": True, "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Главная", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Продукты", "url": "/admin/products/newproductmodel/"},
        {"name": "Тип продуктов", "url": "/admin/products/producttype/"},
        {"name": "Бренды", "url": "/admin/outside/brand/"},
        {"name": "Категории", "url": "/admin/products/category/"},
        {"name": "Все медии", "url": "/admin/products/allmedia/"},
        # {"name": "Продукт атрибуты", "url": "/admin/products/productattributevalue/"},
        # {"name": "Продукт атрибуты2", "url": "/admin/products/productattributevalues/"},

    ], "usermenu_links": [
        {"model": "auth.user"}
    ], "show_sidebar": True, "navigation_expanded": True, "hide_apps": [], "hide_models": [],
    "order_with_respect_to": ["outside", "checkout", "user_profile", "products", "cart", "works"],
    "related_modal_active": False, "custom_css": None, "custom_js": None,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"}
}

# PAYME: dict = {
#     'PAYME_ID': 'payme-id',
#     'PAYME_KEY': 'payme-key',
#     'PAYME_URL': 'payme-checkout-url',
#     'PAYME_CALL_BACK_URL': 'your-callback-url', # merchant api callback url
#     'PAYME_MIN_AMOUNT': 'payme-min-amount', # integer field
#     'PAYME_ACCOUNT': 'order-id',
# }


# PAYME: dict = {
#     'PAYME_ID': '6221f9548dccd302156b739f', # merchant_id
#     'PAYME_KEY': '@Ez32Kxc2s7PK03q0HQQ&inf#IH5aVutEh&o', # merchant_key
#     'PAYME_URL': 'https://test.paycom.uz',
#     'PAYME_CALL_BACK_URL': 'https://api.gipermart.uz/paycom/', # merchant api callback url
#     'PAYME_MIN_AMOUNT': '1', # integer field
#     'PAYME_ACCOUNT': 'payment_id',  # payme kassa rekviziti
# }


PAYCOM_SETTINGS = {
    "KASSA_ID": "6221f9548dccd302156b739f",
    # "TOKEN": "6221f9548dccd302156b739f",  # token
    "PHONE": "+998901234567",
    "SECRET_KEY": "0UyzTv?teb1IqR486Nt1&q06t?F@4TqgQC5p",  # password
    "ACCOUNTS": {
        "KEY": "payment_id"
    }
}


PAYMENT_UNITS = 241092  # Misol uchun

VAT_PERCENTAGE = 12

PACKAGE_CODE = "08415001001000000"
