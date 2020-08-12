import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GroupPlus.settings")

application = get_wsgi_application()
application = WhiteNoise(application)
application.add_files(Path('static-files'), prefix='/static')
