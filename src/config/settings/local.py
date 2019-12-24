# -*- coding: utf-8 -*-
from config.settings.common import *



# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", default=True)
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="4)i0p15fwh0c+@b+m4qbd4_%ix19)_!xj(o(c(tp+&1c5-wh8$"
)

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# See: https://github.com/julianwachholz/dj-config-url
DATABASES = {
    "default": env.db(
        "DATABASE_URL", default="postgres:///{}".format(PROJECT_NAME.lower())
    )
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# EMAIL
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

# django-debug-toolbar
# ------------------------------------------------------------------------------
# See: http://django-debug-toolbar.readthedocs.io/en/stable/
MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
INSTALLED_APPS += ("debug_toolbar",)

INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}

# django-extensions
# ------------------------------------------------------------------------------
# See: https://django-extensions.readthedocs.io/en/latest/
INSTALLED_APPS += ("django_extensions", "django_gulp",)

ALLOWED_HOSTS = ["*"]
