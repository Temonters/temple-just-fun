from django.core.wsgi import get_wsgi_application
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'temple_project.settings')
application = get_wsgi_application()
app = application