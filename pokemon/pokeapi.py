"""
Cliente de PokeAPI (https://pokeapi.co/).

PokeAPI es una API pública y gratuita con los datos de todos los Pokémon.
Aquí la consultamos y convertimos su respuesta (en inglés) a los campos
de nuestro modelo Pokemon (en español).

Usamos urllib (librería estándar de Python) para no instalar nada extra.

Uso:
    from pokemon.pokeapi import obtener_pokemon, importar_pokemon
    datos = obtener_pokemon('pikachu')   # dict con los campos del modelo
    pokemon, creado = importar_pokemon(25)  # lo guarda en la BD
"""
import json
import urllib.error
import urllib.request

BASE_URL = 'https://pokeapi.co/api/v2'
TIMEOUT = 10  # segundos

# PokeAPI devuelve los tipos en inglés; los traducimos a nuestros TIPO_CHOICES.
TIPOS_ES = {
    'normal': 'Normal', 'fire': 'Fuego', 'water': 'Agua', 'grass': 'Planta',
    'electric': 'Eléctrico', 'ice': 'Hielo', 'fighting': 'Lucha', 'poison': 'Veneno',
    'ground': 'Tierra', 'flying': 'Volador', 'psychic': 'Psíquico', 'bug': 'Bicho',
    'rock': 'Roca', 'ghost': 'Fantasma', 'dragon': 'Dragón', 'dark': 'Siniestro',
    'steel': 'Acero', 'fairy': 'Hada',
}


class PokeAPIError(Exception):
    """Error al consultar PokeAPI (no existe, sin internet, etc.)."""


def _get_json(url):
    """Hace un GET a la URL y devuelve el JSON como dict."""
    req = urllib.request.Request(url, headers={'User-Agent': 'pokedex-django'})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise PokeAPIError('Ese Pokémon no existe en PokeAPI.') from e
        raise PokeAPIError(f'PokeAPI respondió con error {e.code}.') from e
    except (urllib.error.URLError, TimeoutError) as e:
        raise PokeAPIError('No se pudo conectar con PokeAPI. ¿Hay internet?') from e


def _descripcion_es(especie):
    """Busca la primera descripción de la Pokédex en español."""
    for entrada in especie.get('flavor_text_entries', []):
        if entrada['language']['name'] == 'es':
            # El texto trae saltos de línea raros (\n, \f); los limpiamos.
            return ' '.join(entrada['flavor_text'].split())
    return ''


def obtener_pokemon(nombre_o_numero):
    """
    Consulta PokeAPI y devuelve un dict listo para crear un Pokemon.

    Acepta nombre ('pikachu') o número (25).
    """
    clave = str(nombre_o_numero).strip().lower()
    if not clave:
        raise PokeAPIError('Escribe un nombre o número.')

    datos = _get_json(f'{BASE_URL}/pokemon/{clave}/')
    # La especie trae la descripción y el nombre "bonito" (con mayúsculas).
    especie = _get_json(datos['species']['url'])

    stats = {s['stat']['name']: s['base_stat'] for s in datos['stats']}
    tipos = [TIPOS_ES.get(t['type']['name'], 'Normal')
             for t in sorted(datos['types'], key=lambda t: t['slot'])]

    nombre = next(
        (n['name'] for n in especie.get('names', []) if n['language']['name'] == 'es'),
        datos['name'].capitalize(),
    )
    imagen = (datos['sprites'].get('other', {}).get('official-artwork', {}).get('front_default')
              or datos['sprites'].get('front_default'))

    return {
        'nombre': nombre,
        'numero': especie['id'],  # número de la Pokédex Nacional
        'tipo': tipos[0],
        'tipo_secundario': tipos[1] if len(tipos) > 1 else None,
        'hp': stats.get('hp', 50),
        'ataque': stats.get('attack', 50),
        'defensa': stats.get('defense', 50),
        'velocidad': stats.get('speed', 50),
        'descripcion': _descripcion_es(especie),
        'imagen_url': imagen,
    }


def importar_pokemon(nombre_o_numero):
    """
    Trae un Pokémon de PokeAPI y lo guarda (o actualiza) en la BD.
    Devuelve (pokemon, creado).
    """
    from .models import Pokemon  # import aquí para evitar import circular

    datos = obtener_pokemon(nombre_o_numero)
    return Pokemon.objects.update_or_create(numero=datos['numero'], defaults=datos)
