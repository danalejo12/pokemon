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
