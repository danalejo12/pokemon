# 🐍 Pokedex — App de Pokémon en Django

> Una Pokedex web completa con **CRUD**, diseño temático Pokémon, buscador, filtros, paginación y animaciones — todo en **Python + Django**.

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1-092E20?style=flat&logo=django&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-7%20passing-brightgreen)

---

## 📋 Índice

- [¿Qué es?](#-qué-es)
- [Características](#-características)
- [Stack tecnológico](#-stack-tecnológico)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
  - [Páginas y rutas](#páginas-y-rutas)
  - [CRUD completo](#crud-completo)
  - [Buscador y filtros](#buscador-y-filtros)
  - [Panel de administración](#panel-de-administración)
  - [Datos de ejemplo (seed)](#datos-de-ejemplo-seed)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Modelo de datos](#-modelo-de-datos)
- [Comandos útiles](#-comandos-útiles)
- [Pruebas](#-pruebas)
- [Conceptos de Django que aprenderás](#-conceptos-de-django-que-aprenderás)
- [Personalización](#-personalización)
- [Solución de problemas](#-solución-de-problemas)
- [Contribuciones](#-contribuciones)
- [Licencia y marcas](#-licencia-y-marcas)

---

## 📖 ¿Qué es?

Pokedex es una aplicación web estilo Pokédex interactiva: puedes **crear, ver, editar y eliminar Pokémon**, buscarlos por nombre, filtrarlos por tipo, ver sus estadísticas con barras animadas y gestionar habilidades.

Está construida con Django siguiendo el patrón **MVT (Modelo – Vista – Template)** y vistas basadas en clases (CBV) para reutilizar la lógica del CRUD.

Ideal como proyecto para **aprender Django desde cero**: cada archivo incluye comentarios en español explicando qué hace y por qué.

---

## ✨ Características

### Funcionales
- [x] **CRUD completo** de Pokémon: Crear, Leer, Actualizar, Eliminar
- [x] Lista paginada (12 por página)
- [x] Buscador por nombre
- [x] Filtro por tipo principal o secundario
- [x] Ficha de detalle con stats animados (HP, Ataque, Defensa, Velocidad)
- [x] Modelo `Habilidad` con relación Muchos a Muchos
- [x] Validación de stats entre 1 y 255
- [x] Mensajes flash tras crear / editar / eliminar
- [x] Confirmación antes de borrar
- [x] Panel de administración de Django personalizado
- [x] Comando `seed` para cargar 15 Pokémon de ejemplo
- [x] 7 tests automáticos (modelo y vistas)
- [x] Vista previa de imagen al pegar una URL en el formulario

### Diseño
- [x] Paleta temática: amarillo Pikachu `#FFCB05` + rojo Pokébola `#E3350D`
- [x] Navbar con Pokébola en miniatura hecha en CSS
- [x] Tarjetas con hover, sombra y entrada animada escalonada
- [x] Badges de tipo con colores oficiales (Fuego, Agua, Planta, etc.)
- [x] Barras de estadísticas animadas con JavaScript
- [x] Fondo degradado nocturno
- [x] Responsive para móvil

---

## 🛠️ Stack tecnológico

| Tecnología | Versión / Uso |
|---|---|
| **Python** | 3.12+ (probado en 3.14) |
| **Django** | 6.1.3 |
| **Base de datos** | SQLite (archivo `db.sqlite3`) |
| **Templates** | Django Templates (`{% %}`) |
| **Estáticos** | CSS puro + JS vanilla |
| **Sprites** | Imágenes oficiales de [PokeAPI](https://pokeapi.co/docs/v2#sprites) |

---

## 📦 Requisitos

- Python 3.12 o superior
- pip (incluido con Python)
- Git (solo si quieres clonar o subir cambios)
- Un navegador moderno (Chrome, Edge, Firefox)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/danalejo12/pokemon.git
cd pokemon
```

> Si ya tienes la carpeta, salta este paso.

### 2. Crear y activar el entorno virtual

**Windows (PowerShell / CMD):**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Verás `(venv)` al inicio de tu terminal cuando esté activo.

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear la base de datos

```bash
python manage.py migrate
```

Esto crea el archivo `db.sqlite3` y todas las tablas.

### 5. (Opcional) Cargar datos de ejemplo

```bash
python manage.py seed
```

### 6. Levantar el servidor

```bash
python manage.py runserver
```

Abre en el navegador: **http://127.0.0.1:8000/**

---

## 🎮 Uso

### Páginas y rutas

| URL | Qué hace |
|---|---|
| `/` | Página de inicio con Pokémon destacados |
| `/lista/` | Lista completa con buscador y filtros |
| `/crear/` | Formulario para registrar un Pokémon |
| `/<id>/` | Ficha de detalle de un Pokémon (ej: `/4/` = Pikachu) |
| `/<id>/editar/` | Editar un Pokémon existente |
| `/<id>/eliminar/` | Confirmar y eliminar un Pokémon |
| `/admin/` | Panel de administración de Django |

> **Nota:** el `<id>` de la URL es el **ID interno** de la base de datos, no el número Pokedex. El número Pokedex (ej: `#025`) es un campo separado dentro de la ficha.

### CRUD completo

| Operación | Vista | Dónde |
|---|---|---|
| **Crear** (Create) | `PokemonCreateView` | `/crear/` |
| **Leer** (Read) | `PokemonListView` + `PokemonDetailView` | `/lista/` y `/<id>/` |
| **Editar** (Update) | `PokemonUpdateView` | `/<id>/editar/` |
| **Eliminar** (Delete) | `PokemonDeleteView` | `/<id>/eliminar/` |

### Buscador y filtros

En `/lista/` puedes:

- Escribir un nombre: `/lista/?q=pika`
- Filtrar por tipo: `/lista/?tipo=Fuego`
- Combinar ambos: `/lista/?q=char&tipo=Fuego`
- Cambiar de página: `/lista/?page=2`

### Panel de administración

```bash
# Crear un usuario administrador (solo la primera vez)
python manage.py createsuperuser
```

Luego entra a **http://127.0.0.1:8000/admin/** con ese usuario. Ahí podrás:

- Ver, crear y editar Pokémon y Habilidades
- Filtrar por tipo y buscar por nombre
- Gestionar usuarios y permisos de Django

### Datos de ejemplo (seed)

```bash
python manage.py seed           # carga datos sin borrar los existentes
python manage.py seed --reset   # borra todo y vuelve a cargar
```

Los 15 Pokémon incluidos son:

| # | Pokémon | Tipos |
|---|---|---|
| 001 | Bulbasaur | Planta / Veneno |
| 006 | Charizard | Fuego / Volador |
| 009 | Blastoise | Agua |
| 025 | Pikachu | Eléctrico |
| 094 | Gengar | Fantasma / Veneno |
| 133 | Eevee | Normal |
| 143 | Snorlax | Normal |
| 149 | Dragonite | Dragón / Volador |
| 150 | Mewtwo | Psíquico |
| 151 | Mew | Psíquico |
| 445 | Garchomp | Dragón / Tierra |
| 448 | Lucario | Lucha / Acero |

Más Venusaur, Charmander y Squirtle. Todos con arte oficial de PokeAPI y descripción de la Pokedex.

---

## 📂 Estructura del proyecto

```
C:\pokemon\
├── manage.py                      # Entrada de Django (runserver, migrate, etc.)
├── requirements.txt               # Dependencias (Django==6.1.3)
├── db.sqlite3                     # Base de datos SQLite (se genera sola)
├── .gitignore                     # Archivos ignorados por Git (venv, BD, etc.)
├── README.md                      # Este archivo
│
├── pokedex/                       # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py                # Ajustes generales (apps, BD, templates, estáticos)
│   ├── urls.py                    # URLs principales (/admin/, /pokemon/)
│   └── wsgi.py                    # Punto de entrada para servidores web
│
├── pokemon/                       # ¡Nuestra app!
│   ├── __init__.py
│   ├── apps.py                    # Configuración de la app
│   ├── models.py                  # Tablas: Pokemon y Habilidad
│   ├── views.py                   # Vistas (List, Detail, Create, Update, Delete)
│   ├── forms.py                   # Formularios con validación (ModelForm)
│   ├── urls.py                    # Rutas de la app
│   ├── admin.py                   # Configuración del panel /admin/
│   ├── tests.py                   # Pruebas automáticas (7 tests)
│   ├── templates/
│   │   └── pokemon/
│   │       ├── base.html              # Layout base (navbar + footer)
│   │       ├── inicio.html            # Portada
│   │       ├── lista.html             # Listado con buscador y paginación
│   │       ├── detalle.html           # Ficha del Pokémon
│   │       ├── formulario.html        # Crear / Editar (reutilizado)
│   │       └── confirmar_borrado.html # Confirmación de eliminar
│   └── management/
│       └── commands/
│           └── seed.py            # Comando: python manage.py seed
│
├── static/                        # Archivos estáticos (CSS / JS)
│   ├── css/
│   │   └── style.css              # Estilos temáticos Pokémon
│   └── js/
│       └── app.js                 # Animaciones y micro-interacciones
│
└── venv/                          # Entorno virtual (no se sube a Git)
```

---

## 🗄️ Modelo de datos

### `Pokemon`

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Auto (PK) | Clave primaria interna |
| `nombre` | CharField (único) | Nombre, ej: `Pikachu` |
| `numero` | PositiveInteger (único) | N.º en la Pokedex, ej: `25` |
| `tipo` | CharField + choices | Tipo principal (18 tipos) |
| `tipo_secundario` | CharField (opcional) | Segundo tipo |
| `hp` | PositiveInteger | Puntos de salud |
| `ataque` | PositiveInteger | Ataque |
| `defensa` | PositiveInteger | Defensa |
| `velocidad` | PositiveInteger | Velocidad |
| `descripcion` | TextField | Descripción de la Pokedex |
| `imagen_url` | URLField | Sprite / arte oficial |
| `creado_en` | DateTime | Se genera solo al crear |
| `actualizado_en` | DateTime | Se actualiza solo al editar |

Propiedades útiles: `total_stats` (suma de stats) y `tipos_display` (ej: *“Fuego / Volador”*).

### `Habilidad`

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Auto (PK) | Clave primaria |
| `nombre` | CharField (único) | Ej: `Impactrueno` |
| `tipo` | CharField + choices | Tipo del movimiento |
| `potencia` | PositiveInteger | Daño base (0 = de estado) |
| `descripcion` | TextField | Texto explicativo |
| `pokemones` | ManyToMany → Pokemon | Pokémon que la aprenden |

Las **relaciones** claves:

- Un `Pokemon` puede tener muchas `Habilidad` y viceversa (M2M).
- Desde un Pokémon accedes con `pokemon.habilidades.all()`.

---

## ⌨️ Comandos útiles

```bash
# Instalar dependencias
pip install -r requirements.txt

# Migraciones (crear / actualizar tablas)
python manage.py migrate
python manage.py makemigrations   # tras cambiar models.py
python manage.py showmigrations

# Datos de ejemplo
python manage.py seed
python manage.py seed --reset

# Servidor de desarrollo
python manage.py runserver
python manage.py runserver 8001   # puerto alternativo

# Admin
python manage.py createsuperuser

# Pruebas
python manage.py test
python manage.py test pokemon -v 2

# Shell interactiva de Django
python manage.py shell
```

> **Tip:** en el shell puedes explorar la BD con:
> ```python
> from pokemon.models import Pokemon
> Pokemon.objects.count()
> Pokemon.objects.filter(tipo='Fuego')
> ```

---

## 🧪 Pruebas

```bash
python manage.py test
```

Salida esperada:

```
Found 7 test(s).
System check identified no issues (0 silenced).
.......
OK
```

Los tests cubren:

- Modelo: `__str__`, `total_stats`, `tipos_display` (simple y doble)
- Vistas: lista muestra Pokémon, detalle muestra datos, crear vía POST funciona

---

## 🎓 Conceptos de Django que aprenderás

Este proyecto está pensado para estudiar. Revisa los comentarios en español dentro de cada archivo para entender:

| Concepto | Dónde verlo |
|---|---|
| **Modelos** — clases Python → tablas SQL | `pokemon/models.py` |
| **Migraciones** — versionar esquema de BD | `python manage.py migrate` |
| **Vistas basadas en clases (CBV)** — CRUD reutilizable | `pokemon/views.py` |
| **Formularios (ModelForm)** — validación automática | `pokemon/forms.py` |
| **Templates** — HTML con `{% extends %}`, `{% block %}`, `{% url %}` | `pokemon/templates/` |
| **URLs con nombre** — enlazar sin hardcodear rutas | `pokemon/urls.py` |
| **Admin automático** — pero personalizado | `pokemon/admin.py` |
| **Mensajes flash** — feedback tras cada acción | `views.py` + `base.html` |
| **Paginación + filtros** — `paginate_by` y `get_queryset()` | `PokemonListView` |
| **Estáticos** — CSS/JS con `{% load static %}` | `static/` |
| **CSRF** — `{% csrf_token %}` en formularios POST | `formulario.html` |
| **Tests** — verificar modelo y vistas | `pokemon/tests.py` |

---

## 🎨 Personalización

### Cambiar los colores

Edita las variables al inicio de `static/css/style.css`:

```css
:root {
    --pikachu: #FFCB05;    /* amarillo principal */
    --rojo: #E3350D;       /* rojo pokébola */
    --azul: #2A75BB;       /* azul pokedex */
}
```

### Cambiar imágenes de Pokémon

Puedes pegar cualquier URL en el campo *imagen_url* del formulario. Un patrón recomendado (arte oficial):

```
https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/<numero>.png
```

Ejemplo para Pikachu (`25`):

```
https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png
```

### Agregar un Pokémon desde la web

1. Ve a `/crear/`
2. Completa nombre, número, tipo y stats (1–255)
3. (Opcional) pega la URL de la imagen — verás una vista previa
4. Guarda → aparece en la lista con mensaje de éxito

---

## 🔧 Solución de problemas

| Problema | Solución |
|---|---|
| `ModuleNotFoundError: No module named 'django'` | Activa el venv y corre `pip install -r requirements.txt` |
| `Table 'pokemon_pokemon' doesn't exist` | Corre `python manage.py migrate` |
| Puerto ocupado (`Address already in use`) | Usa otro puerto: `python manage.py runserver 8001` o cierra el proceso anterior |
| No se ven las imágenes | Revisa `imagen_url` o usa el patrón de PokeAPI descrito arriba |
| `TemplateSyntaxError` con `block` duplicado | No escribas `{% block ... %}` dentro de comentarios `{# #}` — Django lo interpreta igual |
| Olvidaste tu usuario admin | `python manage.py createsuperuser` (crea uno nuevo) |
| Quieres empezar de cero | `python manage.py seed --reset` recarga los datos de ejemplo |

---

## 🤝 Contribuciones

¿Quieres mejorarlo? ¡Son bienvenidas!

1. Haz un **fork** del repositorio
2. Crea una rama: `git checkout -b mi-mejora`
3. Haz tus cambios y **prueba** con `python manage.py test`
4. Haz `commit` y `push` a tu rama
5. Abre un **Pull Request**

Ideas para mejorar:

- Login de usuarios con equipos propios
- Subida de fotos reales en vez de URLs
- Batallas entre Pokémon basadas en sus stats
- Importación automática desde PokeAPI
- API REST con Django REST Framework

---

## 📄 Licencia y marcas

- Código de este proyecto: **MIT** (úsalo libremente con atribución).
- **Pokémon** y los nombres de los Pokémon son marcas de **Nintendo / Game Freak / Creatures Inc.**
- Las imágenes se cargan desde la API pública de sprites de [PokeAPI](https://pokeapi.co/).
- Proyecto creado con fines **educativos y de aprendizaje** — no afiliado ni respaldado por Nintendo.

---

¡Atrapa 'em all! 🎉
