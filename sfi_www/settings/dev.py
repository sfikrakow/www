from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

WEBPACK_LOADER['DEFAULT']['CACHE'] = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*q^o$d!6el@6vg-9ylnna5-t+@yvnraeyg5t6&!x=$5mh=x4%^'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

OIDC_ADMIN_ROLE = 'sfi'
OIDC_OP_AUTHORIZATION_ENDPOINT = 'https://sso.sfi.pl/auth/realms/public/protocol/openid-connect/auth'
OIDC_OP_TOKEN_ENDPOINT = 'https://sso.sfi.pl/auth/realms/public/protocol/openid-connect/token'
OIDC_OP_USER_ENDPOINT = 'https://sso.sfi.pl/auth/realms/public/protocol/openid-connect/userinfo'
OIDC_OP_JWKS_ENDPOINT = 'https://sso.sfi.pl/auth/realms/public/protocol/openid-connect/certs'
OIDC_OP_LOGOUT_ENDPOINT = 'https://sso.sfi.pl/auth/realms/public/protocol/openid-connect/logout'
OIDC_RP_CLIENT_ID = 'dev'
OIDC_RP_CLIENT_SECRET = None

MIDDLEWARE += [
    'livereload.middleware.LiveReloadScript',
]

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

try:
    from .local import *
except ImportError:
    pass
