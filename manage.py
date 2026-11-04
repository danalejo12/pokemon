#!/usr/bin/env python
"""Punto de entrada para ejecutar comandos de Django.

Django usa este archivo para saber en qué proyecto trabajar
(django-admin process). Casi nunca necesitas tocarlo.
"""
import os
import sys


def main():
    # Le dice a Django qué configuración usar (el modulo settings).
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokedex.settings')
    try:
        # Importa la utilidad de Django para ejecutar comandos.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No pudimos importar Django. ¿Está instalado?"
        ) from exc
    # Delegamos el control a Django con los argumentos que pasamos
    # por la terminal (ej: runserver, migrate, createsuperuser).
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
