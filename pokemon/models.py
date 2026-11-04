"""
MODELOS: aquí defines tus tablas de base de datos.

Cada clase = una tabla en la BD.
Cada atributo = una columna.
Django se encargará de crear las tablas cuando hagas `migrate`.

En esta app tenemos dos modelos:
- Pokemon: el personaje principal (nombre, tipo, stats, imagen, etc.)
- Habilidad: las habilidades que aprende un Pokémon (relación muchos a muchos).
"""
from django.db import models
from django.urls import reverse


class Pokemon(models.Model):
    """Modelo principal: un Pokémon de la Pokedex."""
    # Nombre único del Pokémon (ej: "Pikachu").
    nombre = models.CharField(
        max_length=50,
        unique=True,
        help_text="Nombre del Pokémon"
    )
    # Número en la Pokedex nacional (ej: 25).
    numero = models.PositiveIntegerField(
        unique=True,
        help_text="Número en la Pokedex Nacional"
    )
    # Tipo principal (Fuego, Agua, Planta, Eléctrico, etc.).
    TIPO_CHOICES = [
        ('Normal', 'Normal'),
        ('Fuego', 'Fuego'),
        ('Agua', 'Agua'),
        ('Planta', 'Planta'),
        ('Eléctrico', 'Eléctrico'),
        ('Hielo', 'Hielo'),
        ('Lucha', 'Lucha'),
        ('Veneno', 'Veneno'),
        ('Tierra', 'Tierra'),
        ('Volador', 'Volador'),
        ('Psíquico', 'Psíquico'),
        ('Bicho', 'Bicho'),
        ('Roca', 'Roca'),
        ('Fantasma', 'Fantasma'),
        ('Dragón', 'Dragón'),
        ('Siniestro', 'Siniestro'),
        ('Acero', 'Acero'),
        ('Hada', 'Hada'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    # Tipo secundario (opcional, ej: Charizard es Fuego/Volador).
    tipo_secundario = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        blank=True,  # Permite dejarlo vacío.
        null=True,
        help_text="Tipo secundario (opcional)"
    )
    # Estadísticas base (0-255 típicamente en Pokémon).
    hp = models.PositiveIntegerField(default=50, help_text="Puntos de salud")
    ataque = models.PositiveIntegerField(default=50)
    defensa = models.PositiveIntegerField(default=50)
    velocidad = models.PositiveIntegerField(default=50)
    # Descripción de la Pokedex.
    descripcion = models.TextField(
        blank=True,
        help_text="Descripción de la Pokedex"
    )
    # URL de la imagen (no subimos archivos, usamos sprites oficiales).
    imagen_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL de la imagen o sprite"
    )
    # Cuándo se agregó (se crea solo).
    creado_en = models.DateTimeField(auto_now_add=True)
    # Cuándo se modificó por última vez (se actualiza solo).
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        # Orden por defecto cuando listemos Pokémon.
        ordering = ['numero']
        verbose_name = 'Pokémon'
        verbose_name_plural = 'Pokémones'

    def __str__(self):
        # Esto es lo que verás en el admin y en los listados.
        return f"#{self.numero:03d} {self.nombre}"

    def get_absolute_url(self):
        # URL del detalle (ej: /pokemon/25/).
        # reverse() busca por nombre de la URL en urls.py.
        return reverse('pokemon-detalle', kwargs={'pk': self.pk})

    @property
    def total_stats(self):
        """Suma total de stats (útil para mostrar en la ficha)."""
        return self.hp + self.ataque + self.defensa + self.velocidad

    @property
    def tipos_display(self):
        """Devuelve los tipos como texto (ej: "Fuego / Volador")."""
        if self.tipo_secundario:
            return f"{self.tipo} / {self.tipo_secundario}"
        return self.tipo


class Habilidad(models.Model):
    """Habilidades que puede aprender un Pokémon."""
    nombre = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(
        max_length=20,
        choices=Pokemon.TIPO_CHOICES,
        default='Normal'
    )
    potencia = models.PositiveIntegerField(
        default=0,
        help_text="Daño base (0 si es de estado)"
    )
    descripcion = models.TextField(blank=True)
    # Relación muchos a muchos: un Pokémon puede tener varias habilidades
    # y una habilidad puede ser aprendida por muchos Pokémon.
    pokemones = models.ManyToManyField(
        Pokemon,
        related_name='habilidades',
        blank=True
    )

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
