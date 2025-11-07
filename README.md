Proyecto: gestion_de_adopciones
----------------------------------
Este es un scaffold Django que utiliza procedures en PostgreSQL para realizar CRUD.
Instrucciones rápidas:

1) Crear entorno virtual y activar:
   python -m venv venv
   source venv/bin/activate   (Windows: venv\Scripts\activate)

2) Instalar dependencias:
   pip install -r requirements.txt

3) Crear base de datos en PostgreSQL (ejecutar el SQL que te entregué previamente):
   - Ejecuta el script SQL que crea las tablas y procedures (gestion_adopciones.sql)
   - Asegúrate de que la DB y los procedimientos existan.

4) Configurar variables de entorno (opcional):
   export POSTGRES_DB=gestion_adopciones
   export POSTGRES_USER=postgres
   export POSTGRES_PASSWORD=tu_password
   export POSTGRES_HOST=localhost
   export POSTGRES_PORT=5432

5) Ejecutar migraciones básicas y crear superuser:
   python manage.py migrate
   python manage.py createsuperuser

6) Ejecutar servidor:
   python manage.py runserver

Nota: Este proyecto llama a stored procedures ya existentes en la DB; no se incluye una migration para crearlos.
