"""
Comando: importa Pokémon desde PokeAPI (https://pokeapi.co/).

Uso:
    python manage.py importar_pokeapi pikachu 6 mewtwo   # por nombre o número
    python manage.py importar_pokeapi --rango 1 151      # todos los de Kanto
"""
from django.core.management.base import BaseCommand, CommandError

from pokemon.pokeapi import PokeAPIError, importar_pokemon


class Command(BaseCommand):
    help = 'Importa Pokémon desde PokeAPI por nombre, número o rango.'

    def add_arguments(self, parser):
        parser.add_argument('pokemones', nargs='*', help='Nombres o números')
        parser.add_argument('--rango', nargs=2, type=int, metavar=('DESDE', 'HASTA'),
                            help='Importa todos los números de DESDE a HASTA')

    def handle(self, *args, **options):
        claves = list(options['pokemones'])
        if options['rango']:
            desde, hasta = options['rango']
            claves += list(range(desde, hasta + 1))
        if not claves:
            raise CommandError('Indica nombres/números o usa --rango DESDE HASTA.')

        for clave in claves:
            try:
                pokemon, creado = importar_pokemon(clave)
            except PokeAPIError as e:
                self.stderr.write(self.style.ERROR(f'{clave}: {e}'))
                continue
            accion = 'creado' if creado else 'actualizado'
            self.stdout.write(self.style.SUCCESS(f'{pokemon} {accion}'))
