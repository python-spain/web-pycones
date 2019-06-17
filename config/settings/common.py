# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from os.path import basename, join
from sys import path

import environ
import markdown


# PATH CONFIGURATION
# ------------------------------------------------------------------------------
# environ.Path value to the django repo directory:
ROOT_DIR = environ.Path(__file__) - 3

# environ.Path value to the project directory:
APPS_DIR = ROOT_DIR.path("pycones")

# Absolute filesystem path to the config directory:
CONFIG_ROOT = str(APPS_DIR.path("config"))

# Absolute filesystem path to the project directory:
PROJECT_ROOT = str(APPS_DIR)

# Absolute filesystem path to the django repo directory:
DJANGO_ROOT = str(ROOT_DIR)

# Project folder:
PROJECT_FOLDER = basename(PROJECT_ROOT)

# Project name:
PROJECT_NAME = basename(PROJECT_ROOT).capitalize()

# Project domain:
PROJECT_DOMAIN = "%s.com" % PROJECT_NAME.lower()

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(CONFIG_ROOT)

env = environ.Env()
env.read_env(join(DJANGO_ROOT, ".env"))
# DEBUG CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
API_DEBUG = DEBUG

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (("APSL", "devops@apsl.net"),)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = "UTC"

# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "es"
ugettext = lambda s: s
LANGUAGES = (
    ("es", ugettext("Español")),
    #    ("ca", ugettext("Catalán")),
    #    ("gl", ugettext("Gallego")),
    #    ("eu", ugettext("Euskera")),
    ("en", ugettext("English")),
)
LOCALE_PATHS = (str(APPS_DIR.path("locale")),)

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

# EMAIL
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="{} <noreply@{}>".format(PROJECT_NAME, PROJECT_DOMAIN),
)
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX", default="[{}] ".format(PROJECT_NAME)
)
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

# MESSAGES
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/1.11/ref/contrib/messages/
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/templates/
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                "pycones.utils.context_processors.project_settings",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "string_if_invalid": "NULL",
        },
    }
]

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    # Useful template tags:
    "django.contrib.humanize",
    # Admin
    "modeltranslation",
    "django.contrib.admin",
)
THIRD_PARTY_APPS = tuple()

# Apps specific for this project go here.
LOCAL_APPS = (
    "pycones.utils",
    "pycones.users",
    "pycones.blog",
    "pycones.sponsorships",
    "pycones.proposals",
    "pycones.reviewers",
    "pycones.speakers",
    "pycones.schedules",
    "pycones.jobboard",
    "pycones.contentchunk",
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR("media"))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR("public"))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (str(APPS_DIR.path("static")),)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# See: https://github.com/julianwachholz/dj-config-url
DATABASES = {
    "default": env.db(
        "DATABASE_URL", default="postgis:///{}".format(PROJECT_NAME.lower())
    )
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = "users.User"

# PASSWORD VALIDATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ADMIN SITE
# ------------------------------------------------------------------------------
# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r"^admin/"

# MARKUP FIELD CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://github.com/jamesturk/django-markupfield/
INSTALLED_APPS += ("markupfield",)
MARKUP_FIELD_TYPES = (("markdown", markdown.markdown),)

# TAGGIT SETTINGS
# ------------------------------------------------------------------------------
# See: https://django-taggit.readthedocs.io/en/latest/
INSTALLED_APPS += ("taggit", "taggit_autosuggest")
TAGGIT_CASE_INSENSITIVE = True

# DJANGO MODELTRANSLATION
# ------------------------------------------------------------------------------
# See: http://django-modeltranslation.readthedocs.io/en/latest/index.html
MODELTRANSLATION_DEFAULT_LANGUAGE = "es"
MODELTRANSLATION_FALLBACK_LANGUAGES = ("es", "en")
MODELTRANSLATION_LANGUAGES = ("es", "en")

# PROJECT CUSTOM SETTINGS
# ------------------------------------------------------------------------------
# This values may vary during the life of the conference.
LANDING_GLOBAL_REDIRECT = env.bool("PYCONES_LANDING_GLOBAL_REDIRECT", default=False)
CONFERENCE_TITLE = "PyConES 2019"
CONTACT_EMAIL = "contact@2019.es.pycon.org"
SPONSORS_EMAIL = "contact@2019.es.pycon.org"
CFP_EMAIL = "contact@2019.es.pycon.org"
PRESS_EMAIL = "contact@2019.es.pycon.org"
FINANCIAL_AID_EMAIL = "contact+finaid@2019.es.pycon.org"

# DJANGO SIMPLE OPTIONS
# ------------------------------------------------------------------------------
# See: https://github.com/marcosgabarda/django-simple-options
INSTALLED_APPS += ("options",)
TEMPLATES[0]["OPTIONS"]["context_processors"] += ["options.context_processors.options"]
CONFIGURATION_DEFAULT_OPTIONS = {
    "submit_proposal_post_pk": {
        "value": 0,
        "type": 1,
        "public_name": "Value for the post ID with proposal instructions",
    },
    "submit_proposal_opened": {
        "value": 0,
        "type": 1,
        "public_name": "Set the submit of proposals opened",
    },
    "edit_proposals_allowed": {
        "value": 0,
        "type": 1,
        "public_name": "Set the edition of proposals",
    },
    "relevance_weights": {"value": 1.0, "type": 2, "public_name": "Relevance weights"},
    "interest_weights": {"value": 1.0, "type": 2, "public_name": "Interest weights"},
    "newness_weights": {"value": 1.0, "type": 2, "public_name": "Newness weights"},
    "schedule_opened": {
        "value": 0,
        "type": 1,
        "public_name": "Makes the schedule visible",
    },
    "attendees_zone_activated": {
        "value": 0,
        "type": 1,
        "public_name": "Activates the attendees zone",
    },
    "sold_out": {"value": 0, "type": 1, "public_name": "Sets tickets as sold out"},
    "activated_tickets_sale_button": {
        "value": 0,
        "type": 1,
        "public_name": "Activates button for selling tickets",
    },
    "activated_tickets_sale_page": {
        "value": 0,
        "type": 1,
        "public_name": "Activates page for selling tickets",
    },
    "activate_reviews": {"value": 0, "type": 1, "public_name": "Activate reviews"},
}

