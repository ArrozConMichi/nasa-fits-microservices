import os
import sys
from django.core.management import execute_from_command_line

# Le indicamos a Django qué archivo de configuración debe usar
# (El archivo nasa_gateway/settings.py que creó Django automáticamente)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nasa_gateway.settings')

if __name__ == '__main__':
    # Esto ejecuta el servidor de desarrollo usando el manage.py existente
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])