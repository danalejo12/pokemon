"""
VISTAS: aquí está la lógica de la app.

Cada vista recibe una petición HTTP (request) y devuelve una respuesta
(normalmente un HTML renderizado desde un template).

Usamos vistas basadas en clases (CBV) para el CRUD, porque reutilizan
lógica y son más cortas que escribir todo a mano.

Flujo general:
1. El usuario entra a una URL (ej: /pokemon/25/).
2. Django llama a la vista correspondiente (definida en urls.py).
3. La vista consulta la BD, procesa datos y renderiza un template.
4. El template muestra el HTML al usuario.
"""
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Pokemon
from .forms import PokemonForm


# ┌─────────────────────────────────────────────────────────────┐
# │  LISTA (R de CRUD) — muestra todos los Pokémon              │
# └─────────────────────────────────────────────────────────────┘
class PokemonListView(ListView):
    """
    Lista paginada de Pokémon con buscador por nombre y filtro por tipo.

    - model = Pokemon → Django sabe qué tabla consultar.
    - template_name = qué HTML usar.
    - context_object_name = nombre de la variable en el template.
    - paginate_by = cuántos por página.
    """
    model = Pokemon
    template_name = 'pokemon/lista.html'
    context_object_name = 'pokemones'
    paginate_by = 12  # 12 Pokémon por página.

    def get_queryset(self):
        """
        Sobrescribimos para filtrar por búsqueda y tipo.
        Django llama a get_queryset() para obtener los datos.
        """
        # Empezamos con todos los Pokémon.
        qs = Pokemon.objects.all()

        # Buscador: /pokemon/?q=pika
        q = self.request.GET.get('q', '').strip()
        if q:
            # __icontains = que contenga (sin importar mayúsculas).
            qs = qs.filter(nombre__icontains=q)

        # Filtro por tipo: /pokemon/?tipo=Fuego
        tipo = self.request.GET.get('tipo', '').strip()
        if tipo:
            # Busca en tipo principal O secundario.
            from django.db.models import Q
            qs = qs.filter(Q(tipo=tipo) | Q(tipo_secundario=tipo))

        return qs

    def get_context_data(self, **kwargs):
        """Agregamos datos extra al template (para el buscador y filtro)."""
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['tipo_seleccionado'] = self.request.GET.get('tipo', '')
        # Lista de tipos disponibles para el select.
        context['tipos'] = [c[0] for c in Pokemon.TIPO_CHOICES]
        context['total_pokemones'] = Pokemon.objects.count()
        return context


# ┌─────────────────────────────────────────────────────────────┐
# │  DETALLE (R de CRUD) — muestra un Pokémon en detalle        │
# └─────────────────────────────────────────────────────────────┘
class PokemonDetailView(DetailView):
    """Muestra la ficha completa de un Pokémon."""
    model = Pokemon
    template_name = 'pokemon/detalle.html'
    context_object_name = 'pokemon'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Habilidades relacionadas (ya vienen en pokemon.habilidades).
        context['habilidades'] = self.object.habilidades.all()
        # Total de stats para la barra.
        context['total_stats'] = self.object.total_stats
        return context


# ┌─────────────────────────────────────────────────────────────┐
# │  CREAR (C de CRUD) — formulario para agregar un Pokémon     │
# └─────────────────────────────────────────────────────────────┘
class PokemonCreateView(CreateView):
    """
    CreateView ya trae el formulario listo.
    Solo debemos decirle qué modelo, formulario y template usar,
    y a dónde redirigir después de guardar.
    """
    model = Pokemon
    form_class = PokemonForm
    template_name = 'pokemon/formulario.html'
    # A dónde ir después de crear (a la lista).
    success_url = reverse_lazy('pokemon-lista')

    def form_valid(self, form):
        """Se llama cuando el formulario es válido. Mostramos un mensaje."""
        messages.success(self.request, f"¡{form.instance.nombre} se unió a la Pokedex!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = '¡Atrapa un nuevo Pokémon!'
        context['boton_submit'] = 'Guardar Pokémon'
        return context


# ┌─────────────────────────────────────────────────────────────┐
# │  EDITAR (U de CRUD) — modifica un Pokémon existente         │
# └─────────────────────────────────────────────────────────────┘
class PokemonUpdateView(UpdateView):
    """Igual que CreateView, pero cargando un objeto existente."""
    model = Pokemon
    form_class = PokemonForm
    template_name = 'pokemon/formulario.html'
    success_url = reverse_lazy('pokemon-lista')

    def form_valid(self, form):
        messages.info(self.request, f"{form.instance.nombre} fue actualizado.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar {self.object.nombre}"
        context['boton_submit'] = 'Guardar cambios'
        return context


# ┌─────────────────────────────────────────────────────────────┐
# │  ELIMINAR (D de CRUD) — confirman y borran un Pokémon       │
# └─────────────────────────────────────────────────────────────┘
class PokemonDeleteView(DeleteView):
    """
    DeleteView muestra una página de confirmación antes de borrar.
    Si el usuario confirma con POST, borra y redirige.
    """
    model = Pokemon
    template_name = 'pokemon/confirmar_borrado.html'
    success_url = reverse_lazy('pokemon-lista')

    def form_valid(self, form):
        messages.warning(self.request, f"{self.object.nombre} fue liberado...")
        return super().form_valid(form)  # Esto hace el borrado real.


# ┌─────────────────────────────────────────────────────────────┐
# │  VISTA SIMPLE (función) — la página de inicio               │
# └─────────────────────────────────────────────────────────────┘
def inicio(request):
    """
    Vista basada en función (FBV) para la home.
    Muestra 6 Pokémon destacados y estadísticas.
    """
    # Traemos 6 Pokémon con imagen (los primeros por número).
    destacados = Pokemon.objects.exclude(imagen_url__isnull=True).exclude(imagen_url='')[:6]
    # Si no hay suficientes, completamos con los primeros.
    if destacados.count() < 6:
        destacados = Pokemon.objects.all()[:6]

    context = {
        'destacados': destacados,
        'total_pokemones': Pokemon.objects.count(),
        'tipos': [c[0] for c in Pokemon.TIPO_CHOICES],
    }
    # render() mezcla el template con los datos del contexto.
    return render(request, 'pokemon/inicio.html', context)
