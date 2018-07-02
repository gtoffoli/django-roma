# -*- coding: utf-8 -*-

# Django settings for roma project.

from roma.private import *

import sys, django

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(__file__)
PARENT_ROOT = os.path.dirname(PROJECT_ROOT)
sys.path.insert(0, PARENT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))  # vedi https://pypi.python.org/pypi/django-richtext-blog
SEARCH_BACKEND = None

if PRODUCTION:
    DEBUG = False
    DEBUG_TOOLBAR = False
    USE_HAYSTACK = True
    SEARCH_BACKEND = "whoosh"
else:
    DEBUG = True
    DEBUG_TOOLBAR = False
    USE_HAYSTACK = True
    SEARCH_BACKEND = "whoosh"
    # MMR old version - TEMPLATE_STRING_IF_INVALID = '%s'
# TEMPLATE_DEBUG = DEBUG

SHOW_MAPS = True
MAX_POIS = 50
srid_OSM = 3857

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
TIME_ZONE = 'Europe/Rome'
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'it'
# If you set this to False, Django will make some optimizations so as not to load the internationalization machinery.
USE_I18N = True
# If you set this to False, Django will not format dates, numbers and alendars according to the current locale.
USE_L10N = True
# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

ONLINE_DOMAIN = 'www.romapaese.it'
SITE_ID = 1
SITE_NAME = 'RomaPaese'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# MEDIA_ROOT = ''
MEDIA_ROOT = os.path.join(PARENT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a # trailing slash.
MEDIA_URL = '/media/' # vedi https://pypi.python.org/pypi/django-richtext-blog
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
STATIC_ROOT = PARENT_ROOT+'/static/'
# STATIC_ROOT = os.path.join(PROJECT_HOME, 'static') # vedi https://pypi.python.org/pypi/django-richtext-blog
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
# ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/' # vedi https://pypi.python.org/pypi/django-richtext-blog

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #sys.platform.count('linux') and '/home/ubuntu/django/roma/roma/static' or '/django/roma/roma/static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'roma.urls'

LOGIN_REDIRECT_URL = '/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
             os.path.join(PROJECT_ROOT, 'templates'),
             ),
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug', # MMR added
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.csrf',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                # MMR temporaneamente disattivato - 'richtext_blog.context_processors.blog_global',
                'roma.context_processors.context_processor',
                # "allauth.account.context_processors.account",
                # "allauth.socialaccount.context_processors.socialaccount",
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'bootstrap3',
    'captcha',
    'dal',
    'dal_select2',
    'dal_queryset_sequence',
    'dal_select2_queryset_sequence',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'django.contrib.gis',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.openid',
    # 'allauth.socialaccount.providers.twitter',
    # MMR 'richtext_blog',
    'menu',
    # 'paypal.standard.ipn',
    'datatrans',
    'rest_framework',
    'django_filters',
    # MMR 'fairvillage',
    'roma',
    'pois',
    'django_user_agents',
    'django_cleanup',
)
if DEBUG and DEBUG_TOOLBAR:
    INSTALLED_APPS = list(INSTALLED_APPS) + ['debug_toolbar']
if USE_HAYSTACK:
    INSTALLED_APPS = ['haystack'] + list(INSTALLED_APPS)

# Cache backend is optional, but recommended to speed up user agent parsing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'custom': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PARENT_ROOT, 'cache/base'),
        'TIMEOUT': 24*60*60,
        'MAX_ENTRIES': 10,
    },
    'pois': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PARENT_ROOT, 'cache/pois'),
        'TIMEOUT': 7*24*60*60,
        'MAX_ENTRIES': 1000,
    },
    'themes': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PARENT_ROOT, 'cache/themes'),
        'TIMEOUT': 7*24*60*60,
        'MAX_ENTRIES': 50,
    },
    'categories': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PARENT_ROOT, 'cache/categories'),
        'TIMEOUT': 7*24*60*60,
        'MAX_ENTRIES': 500,
    },
    'zones': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PARENT_ROOT, 'cache/zones'),
        'TIMEOUT': 7*24*60*60,
        'MAX_ENTRIES': 500,
    },
    'zonemaps': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PARENT_ROOT, 'cache/zonemaps'),
        'TIMEOUT': 7*24*60*60,
        'MAX_ENTRIES': 500,
    },
    'catzones': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PARENT_ROOT, 'cache/catzones'),
        'TIMEOUT': 7*24*60*60,
        'MAX_ENTRIES': 2000,
    },
    'streets': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PARENT_ROOT, 'cache/streets'),
        'TIMEOUT': 7*24*60*60,
        'MAX_ENTRIES': 1000,
    },
}

# 20170928 MMR added - None -> disable caching -
USER_AGENTS_CACHE = None #'default'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Silence SuspiciousOperation.DisallowedHost exception ('Invalid
        # HTTP_HOST' header messages). Set the handler to 'null' so we don't
        # get those annoying emails.
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    }
}

POI_CATEGORIES = (
    '02030000', # Servizi per l'edilizia
    '02050000', # Servizi per l'impiego e l'orientamento
    '02110000', # Servizi di gestione della proprietà immobiliare
    '03170000', # Attrazioni storiche e culturali
    '04240000', # Complessi sportivi
    '04250000', # Luoghi d'incontro, stadi, cineteatri
    '05260000', # Cura degli animali
    '05280000', # Professionisti e istituzioni della sanità
    '05290000', # Servizi di supporto alla sanità
    '05300000', # Privato sociale (nuovo)
    '05310000', # Formazione primaria, secondaria e terziaria
    '05320000', # Formazione ricreativa e vocazionale
    '06330000', # Governo centrale e locale
    '06340000', # Infrastrutture e impianti
    '06350000', # Organizzazioni
    '09480000', # Casa, ufficio, tempo libero e giardinaggio
)

LANGUAGES = (
  ('it', 'Italiano'),
  ('en', 'English'),
  ('es', 'Espanol'),
)

# django-localeurl settings
PREFIX_DEFAULT_LOCALE = False

"""
MMR 20181701
ROSETTA_MESSAGES_PER_PAGE = 20
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = False
ROSETTA_MESSAGES_SOURCE_LANGUAGE_CODE = 'en'
ROSETTA_MESSAGES_SOURCE_LANGUAGE_NAME = 'English'
ROSETTA_STORAGE_CLASS = 'rosetta.storage.SessionRosettaStorage'
"""

# TinyMCE settings
TINYMCE_COMPRESSOR = False

TINYMCE_DEFAULT_CONFIG = {
    'schema': "html5",
    'resize' : "both",
    'height': 350,
    'branding': False,
    # 'plugins': "advlist charmap textcolor colorpicker table link anchor image media visualblocks code fullscreen preview",
    'plugins': "paste lists advlist charmap textcolor colorpicker table link anchor image visualblocks code fullscreen preview",
    # 'toolbar': 'undo redo | formatselect bold italic underline | alignleft aligncenter alignright alignjustify | forecolor backcolor subscript superscript charmap | bullist numlist outdent indent | table link unlink anchor image media | cut copy paste removeformat | visualblocks code fullscreen preview',
    'toolbar': 'undo redo | formatselect styleselect bold italic underline | alignleft aligncenter alignright alignjustify | forecolor backcolor subscript superscript charmap | bullist numlist outdent indent | table link unlink anchor image | cut copy paste removeformat | visualblocks code fullscreen preview',
    'content_css' : os.path.join(STATIC_URL,"tinymce/mycontent.css"),
    'style_formats': [
      {'title': '10px', 'inline': 'span', 'styles': {'font-size': '10px'}},
      {'title': '11px', 'inline': 'span', 'styles': {'font-size': '11px'}},
      {'title': '12px', 'inline': 'span', 'styles': {'font-size': '12px'}},
      {'title': '13px', 'inline': 'span', 'styles': {'font-size': '13px'}},
      {'title': '14px', 'inline': 'span', 'styles': {'font-size': '14px'}},
      {'title': '15px', 'inline': 'span', 'styles': {'font-size': '15px'}},
      {'title': '16px', 'inline': 'span', 'styles': {'font-size': '16px'}},
      {'title': '17px', 'inline': 'span', 'styles': {'font-size': '17px'}},
      {'title': '18px', 'inline': 'span', 'styles': {'font-size': '18px'}},
      {'title': 'clear floats', 'block': 'div', 'styles': {'clear': 'both'}},
    ],
    'plugin_preview_width' : 800,
    'plugin_preview_height' : 600,
    'advlist_class_list' : [
        {'title': 'select', 'value': ''},
        {'title': 'image responsive', 'value': 'img-responsive-basic center-block'},
        {'title': 'image responsive left', 'value': 'img-responsive-basic pull-left'},
        {'title': 'image responsive right', 'value': 'img-responsive-basic pull-right'}],
    'image_advtab' : True,
    'image_caption': False,
    'image_class_list' : [
        {'title': 'select', 'value': ''},
        {'title': 'image responsive', 'value': 'img-responsive-basic center-block'},
        {'title': 'image responsive left', 'value': 'img-responsive-basic pull-left marginR10'},
        {'title': 'image responsive right', 'value': 'img-responsive-basic pull-right marginL10'}],
    'paste_data_images': True,
    'table_class_list': [
        {'title': 'select', 'value': ''},
        {'title': 'table responsive', 'value': 'table-responsive'},
        {'title': 'table responsive width 100%', 'value': 'table-responsive width-full'},],
    'file_browser_callback_types': 'image',
    'paste_as_text': True,
    # URL settings
    # 'convert_urls' : False,
    'relative_urls' : False,
}
"""
MMR 20181701
# Filebrowser settings
FILEBROWSER_DIRECTORY = 'uploads/'
"""

"""
# richtext_blog settings
SLUGS_EDITABLE = True
SITE_DESCRIPTION = 'Blog di prova'
"""

# simple-captcha settings
CAPTCHA_LETTER_ROTATION = (-20, 20) # (-35, 35)
CAPTCHA_BACKGROUND_COLOR = '#ffffff' # '#ffffff'
CAPTCHA_FOREGROUND_COLOR = '#800000' # '#001100'
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',) # ('captcha.helpers.noise_arcs', 'captcha.helpers.noise_dots',)
CAPTCHA_LENGTH = 5 # 4  # Chars

# django-paypal settings
# PAYPAL_RECEIVER_EMAIL = "toffoli@linkroma.it"

if sys.platform.count('linux'):
    DEFAULT_FROM_EMAIL = 'RomaPaese <noreply@linkroma.it>'
else:
    DEFAULT_FROM_EMAIL = 'RomaPaese <noreply@localhost>'

ACCOUNT_AUTHENTICATION_METHOD = "email" # "username"
ACCOUNT_USERNAME_REQUIRED = False # True
ACCOUNT_EMAIL_REQUIRED = True # False
ACCOUNT_EMAIL_VERIFICATION = "mandatory" # "optional"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none" # ACCOUNT_EMAIL_VERIFICATION

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'VERSION': 'v2.12',
    }
}

INTERNAL_IPS = ('127.0.0.1',)

if SEARCH_BACKEND == 'whoosh':
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(PARENT_ROOT, 'whoosh_index'),
        },
    }
elif SEARCH_BACKEND == 'solr':
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
            'URL': 'http://localhost:8080/solr',
        },
    }

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
}
"""
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
"""
POITYPE_SLUGS = []

DATATRANS_TRANSLATE_MAP = {
    'flatpage': ('%s', 'url', 'title', 'roma.forms.FlatPageForm',),
    'poi': ('/risorsa/%s/', 'slug', 'name', 'pois.forms.PoiForm',),
}

VERSION_GOOGLE_MAPS = '3.32'

