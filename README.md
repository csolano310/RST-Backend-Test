# ✅ To-Do App – Full Stack con Django + Vue + JWT

Aplicación web simple de gestión de tareas con funcionalidades completas de autenticación, CRUD de tareas y filtrado.

---

## 🛠 Tecnologías usadas

### Back-End:
- Python 3.x
- Django 4.x
- Django REST Framework
- CORS Headers

### Front-End:
- Vue 3 + Composition API
- Vue Router
- Axios
- Bootstrap 5

---

## 🔐 Funcionalidades

- Registro e inicio de sesión con JWT
- CRUD de tareas (crear, listar, editar, eliminar)
- Filtro de tareas por estado (pendiente / completada)
- Protección de rutas y tareas por usuario
- Interfaz responsiva con Bootstrap

---

## ⚙️ Instalación y ejecución

### 1. Clonar el repositorio

### BACK-END

**1. Desde el mismo bash, abrir la carpeta de back del repositorio**

cd ToDoApp

**2. Crear entorno virtual para arrancar la app**

python -m venv env
source env/bin/activate 

**3. Instalar librerías con el archivo requirements.txt**

Dentro de la carpeta del back, se encuentra el archivo requirements.txt para poder instalar las librerías necesarias para la ejecución del proyecto.

Ejecutar el comando:

pip install -r requirements.txt

**4. Migrar Bases de datos**

Dentro del archivo .env se encuentran las diferentes configuraciones de variables globales para poder realizar las diferentes conexiones a base de datos y a servidor SMTP para envío de correo de confirmación de registro; configurar dichos valores con los servidos de preferencia.

Una vez configurados las conexiones, se debe realizar la respectiva migración, para esto se debe ejecutar.

python manage.py makemigrations
python manage.py migrate

**5. Iniciar el servidor **

Ejecutar el comando:

python manage.py runserver

El API ya se encuentra disponible para que pueda ser consumida, se pueden consumir las API con postman si se quiere realizar las pruebas de cada endpoints de las misma.
