"""
WSGI config para el proyecto Pokedex.

WSGI (Web Server Gateway Interface) es el estándar que usan los
servidores web (Gunicorn, uWSGI) para hablar con Django.
En desarrollo con `runserver` no necesitas tocarlo.
"""
import os

from django.core.wsgi import get_wsgi_application

# Le decimos qué configuración usar (settings.py).
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokedex.settings')

# Django crea la aplicación WSGI que el servidor usará.
application = get_wsgi_application()
