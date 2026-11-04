"""
FORMULARIOS: Django Forms validan los datos antes de guardarlos.

ModelForm = formulario que se mapea directo a un modelo.
Esto nos ahorra escribir campos a mano y nos da validación gratis.
"""
from django import forms
from .models import Pokemon


class PokemonForm(forms.ModelForm):
    """Formulario para crear y editar un Pokémon."""
    class Meta:
        model = Pokemon
        # Campos que aparecen en el formulario.
        fields = [
            'nombre', 'numero', 'tipo', 'tipo_secundario',
            'hp', 'ataque', 'defensa', 'velocidad',
            'descripcion', 'imagen_url'
        ]
        # Widgets: cómo se renderiza cada campo en HTML.
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe la descripción de la Pokedex...'}),
            'imagen_url': forms.URLInput(attrs={'placeholder': 'https://...'}),
        }
        # Etiquetas en español para el formulario.
        labels = {
            'nombre': 'Nombre',
            'numero': 'N.º Pokedex',
            'tipo': 'Tipo principal',
            'tipo_secundario': 'Tipo secundario (opcional)',
            'hp': 'HP',
            'ataque': 'Ataque',
            'defensa': 'Defensa',
            'velocidad': 'Velocidad',
            'descripcion': 'Descripción',
            'imagen_url': 'URL de imagen',
        }
        # Ayuda que se muestra bajo cada campo.
        help_texts = {
            'numero': 'Número en la Pokedex Nacional (ej: 25 para Pikachu)',
            'imagen_url': 'Pega la URL del sprite oficial (ej: de PokeAPI)',
        }

    def clean(self):
        """
        Validación personalizada: los stats deben estar entre 1 y 255.
        clean() se llama con todos los datos ya parseados.
        """
        cleaned_data = super().clean()
        # Validamos cada stat.
        for campo in ('hp', 'ataque', 'defensa', 'velocidad'):
            valor = cleaned_data.get(campo)
            if valor is not None and not 1 <= valor <= 255:
                self.add_error(campo, 'El valor debe estar entre 1 y 255.')
        return cleaned_data
