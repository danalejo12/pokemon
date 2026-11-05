# Configuración del panel de administrador de Django.
# Aquí defines cómo se ven los modelos en /admin/.
from django.contrib import admin
from .models import Pokemon, Habilidad, Region, Gimnasio, Entrenador


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    # Columnas que se muestran en el listado del admin.
    list_display = ('numero', 'nombre', 'tipo', 'hp', 'ataque', 'creado_en')
    # Filtros laterales.
    list_filter = ('tipo', 'tipo_secundario')
    # Campo de búsqueda arriba.
    search_fields = ('nombre', 'descripcion')
    # Agrupamos los campos en el formulario de edición.
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'numero', 'tipo', 'tipo_secundario')
        }),
        ('Estadísticas', {
            'fields': ('hp', 'ataque', 'defensa', 'velocidad')
        }),
        ('Extras', {
            'fields': ('descripcion', 'imagen_url')
        }),
    )


@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'potencia')
    list_filter = ('tipo',)
    search_fields = ('nombre', 'descripcion')
    filter_horizontal = ('pokemones',)  # Widget para M2M.


class GimnasioInline(admin.TabularInline):
    """Permite editar los gimnasios desde la página de la región."""
    model = Gimnasio
    extra = 0


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'generacion')
    inlines = [GimnasioInline]


@admin.register(Gimnasio)
class GimnasioAdmin(admin.ModelAdmin):
    list_display = ('orden', 'nombre', 'ciudad', 'lider', 'tipo', 'medalla', 'region')
    list_filter = ('region', 'tipo')
    search_fields = ('nombre', 'ciudad', 'lider')


@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'edad', 'ciudad_origen', 'region')
    list_filter = ('region',)
    search_fields = ('nombre',)
    filter_horizontal = ('equipo', 'medallas')
