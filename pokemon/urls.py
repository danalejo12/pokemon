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
]
