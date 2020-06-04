# canvas_project_api
Web Canvas project's REST API with Django, DRF, DRF-JWT and Guardian.

## Levantar el proyecto
1. Para levantar el proyecto se recomienda crear un ambiente virtual con virtualenv.
2. Se debe tener una base de datos Postgres en localhost o configurar una base de datos en el canvasAPI/settings.py
3. Luego correr la instrucción `pip install -r requirements.txt` para instalar dependencias.
4. Hacer migraciones con `python manage.py makemigrations`.
5. Hacer migraciones con `python manage.py migrate`.
6. Cargar data para prueba con `python manage.py loaddata bd.json`.
7. Correr el servidor en localhost `python manage.py runserver`.

