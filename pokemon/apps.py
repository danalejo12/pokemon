# Configuración de la app.
from django.apps import AppConfig


class PokemonConfig(AppConfig):
    # Ruta por defecto (Python 3.12+).
    default_auto_field = 'django.db.models.BigAutoField'
    # Nombre de la app, debe coincidir con la carpeta 'pokemon'.
    name = 'pokemon'
