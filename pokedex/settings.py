"""
Configuración del proyecto Pokedex.

Django está construido sobre "apps". Cada app se registra aquí
en INSTALLED_APPS. Los templates, la base de datos (SQLite por
simplicidad) y los archivos estáticos (CSS/JS) se configuran aquí.
"""
from pathlib import Path

# BASE_DIR apunta a la raíz del proyecto (carpeta que contiene manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ Solo para desarrollo local. Nunca subas SECRET_KEY a producción real.
SECRET_KEY = 'django-insecure-pokedex-dev-key-12345'

# En True acepta cualquier host (útil en desarrollo). En producción pon tu dominio.
DEBUG = True
ALLOWED_HOSTS = ['*']

# Lista de aplicaciones que carga Django.
# Las primeras 5 son las que trae Django ya hechas (admin, auth, etc.).
# Al final agregamos nuestra app 'pokemon'.
INSTALLED_APPS = [
    'django.contrib.admin',       # Panel de administrador.
    'django.contrib.auth',        # Sistema de usuarios / login.
    'django.contrib.contenttypes',# Tabla para permisos genéricos.
    'django.contrib.sessions',    # Sesiones (para carrito, login, etc.).
    'django.contrib.messages',    # Mensajes flash ("¡Pokémon creado!").
    'django.contrib.staticfiles', # Sirve CSS/JS en desarrollo.
    'pokemon',                    # <-- ¡NUESTRA APP!
]

# Middleware: capas que procesan cada petición HTTP antes de llegar a la vista.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Protege contra ataques CSRF en formularios.
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Archivo principal de URLs: aquí Django busca las rutas.
ROOT_URLCONF = 'pokedex.urls'

# Configuración de templates (HTML). Django busca carpetas "templates".
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Carpetas extra para templates (lo dejamos por defecto).
        'APP_DIRS': True,  # Busca templates dentro de cada app (pokemon/templates/...).
        'OPTIONS': {
            # Funciones que estarán disponibles en todos los templates.
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Apunta a la función WSGI que usa el servidor web.
WSGI_APPLICATION = 'pokedex.wsgi.application'

# Base de datos: usamos SQLite (un solo archivo db.sqlite3). Ideal para aprender.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseñas (para el admin si creas usuarios).
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Idioma y zona horaria.
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS, JS, imágenes).
STATIC_URL = 'static/'

# Carpeta donde Django buscará archivos estáticos adicionales (CSS global).
STATICFILES_DIRS = [BASE_DIR / 'static']

# Dónde redirigir después de login/logout en el admin.
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/login/'

# Clave primaria por defecto.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
