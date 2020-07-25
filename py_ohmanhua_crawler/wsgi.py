"""
WSGI config for py_ohmanhua_crawler project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dj_static import Cling # <- 加入

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'py_ohmanhua_crawler.settings')

# application = get_wsgi_application()
application = Cling(get_wsgi_application()) # <- 修改