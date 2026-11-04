"""
Comando personalizado: python manage.py seed

Llena la base de datos con Pokémon de ejemplo (los clásicos de Kanto).
Es útil para probar la app sin crear todo a mano.

Uso:
    python manage.py seed          # crea los datos
    python manage.py seed --reset  # borra todo primero
"""
from django.core.management.base import BaseCommand
from pokemon.models import Pokemon, Habilidad


# Datos de ejemplo con sprites oficiales de PokeAPI.
POKEMONES_SEED = [
    {'nombre': 'Bulbasaur', 'numero': 1, 'tipo': 'Planta', 'tipo_secundario': 'Veneno',
     'hp': 45, 'ataque': 49, 'defensa': 49, 'velocidad': 45,
     'descripcion': 'Puede sobrevivir durante días únicamente con la luz del sol que absorbe su semilla.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png'},
    {'nombre': 'Charmander', 'numero': 4, 'tipo': 'Fuego',
     'hp': 39, 'ataque': 52, 'defensa': 43, 'velocidad': 65,
     'descripcion': 'La llama de su cola indica su estado de salud. Si se apaga, muere.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/4.png'},
    {'nombre': 'Squirtle', 'numero': 7, 'tipo': 'Agua',
     'hp': 44, 'ataque': 48, 'defensa': 65, 'velocidad': 43,
     'descripcion': 'Cuando se siente en peligro, se refugia en su caparazón y escupe agua con fuerza.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/7.png'},
    {'nombre': 'Pikachu', 'numero': 25, 'tipo': 'Eléctrico',
     'hp': 35, 'ataque': 55, 'defensa': 40, 'velocidad': 90,
     'descripcion': 'Cuando se enoja, libera electricidad de sus mejillas. Puede derrotar a un enemigo lanzando rayos.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png'},
    {'nombre': 'Charizard', 'numero': 6, 'tipo': 'Fuego', 'tipo_secundario': 'Volador',
     'hp': 78, 'ataque': 84, 'defensa': 78, 'velocidad': 100,
     'descripcion': 'Escupe fuego a una temperatura de 2000 °C. Puede cruzar los cielos a Mach 2.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png'},
    {'nombre': 'Blastoise', 'numero': 9, 'tipo': 'Agua',
     'hp': 79, 'ataque': 83, 'defensa': 100, 'velocidad': 78,
     'descripcion': 'Fuerza bruta, nadando a altas velocidades lanza su peso completo en un embiste.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/9.png'},
    {'nombre': 'Venusaur', 'numero': 3, 'tipo': 'Planta', 'tipo_secundario': 'Veneno',
     'hp': 80, 'ataque': 82, 'defensa': 83, 'velocidad': 80,
     'descripcion': 'Su flor florece cuando está absorbiendo la luz del sol. Libera un aroma que calma los ánimos.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/3.png'},
    {'nombre': 'Gengar', 'numero': 94, 'tipo': 'Fantasma', 'tipo_secundario': 'Veneno',
     'hp': 60, 'ataque': 65, 'defensa': 60, 'velocidad': 110,
     'descripcion': 'Bajo una luna llena, si tu sombra se ríe sola, podría ser el trabajo de un Gengar.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png'},
    {'nombre': 'Snorlax', 'numero': 143, 'tipo': 'Normal',
     'hp': 160, 'ataque': 110, 'defensa': 65, 'velocidad': 30,
     'descripcion': 'Su estómago puede digerir casi cualquier cosa. Come 400 kg de comida al día.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/143.png'},
    {'nombre': 'Dragonite', 'numero': 149, 'tipo': 'Dragón', 'tipo_secundario': 'Volador',
     'hp': 91, 'ataque': 119, 'defensa': 95, 'velocidad': 80,
     'descripcion': 'Un Pokémon amable. Se dice que puede rodear el mundo en solo 16 horas.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/149.png'},
    {'nombre': 'Mewtwo', 'numero': 150, 'tipo': 'Psíquico',
     'hp': 106, 'ataque': 110, 'defensa': 90, 'velocidad': 130,
     'descripcion': 'Su ADN es casi el mismo que el de Mew. Fue creado por científicos tras años de experimentos.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png'},
    {'nombre': 'Mew', 'numero': 151, 'tipo': 'Psíquico',
     'hp': 100, 'ataque': 100, 'defensa': 100, 'velocidad': 100,
     'descripcion': 'Se dice que contiene los genes de todos los Pokémon. Es el Pokémon ancestral.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/151.png'},
    {'nombre': 'Eevee', 'numero': 133, 'tipo': 'Normal',
     'hp': 55, 'ataque': 55, 'defensa': 50, 'velocidad': 55,
     'descripcion': 'Un Pokémon con un código genético irregular. Puede evolucionar en muchas formas distintas.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/133.png'},
    {'nombre': 'Lucario', 'numero': 448, 'tipo': 'Lucha', 'tipo_secundario': 'Acero',
     'hp': 70, 'ataque': 110, 'defensa': 70, 'velocidad': 90,
     'descripcion': 'Puede sentir el aura de todos los seres vivos. Ningún movimiento le falla.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/448.png'},
    {'nombre': 'Garchomp', 'numero': 445, 'tipo': 'Dragón', 'tipo_secundario': 'Tierra',
     'hp': 108, 'ataque': 130, 'defensa': 95, 'velocidad': 102,
     'descripcion': 'Cuando corre a velocidad máxima, sus alas crean cuchillas que pueden cortar la piel.',
     'imagen_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/445.png'},
]

HABILIDADES_SEED = [
    {'nombre': 'Impactrueno', 'tipo': 'Eléctrico', 'potencia': 40,
     'descripcion': 'Ataque eléctrico básico.'},
    {'nombre': 'Lanzallamas', 'tipo': 'Fuego', 'potencia': 90,
     'descripcion': 'Quema al objetivo con llamas.'},
    {'nombre': 'Pistola Agua', 'tipo': 'Agua', 'potencia': 40,
     'descripcion': 'Disparo de agua a presión.'},
    {'nombre': 'Terremoto', 'tipo': 'Tierra', 'potencia': 100,
     'descripcion': 'Provoca un terremoto que daña a todos.'},
    {'nombre': 'Psíquico', 'tipo': 'Psíquico', 'potencia': 90,
     'descripcion': 'Ataque con poder psíquico.'},
    {'nombre': 'Bola Sombra', 'tipo': 'Fantasma', 'potencia': 80,
     'descripcion': 'Orbe de sombra oscura.'},
    {'nombre': 'Danza Espada', 'tipo': 'Normal', 'potencia': 0,
     'descripcion': 'Sube el ataque.'},
    {'nombre': 'A Muertes', 'tipo': 'Dragón', 'potencia': 120,
     'descripcion': 'Ataque dragón devastador.'},
]


class Command(BaseCommand):
    help = 'Llena la BD con Pokémon de ejemplo.'

    def add_arguments(self, parser):
        # --reset borra todos los datos antes de sembrar.
        parser.add_argument('--reset', action='store_true', help='Borrar datos existentes primero')

    def handle(self, *args, **options):
        if options['reset']:
            Pokemon.objects.all().delete()
            Habilidad.objects.all().delete()
            self.stdout.write('Datos anteriores eliminados.')

        # update_or_create: si ya existe (mismo número), lo actualiza.
        creados = 0
        for datos in POKEMONES_SEED:
            obj, creado = Pokemon.objects.update_or_create(
                numero=datos['numero'],
                defaults=datos
            )
            if creado:
                creados += 1

        # Creamos habilidades y las asignamos a algunos Pokémon.
        for datos in HABILIDADES_SEED:
            h, _ = Habilidad.objects.update_or_create(
                nombre=datos['nombre'],
                defaults=datos
            )

        # Asignamos habilidades ejemplo: Pikachu aprende Impactrueno.
        try:
            pikachu = Pokemon.objects.get(numero=25)
            impactrueno = Habilidad.objects.get(nombre='Impactrueno')
            pikachu.habilidades.add(impactrueno)
        except Pokemon.DoesNotExist:
            pass

        self.stdout.write(self.style.SUCCESS(
            f'Seed completado: {creados} Pokemon nuevos (total: {Pokemon.objects.count()}).'
        ))
