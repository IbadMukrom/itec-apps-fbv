"""
WSGI config for itec project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itec.settings')

application = get_wsgi_application()
<<<<<<< HEAD
# application = DjangoWhiteNoise(application)

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())
=======
application = DjangoWhiteNoise(application)
>>>>>>> 7bb5374243ab80de24834640f8194d46e77047d9
