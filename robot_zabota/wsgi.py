import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'robot_zabota.settings')

application = get_wsgi_application()
