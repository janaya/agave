# Django settings for agave_prj project.
import os.path
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Override DATABASES with your custom databases in local_settings.py, e.g.:
#DATABASES = {
#    'default': {
#        'NAME': 'dbname',
#        'ENGINE': 'django.db.backends.mysql',
#        'USER': 'dbuser',
#        'PASSWORD': 'dbpw'
#    },
#    'instances': {
#        'NAME': 'dbname2',
#        'ENGINE': 'django.db.backends.mysql',
#        'USER': 'dbuser2',
#        'PASSWORD': 'dbpw2'
#    }
#}



# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Fix up agave imports here. Wwe ship it a couple of directories up.
#sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_ROOT, '../../')))
sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_ROOT, '../')))
#sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_ROOT, './')))
#sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_ROOT, '../agave')))

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media')

STATIC_ROOT = os.path.join(MEDIA_ROOT, 'static')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

STATIC_URL = '/site_media/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3nxn=*g8ob3zg$30qj2ky4fx91r)x2s=zae-n5mc_j^l4c_sa@'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)
#TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
#    "django.core.context_processors.debug",
#    "django.core.context_processors.i18n",
#    "django.contrib.staticfiles.context_processors.staticfiles",
#    "django.contrib.messages.context_processors.messages"
#)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'agave_prj.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),

)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
#    'south',
#    'fpggsna',
#    'crel',
#    'graphs',
#    'agave.,
    'agave',
#    'django_extensions',
    'django.contrib.markup',
)

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
)

CSV_OUTPUT_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, '../output_csv'))

# Override ZEMANTA_KEY with your custom API KEY in local_settings.py, e.g.
ZEMANTA_KEY = 'key1234'

SPARQL_ENDPOINT_LOCAL = False
#SPARQL_ENDPOINT_LOCAL = True

# Override the Social Network site database in case of importing data from a SN
#SN_DBSERVER = 'localhost'
#SN_DBNAME = 'dbname'
#SN_DBUSER = 'dbuser'
#SN_DBPW = 'dbpw'

#SN_SITE_PROFILES_URL =

if DEBUG:
#    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
#    INTERNAL_IPS = ('127.0.0.1',)
#    INSTALLED_APPS += ('debug_toolbar',)
    pass
else:
    MIDDLEWARE_CLASSES += ('django.middleware.cache.UpdateCacheMiddleware',
                           'django.middleware.common.CommonMiddleware',
                           'django.middleware.cache.FetchFromCacheMiddleware',)

    CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
#    CACHE_MIDDLEWARE_SECONDS
#    CACHE_MIDDLEWARE_KEY_PREFIX
try:
    from local_settings import *
except ImportError:
    pass
