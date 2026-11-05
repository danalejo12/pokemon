"""
 URLs de la app pokemon.

Cada path() mapea una URL a una vista.
El nombre (name=) nos sirve para enlazar desde templates con {% url %}.

Estructura:
  /                  → inicio
  /lista/            → listado de Pokémon
  /crear/            → formulario de creación
  /<pk>/             → detalle de un Pokémon (pk = clave primaria)
  /<pk>/editar/      → edición
  /<pk>/eliminar/    → borrado
  /importar/         → importar un Pokémon desde PokeAPI
  /regiones/         → regiones con sus 8 gimnasios
  /gimnasios/<pk>/   → detalle de un gimnasio
  /entrenadores/     → entrenadores con su equipo y medallas
"""
from django.urls import path
from . import views

urlpatterns = [
    # Página de inicio.
    path('', views.inicio, name='inicio'),
    # Listado completo.
    path('lista/', views.PokemonListView.as_view(), name='pokemon-lista'),
    # Crear nuevo Pokémon.
    path('crear/', views.PokemonCreateView.as_view(), name='pokemon-crear'),
    # Detalle de uno (pk es el id en la BD).
    path('<int:pk>/', views.PokemonDetailView.as_view(), name='pokemon-detalle'),
    # Editar uno.
    path('<int:pk>/editar/', views.PokemonUpdateView.as_view(), name='pokemon-editar'),
    # Borrar uno.
    path('<int:pk>/eliminar/', views.PokemonDeleteView.as_view(), name='pokemon-eliminar'),
    # Importar desde PokeAPI (https://pokeapi.co/).
    path('importar/', views.importar_pokeapi, name='pokemon-importar'),
    # Regiones, gimnasios y entrenadores.
    path('regiones/', views.RegionListView.as_view(), name='region-lista'),
    path('regiones/<int:pk>/', views.RegionDetailView.as_view(), name='region-detalle'),
    path('gimnasios/<int:pk>/', views.GimnasioDetailView.as_view(), name='gimnasio-detalle'),
    path('entrenadores/', views.EntrenadorListView.as_view(), name='entrenador-lista'),
    path('entrenadores/<int:pk>/', views.EntrenadorDetailView.as_view(), name='entrenador-detalle'),
]
