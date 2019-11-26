import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DAJANGO_SETTINGS_MODULE', 'speagle_manager.settings')
django.setup()
application = get_default_application()