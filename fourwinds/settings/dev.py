from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '20g&ri1i7pf$e*_kml%1rrlo%yvy+mn2n57djw2r8%x6&akxv#'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_URL = '/media/'
STATIC_URL = '/assets/'
print "Static url: {}".format(STATIC_URL)
try:
    from .local import *
except ImportError:
    pass
