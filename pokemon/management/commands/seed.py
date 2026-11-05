"""
Comando personalizado: python manage.py seed

Llena la base de datos con Pokémon de ejemplo (los clásicos de Kanto).
Es útil para probar la app sin crear todo a mano.

Uso:
    python manage.py seed          # crea los datos
    python manage.py seed --reset  # borra todo primero
"""
from django.core.management.base import BaseCommand
from pokemon.models import Pokemon, Habilidad, Region, Gimnasio, Entrenador


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
] + [
    # 25 Pokémon famosos adicionales. La imagen se arma con el número
    # (arte oficial de PokeAPI), igual que los de arriba.
    {**datos, 'imagen_url': f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{datos["numero"]}.png'}
    for datos in [
        {'nombre': 'Raichu', 'numero': 26, 'tipo': 'Eléctrico',
         'hp': 60, 'ataque': 90, 'defensa': 55, 'velocidad': 110,
         'descripcion': 'Su cola actúa como toma de tierra para descargar el exceso de electricidad.'},
        {'nombre': 'Jigglypuff', 'numero': 39, 'tipo': 'Normal', 'tipo_secundario': 'Hada',
         'hp': 115, 'ataque': 45, 'defensa': 20, 'velocidad': 20,
         'descripcion': 'Canta una melodía de cuna que duerme a quien la escuche.'},
        {'nombre': 'Meowth', 'numero': 52, 'tipo': 'Normal',
         'hp': 40, 'ataque': 45, 'defensa': 35, 'velocidad': 90,
         'descripcion': 'Adora los objetos redondos y brillantes. Sale de noche a buscar monedas.'},
        {'nombre': 'Psyduck', 'numero': 54, 'tipo': 'Agua',
         'hp': 50, 'ataque': 52, 'defensa': 48, 'velocidad': 55,
         'descripcion': 'Sufre constantes dolores de cabeza que desatan misteriosos poderes psíquicos.'},
        {'nombre': 'Arcanine', 'numero': 59, 'tipo': 'Fuego',
         'hp': 90, 'ataque': 110, 'defensa': 80, 'velocidad': 95,
         'descripcion': 'Un Pokémon legendario en la antigua China por su gracia y velocidad.'},
        {'nombre': 'Alakazam', 'numero': 65, 'tipo': 'Psíquico',
         'hp': 55, 'ataque': 50, 'defensa': 45, 'velocidad': 120,
         'descripcion': 'Su cerebro crece sin parar. Tiene un coeficiente intelectual de 5000.'},
        {'nombre': 'Machamp', 'numero': 68, 'tipo': 'Lucha',
         'hp': 90, 'ataque': 130, 'defensa': 80, 'velocidad': 55,
         'descripcion': 'Con sus cuatro brazos puede lanzar 1000 puñetazos en dos segundos.'},
        {'nombre': 'Onix', 'numero': 95, 'tipo': 'Roca', 'tipo_secundario': 'Tierra',
         'hp': 35, 'ataque': 45, 'defensa': 160, 'velocidad': 70,
         'descripcion': 'Excava bajo tierra a 80 km/h dejando túneles a su paso.'},
        {'nombre': 'Gyarados', 'numero': 130, 'tipo': 'Agua', 'tipo_secundario': 'Volador',
         'hp': 95, 'ataque': 125, 'defensa': 79, 'velocidad': 81,
         'descripcion': 'Extremadamente feroz. Cuando se enfurece, arrasa ciudades enteras.'},
        {'nombre': 'Lapras', 'numero': 131, 'tipo': 'Agua', 'tipo_secundario': 'Hielo',
         'hp': 130, 'ataque': 85, 'defensa': 80, 'velocidad': 60,
         'descripcion': 'Le encanta transportar personas por el mar sobre su caparazón.'},
        {'nombre': 'Vaporeon', 'numero': 134, 'tipo': 'Agua',
         'hp': 130, 'ataque': 65, 'defensa': 60, 'velocidad': 65,
         'descripcion': 'Su estructura celular es similar al agua y puede volverse invisible en ella.'},
        {'nombre': 'Jolteon', 'numero': 135, 'tipo': 'Eléctrico',
         'hp': 65, 'ataque': 65, 'defensa': 60, 'velocidad': 130,
         'descripcion': 'Eriza su pelaje como agujas cargadas con 10 000 voltios.'},
        {'nombre': 'Flareon', 'numero': 136, 'tipo': 'Fuego',
         'hp': 65, 'ataque': 130, 'defensa': 60, 'velocidad': 65,
         'descripcion': 'Almacena fuego en su cuerpo; su temperatura puede superar los 900 °C.'},
        {'nombre': 'Articuno', 'numero': 144, 'tipo': 'Hielo', 'tipo_secundario': 'Volador',
         'hp': 90, 'ataque': 85, 'defensa': 100, 'velocidad': 85,
         'descripcion': 'Ave legendaria que congela el vapor del aire para crear nieve.'},
        {'nombre': 'Zapdos', 'numero': 145, 'tipo': 'Eléctrico', 'tipo_secundario': 'Volador',
         'hp': 90, 'ataque': 90, 'defensa': 85, 'velocidad': 100,
         'descripcion': 'Ave legendaria que aparece entre nubes de tormenta lanzando rayos.'},
        {'nombre': 'Moltres', 'numero': 146, 'tipo': 'Fuego', 'tipo_secundario': 'Volador',
         'hp': 90, 'ataque': 100, 'defensa': 90, 'velocidad': 90,
         'descripcion': 'Ave legendaria de fuego. Se dice que su llegada anuncia la primavera.'},
        {'nombre': 'Umbreon', 'numero': 197, 'tipo': 'Siniestro',
         'hp': 95, 'ataque': 65, 'defensa': 110, 'velocidad': 65,
         'descripcion': 'Los anillos de su cuerpo brillan bajo la luz de la luna.'},
        {'nombre': 'Tyranitar', 'numero': 248, 'tipo': 'Roca', 'tipo_secundario': 'Siniestro',
         'hp': 100, 'ataque': 134, 'defensa': 110, 'velocidad': 61,
         'descripcion': 'Tan poderoso que puede derribar montañas para hacer su nido.'},
        {'nombre': 'Lugia', 'numero': 249, 'tipo': 'Psíquico', 'tipo_secundario': 'Volador',
         'hp': 106, 'ataque': 90, 'defensa': 130, 'velocidad': 110,
         'descripcion': 'Guardián de los mares. Un aleteo suyo puede causar tormentas de 40 días.'},
        {'nombre': 'Ho-Oh', 'numero': 250, 'tipo': 'Fuego', 'tipo_secundario': 'Volador',
         'hp': 106, 'ataque': 130, 'defensa': 90, 'velocidad': 90,
         'descripcion': 'Sus plumas brillan en siete colores. Quien lo ve tendrá felicidad eterna.'},
        {'nombre': 'Blaziken', 'numero': 257, 'tipo': 'Fuego', 'tipo_secundario': 'Lucha',
         'hp': 80, 'ataque': 120, 'defensa': 70, 'velocidad': 80,
         'descripcion': 'Sus patadas llameantes pueden calcinar a cualquier rival.'},
        {'nombre': 'Gardevoir', 'numero': 282, 'tipo': 'Psíquico', 'tipo_secundario': 'Hada',
         'hp': 68, 'ataque': 65, 'defensa': 65, 'velocidad': 80,
         'descripcion': 'Protegerá a su entrenador aunque tenga que arriesgar su vida.'},
        {'nombre': 'Rayquaza', 'numero': 384, 'tipo': 'Dragón', 'tipo_secundario': 'Volador',
         'hp': 105, 'ataque': 150, 'defensa': 90, 'velocidad': 95,
         'descripcion': 'Vive en la capa de ozono y calma las disputas entre Groudon y Kyogre.'},
        {'nombre': 'Greninja', 'numero': 658, 'tipo': 'Agua', 'tipo_secundario': 'Siniestro',
         'hp': 72, 'ataque': 95, 'defensa': 67, 'velocidad': 122,
         'descripcion': 'Ágil como un ninja, lanza estrellas de agua comprimida.'},
        {'nombre': 'Sylveon', 'numero': 700, 'tipo': 'Hada',
         'hp': 95, 'ataque': 65, 'defensa': 65, 'velocidad': 60,
         'descripcion': 'Envuelve a su entrenador con sus cintas para transmitirle cariño.'},
    ]
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

REGIONES_SEED = [
    {'nombre': 'Kanto', 'generacion': 1,
     'descripcion': 'La región donde todo comenzó. Hogar del Profesor Oak y de Pueblo Paleta.'},
    {'nombre': 'Johto', 'generacion': 2,
     'descripcion': 'Región vecina de Kanto, llena de tradición y templos antiguos.'},
]

# (orden, nombre, ciudad, líder, tipo, medalla) — 8 por región.
GIMNASIOS_SEED = {
    'Kanto': [
        (1, 'Gimnasio Plateada', 'Ciudad Plateada', 'Brock', 'Roca', 'Medalla Roca'),
        (2, 'Gimnasio Celeste', 'Ciudad Celeste', 'Misty', 'Agua', 'Medalla Cascada'),
        (3, 'Gimnasio Carmín', 'Ciudad Carmín', 'Lt. Surge', 'Eléctrico', 'Medalla Trueno'),
        (4, 'Gimnasio Azulona', 'Ciudad Azulona', 'Erika', 'Planta', 'Medalla Arcoíris'),
        (5, 'Gimnasio Fucsia', 'Ciudad Fucsia', 'Koga', 'Veneno', 'Medalla Alma'),
        (6, 'Gimnasio Azafrán', 'Ciudad Azafrán', 'Sabrina', 'Psíquico', 'Medalla Pantano'),
        (7, 'Gimnasio Canela', 'Isla Canela', 'Blaine', 'Fuego', 'Medalla Volcán'),
        (8, 'Gimnasio Verde', 'Ciudad Verde', 'Giovanni', 'Tierra', 'Medalla Tierra'),
    ],
    'Johto': [
        (1, 'Gimnasio Malva', 'Ciudad Malva', 'Pegaso', 'Volador', 'Medalla Céfiro'),
        (2, 'Gimnasio Azalea', 'Pueblo Azalea', 'Antón', 'Bicho', 'Medalla Colmena'),
        (3, 'Gimnasio Trigal', 'Ciudad Trigal', 'Blanca', 'Normal', 'Medalla Planicie'),
        (4, 'Gimnasio Iris', 'Ciudad Iris', 'Morti', 'Fantasma', 'Medalla Niebla'),
        (5, 'Gimnasio Orquídea', 'Ciudad Orquídea', 'Aníbal', 'Lucha', 'Medalla Tormenta'),
        (6, 'Gimnasio Olivo', 'Ciudad Olivo', 'Yasmina', 'Acero', 'Medalla Mineral'),
        (7, 'Gimnasio Caoba', 'Pueblo Caoba', 'Fredo', 'Hielo', 'Medalla Glaciar'),
        (8, 'Gimnasio Endrino', 'Ciudad Endrino', 'Débora', 'Dragón', 'Medalla Dragón'),
    ],
}

# equipo = números de Pokédex; medallas = cuántas tiene (las primeras N de su región).
ENTRENADORES_SEED = [
    {'nombre': 'Ash', 'edad': 10, 'ciudad_origen': 'Pueblo Paleta', 'region': 'Kanto',
     'equipo': [25, 6, 1, 7, 143, 448], 'medallas': 8},
    {'nombre': 'Gary', 'edad': 10, 'ciudad_origen': 'Pueblo Paleta', 'region': 'Kanto',
     'equipo': [9, 59, 65, 248, 197], 'medallas': 8},
    {'nombre': 'Red', 'edad': 11, 'ciudad_origen': 'Pueblo Paleta', 'region': 'Kanto',
     'equipo': [25, 3, 6, 9, 143, 131], 'medallas': 8},
    {'nombre': 'Blue', 'edad': 11, 'ciudad_origen': 'Pueblo Paleta', 'region': 'Kanto',
     'equipo': [65, 130, 59, 3], 'medallas': 8},
    {'nombre': 'Leaf', 'edad': 11, 'ciudad_origen': 'Pueblo Paleta', 'region': 'Kanto',
     'equipo': [1, 133, 39], 'medallas': 5},
    {'nombre': 'Ritchie', 'edad': 10, 'ciudad_origen': 'Ciudad Verde', 'region': 'Kanto',
     'equipo': [26, 6, 54], 'medallas': 7},
    {'nombre': 'Tracey', 'edad': 13, 'ciudad_origen': 'Ciudad Azulona', 'region': 'Kanto',
     'equipo': [54, 134], 'medallas': 2},
    {'nombre': 'Jessie', 'edad': 25, 'ciudad_origen': 'Ciudad Azafrán', 'region': 'Kanto',
     'equipo': [52, 94], 'medallas': 0},
    {'nombre': 'James', 'edad': 25, 'ciudad_origen': 'Ciudad Azulona', 'region': 'Kanto',
     'equipo': [52, 95], 'medallas': 0},
    {'nombre': 'Lance', 'edad': 28, 'ciudad_origen': 'Ciudad Endrino', 'region': 'Johto',
     'equipo': [149, 130, 384, 445], 'medallas': 8},
    {'nombre': 'Gold', 'edad': 11, 'ciudad_origen': 'Pueblo Primavera', 'region': 'Johto',
     'equipo': [250, 135, 68, 257], 'medallas': 8},
    {'nombre': 'Silver', 'edad': 11, 'ciudad_origen': 'Pueblo Primavera', 'region': 'Johto',
     'equipo': [248, 94, 197, 136], 'medallas': 6},
    {'nombre': 'Lyra', 'edad': 11, 'ciudad_origen': 'Pueblo Primavera', 'region': 'Johto',
     'equipo': [249, 700, 282], 'medallas': 7},
    {'nombre': 'Kris', 'edad': 11, 'ciudad_origen': 'Pueblo Primavera', 'region': 'Johto',
     'equipo': [144, 145, 146], 'medallas': 4},
    {'nombre': 'Casey', 'edad': 12, 'ciudad_origen': 'Ciudad Trigal', 'region': 'Johto',
     'equipo': [658, 135, 25], 'medallas': 3},
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
            Entrenador.objects.all().delete()
            Region.objects.all().delete()  # borra también sus gimnasios
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

        # Regiones y sus 8 gimnasios.
        for datos in REGIONES_SEED:
            region, _ = Region.objects.update_or_create(nombre=datos['nombre'], defaults=datos)
            for orden, nombre, ciudad, lider, tipo, medalla in GIMNASIOS_SEED[region.nombre]:
                Gimnasio.objects.update_or_create(
                    region=region, orden=orden,
                    defaults={'nombre': nombre, 'ciudad': ciudad, 'lider': lider,
                              'tipo': tipo, 'medalla': medalla},
                )

        # Entrenadores: conectamos con región, Pokémon (equipo) y gimnasios (medallas).
        for datos in ENTRENADORES_SEED:
            region = Region.objects.get(nombre=datos['region'])
            entrenador, _ = Entrenador.objects.update_or_create(
                nombre=datos['nombre'],
                defaults={'edad': datos['edad'], 'ciudad_origen': datos['ciudad_origen'],
                          'region': region},
            )
            entrenador.equipo.set(Pokemon.objects.filter(numero__in=datos['equipo']))
            entrenador.medallas.set(region.gimnasios.filter(orden__lte=datos['medallas']))

        self.stdout.write(self.style.SUCCESS(
            f'Regiones: {Region.objects.count()}, gimnasios: {Gimnasio.objects.count()}, '
            f'entrenadores: {Entrenador.objects.count()}.'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Seed completado: {creados} Pokemon nuevos (total: {Pokemon.objects.count()}).'
        ))
