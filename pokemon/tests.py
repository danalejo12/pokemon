"""
Tests: aquí verificas que tu app funciona correctamente.
Django trae un test runner integrado: `python manage.py test`
"""
from django.test import TestCase
from django.urls import reverse
from .models import Pokemon


class PokemonModelTest(TestCase):
    """Pruebas del modelo Pokemon."""

    def setUp(self):
        # Creamos un Pokémon de prueba antes de cada test.
        self.pikachu = Pokemon.objects.create(
            nombre='Pikachu',
            numero=25,
            tipo='Eléctrico',
            hp=35, ataque=55, defensa=40, velocidad=90,
            descripcion='Ratón eléctrico.'
        )

    def test_str(self):
        """El __str__ debe mostrar número y nombre."""
        self.assertEqual(str(self.pikachu), '#025 Pikachu')

    def test_total_stats(self):
        """La suma de stats debe ser correcta."""
        self.assertEqual(self.pikachu.total_stats, 35 + 55 + 40 + 90)

    def test_tipos_display_solo_principal(self):
        """Sin tipo secundario, solo muestra el principal."""
        self.assertEqual(self.pikachu.tipos_display, 'Eléctrico')

    def test_tipos_display_doble(self):
        """Con tipo secundario, muestra ambos."""
        self.pikachu.tipo_secundario = 'Hielo'
        self.assertEqual(self.pikachu.tipos_display, 'Eléctrico / Hielo')


class PokemonViewsTest(TestCase):
    """Pruebas de las vistas (URLs y respuestas)."""

    def setUp(self):
        self.pikachu = Pokemon.objects.create(
            nombre='Pikachu', numero=25, tipo='Eléctrico',
            hp=35, ataque=55, defensa=40, velocidad=90
        )

    def test_lista_muestra_pokemon(self):
        """La lista debe contener el Pokémon creado."""
        response = self.client.get(reverse('pokemon-lista'))
        self.assertContains(response, 'Pikachu')

    def test_detalle_muestra_pokemon(self):
        """El detalle debe mostrar datos del Pokémon."""
        response = self.client.get(
            reverse('pokemon-detalle', kwargs={'pk': self.pikachu.pk})
        )
        self.assertContains(response, 'Pikachu')
        self.assertContains(response, 'Eléctrico')

    def test_crear_pokemon(self):
        """Crear un Pokémon vía POST debe funcionar."""
        response = self.client.post(reverse('pokemon-crear'), {
            'nombre': 'Charmander', 'numero': 4,
            'tipo': 'Fuego', 'hp': 39, 'ataque': 52,
            'defensa': 43, 'velocidad': 65,
        })
        self.assertEqual(Pokemon.objects.count(), 2)


# ── Regiones, gimnasios, entrenadores y PokeAPI ──
from unittest import mock

from django.core.management import call_command

from .models import Region, Gimnasio, Entrenador
from .pokeapi import PokeAPIError


class SeedRelacionesTest(TestCase):
    """El seed crea 2 regiones con 8 gimnasios cada una y 15 entrenadores conectados."""

    @classmethod
    def setUpTestData(cls):
        call_command('seed', stdout=mock.MagicMock())

    def test_cantidades(self):
        self.assertEqual(Region.objects.count(), 2)
        self.assertEqual(Entrenador.objects.count(), 15)
        for region in Region.objects.all():
            self.assertEqual(region.gimnasios.count(), 8)

    def test_relaciones_de_ash(self):
        ash = Entrenador.objects.get(nombre='Ash')
        self.assertEqual(ash.region.nombre, 'Kanto')
        self.assertIn(Pokemon.objects.get(numero=25), ash.equipo.all())
        self.assertEqual(ash.medallas.count(), 8)
        # Relación inversa: desde el Pokémon se llega al entrenador.
        self.assertIn(ash, Pokemon.objects.get(numero=25).entrenadores.all())

    def test_paginas_responden(self):
        region = Region.objects.first()
        urls = [
            reverse('region-lista'), reverse('region-detalle', args=[region.pk]),
            reverse('gimnasio-detalle', args=[region.gimnasios.first().pk]),
            reverse('entrenador-lista'),
            reverse('entrenador-detalle', args=[Entrenador.objects.first().pk]),
            reverse('pokemon-importar'),
        ]
        for url in urls:
            self.assertEqual(self.client.get(url).status_code, 200, url)


DATOS_FALSOS = {
    'nombre': 'Cyndaquil', 'numero': 155, 'tipo': 'Fuego', 'tipo_secundario': None,
    'hp': 39, 'ataque': 52, 'defensa': 43, 'velocidad': 65,
    'descripcion': 'Es tímido.', 'imagen_url': 'https://example.com/155.png',
}


class ImportarPokeAPITest(TestCase):
    """Simulamos PokeAPI con mock para no depender de internet."""

    @mock.patch('pokemon.pokeapi.obtener_pokemon', return_value=DATOS_FALSOS)
    def test_importa_y_redirige(self, _):
        r = self.client.post(reverse('pokemon-importar'), {'busqueda': 'cyndaquil'})
        pokemon = Pokemon.objects.get(numero=155)
        self.assertRedirects(r, pokemon.get_absolute_url())
        self.assertEqual(pokemon.tipo, 'Fuego')

    @mock.patch('pokemon.pokeapi.obtener_pokemon', side_effect=PokeAPIError('No existe'))
    def test_error_muestra_mensaje(self, _):
        r = self.client.post(reverse('pokemon-importar'), {'busqueda': 'xyz'})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'No existe')
        self.assertFalse(Pokemon.objects.exists())
