"""
WSGI config for fourwinds project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fourwinds.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
application.add_files(os.path.join(os.path.dirname(BASE_DIR), 'media'), prefix='media/')
