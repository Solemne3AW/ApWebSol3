# Solemne 3 Aplicaciones y Tecnologías WEB - Sistema de Gestión de Citas Médicas

Este proyecto es una aplicación web sencilla construida con Django, como parte del marco evaluativo de la Universidad San Sebastián, que simula la gestión de citas médicas. Permite registrar pacientes, médicos y citas, además de gestionar el estado de cada cita.

---

## 🚀 Tecnologías Utilizadas

*   Python 3.9
*   Django
*   PostgreSQL (para despliegue con Docker)
*   Docker y Docker Compose

---

## 📥 Instalación y Ejecución Local

1.  **Clonar el repositorio**
    ```bash
    git clone https://github.com/Solemne3AW/ApWebSol3.git
    cd ApWebSol3
    ```
2.  **Crear un entorno virtual**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3.  **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Aplicar migraciones**
    ```bash
    python manage.py migrate
    ```
5.  **Crear un superusuario**
    ```bash
    python manage.py createsuperuser
    ```
6.  **Ejecutar el servidor**
    ```bash
    python manage.py runserver
    ```
    Accede a la aplicación en: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🐳 Ejecución con Docker

1.  **Modificar `mysite/settings.py`**
    Asegúrate de que la configuración de la base de datos en `mysite/settings.py` esté configurada para PostgreSQL y apunte al servicio `db` de Docker Compose:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'medical_db',
            'USER': 'user',
            'PASSWORD': 'pass',
            'HOST': 'db',  # Este es el nombre del servicio de la base de datos en docker-compose
            'PORT': '5432',
        }
    }
    ```

2.  **Construir y levantar los contenedores**
    Asegúrate de estar en la raíz del proyecto donde se encuentran `Dockerfile` y `docker-compose.yml`.
    ```bash
    docker-compose up -d
    ```
3.  **Crear un superusuario (dentro del contenedor web)**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
4.  **Acceder a la aplicación**
    *   Panel de Administración: [http://localhost:8000/admin/](http://localhost:8000/admin/)
    *   Lista de Citas: [http://localhost:8000/appointments/](http://localhost:8000/appointments/)

5.  **Detener los contenedores**
    ```bash
    docker-compose down
    ```
