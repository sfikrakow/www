from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*q^o$d!6el@6vg-9ylnna5-t+@yvnraeyg5t6&!x=$5mh=x4%^'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

OIDC_ADMIN_ROLE = 'sfi'

MIDDLEWARE += [
    'livereload.middleware.LiveReloadScript',
]

try:
    from .local import *
except ImportError:
    pass
