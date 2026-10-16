# 🎬 Proyecto OTT - Clon de MUBI (Paradigmas de Programación)

Prototipo funcional de una plataforma de streaming de video bajo demanda (OTT), inspirada en el diseño, curaduría y funcionamiento de MUBI. El proyecto implementa una arquitectura MVC con renderizado en el servidor (SSR), base de datos relacional PostgreSQL, proxy inverso de alto rendimiento y despliegue completamente dockerizado.

---

## 🏗️ Arquitectura del Sistema

El proyecto está diseñado bajo una arquitectura de microservicios contenerizados orquestados con **Docker Compose**:

1. **`db` (PostgreSQL 16 Alpine):**
   - Base de datos relacional directa.
   - Inicialización automática mediante script SQL (`database/init.sql`) con esquema completo y datos semilla (usuarios, perfiles, catálogo de 20 películas/series, favoritos, historial y calificaciones).
   - Volumen persistente para datos (`postgres_data`).
2. **`backend` (Python 3.11-slim + Flask):**
   - API y renderizado del lado del servidor con Jinja2.
   - Autenticación segura mediante `bcrypt`.
   - Controladores modulares por Blueprints (`auth`, `home`, `movie`, `profile`, `favorite`).
   - Imagen en Docker Hub: [`juanexzz/ott-backend:latest`](https://hub.docker.com/r/juanexzz/ott-backend)
3. **`frontend` (Nginx Alpine):**
   - Servidor web estático y Proxy Inverso (Reverse Proxy).
   - Sirve directamente archivos estáticos (CSS, JS, imágenes y videos MP4) con compresión y caché de alto rendimiento.
   - Redirige peticiones dinámicas al backend mediante la variable `BACKEND_URL`.
   - Imagen en Docker Hub: [`juanexzz/ott-frontend:latest`](https://hub.docker.com/r/juanexzz/ott-frontend)

```
       [ Cliente / Navegador ]
                 │
                 ▼ (Puerto 80)
     ┌────────────────────────┐
     │   frontend (Nginx)     │
     │ ────────────────────── │
     │  /static/* ──► Cache   │
     │  /*        ──► Proxy   │
     └───────────┬────────────┘
                 │ (Puerto 5000)
                 ▼
     ┌────────────────────────┐
     │    backend (Flask)     │
     └───────────┬────────────┘
                 │ (Puerto 5432)
                 ▼
     ┌────────────────────────┐
     │   db (PostgreSQL 16)   │
     └────────────────────────┘
```

---

## 🚀 Despliegue Rápido con Docker Compose

### Prerrequisitos
- Tener instalado **Docker** y **Docker Compose** (ej. Docker Desktop en Windows/Mac o docker-ce en Linux).

### Pasos para Ejecutar

1. **Clonar el repositorio y situarse en la raíz:**
   ```bash
   git clone https://github.com/Miguel-Angel-Salazar/OTT-.git
   cd OTT-
   git checkout docker-integration
   ```

2. **Configurar las variables de entorno:**
   Copia el archivo de ejemplo `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   # En Windows PowerShell:
   Copy-Item .env.example .env
   ```

3. **Levantar la plataforma:**
   ```bash
   docker compose up -d
   ```
   *Nota:* Docker descargará las imágenes oficiales y de Docker Hub, creará la base de datos, correrá las migraciones y datos semilla automáticamente, y levantará todos los servicios.

4. **Acceder a la aplicación:**
   Abre tu navegador en:
   - **Frontend principal:** [http://localhost](http://localhost) (o puerto 80)
   - **Backend directo (opcional):** [http://localhost:5000](http://localhost:5000)
   - **Base de datos PostgreSQL (opcional):** `localhost:5432`

---

## 👤 Cuentas de Prueba Preconfiguradas

La base de datos se inicializa automáticamente con los siguientes usuarios listos para iniciar sesión:

| Usuario | Contraseña | Rol / Perfil | Suscripción | Región |
| :--- | :--- | :--- | :--- | :--- |
| `admin@ott.com` | `admin123` | Administrador MUBI | Premium | LATAM |
| `demo@ott.com` | `demo123` | Cinéfilo Demo | Básica | LATAM |

*También puedes registrar nuevos usuarios directamente desde la interfaz web.*

---

## 🛠️ Comandos de Administración Docker

- **Ver el estado de los servicios:**
  ```bash
  docker compose ps
  ```

- **Ver los logs en tiempo real:**
  ```bash
  docker compose logs -f
  # O de un servicio específico:
  docker compose logs -f backend
  ```

- **Detener los contenedores:**
  ```bash
  docker compose down
  ```

- **Detener y limpiar volúmenes (reiniciar la BD a cero):**
  ```bash
  docker compose down -v
  ```

- **Construir localmente las imágenes (desarrollo):**
  ```bash
  docker compose build
  # O individualmente:
  docker build -t juanexzz/ott-backend:latest ./backend
  docker build -t juanexzz/ott-frontend:latest ./frontend
  ```

---

## 📦 Estructura del Repositorio

```
OTT-/
├── backend/                  # Código de la aplicación Flask
│   ├── config/               # Conexión a PostgreSQL
│   ├── controllers/          # Controladores Blueprints (auth, home, movie, etc.)
│   ├── database/             # Modelos y scripts auxiliares
│   ├── models/               # Clases y modelos de dominio
│   ├── services/             # Lógica de negocio y consultas SQL directas
│   ├── static/               # Assets locales del backend
│   ├── templates/            # Plantillas Jinja2 (vistas HTML)
│   ├── app.py                # Entrada principal de la app Flask
│   ├── Dockerfile            # Dockerfile para Python 3.11-slim
│   └── requirements.txt      # Dependencias de Python
├── frontend/                 # Servicio de Frontend y Reverse Proxy
│   ├── static/               # Archivos estáticos servidos por Nginx (CSS, JS, videos, posters)
│   ├── nginx.conf.template   # Plantilla con sustitución de variables de entorno
│   └── Dockerfile            # Dockerfile para Nginx Alpine
├── database/
│   └── init.sql              # Script SQL de creación de tablas y datos semilla
├── .dockerignore             # Exclusión de archivos en contexto de build
├── .env.example              # Plantilla de variables de entorno
├── docker-compose.yml        # Orquestación de servicios (db, backend, frontend)
└── README.md                 # Documentación del proyecto
```