# Portal Inmobiliario Coquimbo

Aplicación web Django para consultar propiedades y zonas de la región. Los datos de ejemplo se guardan en archivos JSON dentro de `data/`.

## Requisitos

- Python 3.12 o superior
- pip

## Instalación local

Desde la carpeta del proyecto, ejecuta en PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abre <http://127.0.0.1:8000/>. Rutas principales: `/propiedades/`, `/zonas/` y `/admin/`.

En desarrollo, Django usa valores locales predeterminados. Para otros entornos configura estas variables antes de iniciar la aplicación:

- `DJANGO_DEBUG`: `false` fuera del entorno local.
- `DJANGO_SECRET_KEY`: clave secreta única y privada. Puedes generar una con `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`.
- `DJANGO_ALLOWED_HOSTS`: nombres de host permitidos separados por comas, por ejemplo `mi-dominio.cl,www.mi-dominio.cl`.

No publiques claves reales ni archivos `.env`. El archivo SQLite local se excluye de Git; cada instalación crea su propia base ejecutando `python manage.py migrate`.

## Pruebas y comprobaciones

```powershell
python manage.py test
python manage.py check
```

## Subir a GitHub

1. Instala Git para Windows si `git --version` no funciona y abre una terminal nueva.
2. Crea un repositorio vacío en GitHub, sin README, licencia ni `.gitignore` generados por GitHub.
3. Desde esta carpeta, inicializa y revisa los archivos antes del primer commit:

```powershell
git init
git add .
git status --short
git commit -m "Initial project version"
git branch -M main
git remote add origin https://github.com/USUARIO/REPOSITORIO.git
git push -u origin main
```

Sustituye `USUARIO/REPOSITORIO` por la dirección del repositorio creado. Antes de confirmar, revisa que `git status` no muestre el entorno virtual, la base de datos ni secretos.