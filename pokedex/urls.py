"""
URLs principales del proyecto.

Django busca primero aquí. Si la petición empieza con "/pokemon/",
delegamos todo a las URLs de la app pokemon.
El admin vive en "/admin/".
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Panel de administrador de Django.
    path('admin/', admin.site.urls),
    # Todo lo que empiece con /pokemon/ lo maneja la app pokemon.
    path('pokemon/', include('pokemon.urls')),
    # Y la raíz / redirige a /pokemon/ para que no te pierdas.
    path('', include('pokemon.urls')),
]
