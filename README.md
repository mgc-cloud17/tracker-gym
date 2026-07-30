# 🏋️ Gym Tracker - Web Application

Una aplicación web interactiva para el seguimiento de entrenamientos en el gimnasio, cálculo de volumen de carga y registro de récords personales por usuario.

Desarrollada como proyecto de práctica enfocado en arquitectura web, autenticación segura y persistencia de datos relacionales.

---

## 🚀 Características Principales

* **Autenticación Segura de Usuarios:** Sistema de registro e inicio de sesión con sesiones cifradas (`Flask-Session`) y contraseñas encriptadas mediante *hashing* (`Werkzeug`).
* **Aislamiento de Datos:** Cada usuario gestiona únicamente su propio historial de entrenamientos y estadísticas.
* **Gestión de Entrenamientos (CRUD):** Registro de ejercicios (peso, repeticiones, fecha personalizable) y eliminación de series.
* **Métricas y Estadísticas:**
  * **Volumen Total:** Cálculo automático del tonelaje movido en kg (`∑ peso × repeticiones`).
  * **Récords Personales (PRs):** Identificación automática del peso máximo levantado por cada ejercicio.
* **Interfaz Adaptativa:** Diseño en modo oscuro (*Dark Mode*) fluido y receptivo.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3, Flask.
* **Base de Datos:** SQLite 3 (a través de la librería `cs50`).
* **Frontend:** HTML5, CSS3 (Custom Flexbox & Modifiers).
* **Seguridad:** Werkzeug (`generate_password_hash`, `check_password_hash`).

---

## ⚙️ Instalación y Configuración Local

Si deseas ejecutar este proyecto en tu máquina local, sigue estos pasos:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/tracker-gym.git](https://github.com/TU_USUARIO/tracker-gym.git)
cd tracker-gym

### 2. Instalar dependecias

Asegúrate de tener Python 3.x instalado. Luego ejecuta:

pip install flask cs50 werkzeug

### 3. Inicializar la Base de Datos

Crea el archivo vacío e inicializa la estructura de las tablas:

touch gym.db
python crear_db.py

### 4. Iniciar la aplicación

python -m flask run


Accede a la aplicación desde tu navegador en http://127.0.0.1:5000.

### 📸 Estructura de la Base de Datos

El sistema utiliza una arquitectura relacional simple conectando dos tablas mediante llave foránea (FOREIGN KEY):

usuarios: id, usuario, hash

entrenamientos: id, usuario_id, ejercicio, peso, repeticiones, fecha

💡 Nota: Recuerda cambiar TU_USUARIO en la URL del comando git clone por tu usuario real de GitHub.

---

### 📤 Para terminar y subirlo a GitHub:

Una vez que guardes el archivo `README.md`, solo ejecuta en tu Git Bash:

```bash
git add .
git commit -m "Docs: Add full README documentation"
git push