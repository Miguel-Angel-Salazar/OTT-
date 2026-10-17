# 🎬 Proyecto OTT - Clon de MUBI
### Materia: Paradigmas de Programación — Entrega 2 y Final

Plataforma de streaming de video bajo demanda (OTT), inspirada en el diseño, curaduría y funcionamiento de MUBI. El proyecto implementa una arquitectura Modelo-Vista-Controlador (MVC), persistencia relacional en PostgreSQL, renderizado en servidor con Jinja2, documentación Swagger/OpenAPI, proxy inverso con Nginx y despliegue modular con Docker Compose.

---

## 💻 Tecnologías y Versiones Utilizadas

| Componente | Tecnología | Versión | Rol en el Sistema |
| :--- | :--- | :--- | :--- |
| **Backend** | Python / Flask | Python 3.11 / Flask 3.1.1 | Servidor de aplicaciones, lógica de negocio y SSR |
| **Documentación API** | Flasgger (OpenAPI/Swagger) | 0.9.7.1 | Especificación OpenAPI y Swagger UI interactivo |
| **Base de Datos** | PostgreSQL Alpine | 16-alpine | Base de datos relacional con integridad referencial |
| **Frontend / Proxy** | Nginx Alpine | 1.25-alpine | Proxy inverso, compresión y entrega de estáticos |
| **Seguridad** | bcrypt | 4.3.0 | Hashing y salting criptográfico de contraseñas |
| **Orquestación** | Docker Compose | v2+ | Contenerización y redes internas entre servicios |
| **Pruebas Automatizadas**| Playwright / Unittest | 1.50+ | Pruebas unitarias y pruebas de navegador E2E |

---

## 🏗️ Arquitectura y Comunicación entre Componentes

```
       [ Cliente / Navegador Web ]
                    │
                    ▼ (Puerto 80)
        ┌───────────────────────┐
        │   frontend (Nginx)    │
        │ ───────────────────── │
        │  /static/* ──► Caché  │
        │  /*        ──► Proxy  │
        └───────────┬───────────┘
                    │ (Red interna Docker - Puerto 5000)
                    ▼
        ┌───────────────────────┐
        │    backend (Flask)    │
        │  • Blueprints MVC     │
        │  • Swagger (/apidocs) │
        └───────────┬───────────┘
                    │ (Red interna Docker - Puerto 5432)
                    ▼
        ┌───────────────────────┐
        │   db (PostgreSQL 16)  │
        │  • init.sql (Seeds)   │
        └───────────────────────┘
```

1. **Frontend (`nginx:1.25-alpine`):** Recibe las solicitudes en el puerto 80. Si la ruta solicita un recurso estático (`/static/*`), lo sirve directamente desde el disco con encabezados de caché. Cualquier otra solicitud se redirige al backend vía HTTP.
2. **Backend (`python:3.11-slim + Flask`):** Procesa la solicitud a través del controlador correspondiente, valida sesiones, interactúa con la base de datos y renderiza la plantilla Jinja2 o retorna respuestas JSON (en `/api/*` y `/apidocs/`).
3. **Base de Datos (`postgres:16-alpine`):** Almacena de forma persistente usuarios, perfiles, películas, favoritos, historial y calificaciones, inicializándose automáticamente con el script `database/init.sql`.

---

## 📥 Cómo Descargar el Proyecto

### Opción A: Clonar el Repositorio de Código (Recomendado)
```bash
git clone https://github.com/Miguel-Angel-Salazar/OTT-.git
cd OTT-
```

### Opción B: Descargar las Imágenes desde Docker Hub
Las imágenes precompiladas del equipo están disponibles en Docker Hub:
```bash
docker pull juanexzz/ott-backend:latest
docker pull juanexzz/ott-frontend:latest
docker pull postgres:16-alpine
```

---

## 🚀 Instalación y Ejecución

### Método 1: Con Docker Compose (Entorno Contenerizado)

**Requisitos:** Docker Desktop (Windows/Mac) o Docker Engine + Compose v2 (Linux).

1. **Configurar el archivo de entorno:**
   ```bash
   cp .env.example .env
   # En Windows PowerShell:
   Copy-Item .env.example .env
   ```

2. **Levantar los tres servicios:**
   ```bash
   docker compose up -d
   ```

3. **Verificar que los contenedores estén corriendo:**
   ```bash
   docker compose ps
   ```

4. **Acceder a la aplicación:**
   - **Frontend / Aplicación Web:** [http://localhost](http://localhost) (puerto 80)
   - **Documentación Swagger UI:** [http://localhost/apidocs/](http://localhost/apidocs/)
   - **Healthcheck del Sistema:** [http://localhost/api/health](http://localhost/api/health)

---

### Método 2: Ejecución Local en Desarrollo (Sin Docker)

**Requisitos:** Python 3.11+, PostgreSQL 14+ local.

1. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   # En Linux/Mac:
   source .venv/bin/activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r backend/requirements.txt
   pip install playwright pytest
   playwright install chromium
   ```

3. **Configurar la base de datos en `.env`:**
   Asegurar que la variable `DATABASE_URL` apunte a tu PostgreSQL local:
   ```env
   DATABASE_URL=postgresql://usuario:password@localhost:5432/ott_db
   SECRET_KEY=clave_secreta_para_sesiones
   ```

4. **Inicializar tablas y datos semilla (si es la primera vez):**
   ```bash
   python backend/database/init_db.py
   ```

5. **Iniciar el servidor Flask:**
   ```bash
   python backend/app.py
   ```
   Disponible en: [http://localhost:5000](http://localhost:5000) y Swagger en [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/).

---

## 👤 Cuentas de Prueba Preconfiguradas

La base de datos precarga automáticamente usuarios de prueba para evaluar los distintos roles y regiones:

| Correo | Contraseña | Perfil | Suscripción | Región |
| :--- | :--- | :--- | :--- | :--- |
| `admin@ott.com` | `admin123` | Administrador MUBI | Premium | LATAM |
| `demo@ott.com` | `demo123` | Cinéfilo Demo | Básica | LATAM |

*Nota: También es posible registrar nuevos usuarios directamente desde `/auth/register`.*

---

## 📖 Documentación Swagger (OpenAPI)

El backend incorpora Swagger UI para la inspección y prueba interactiva de los endpoints del sistema.

* **URL de acceso:** `http://localhost/apidocs/` (o `http://localhost:5000/apidocs/`)
* **Especificación OpenAPI (JSON):** `http://localhost/apispec.json`

### Endpoints documentados principales:
* `GET /api/health` — Comprueba la salud del backend y la conexión activa con PostgreSQL.
* `GET /api/movies` — Listado completo del catálogo en formato JSON.
* `GET /api/movies/{id}` — Detalle de una película en formato JSON.
* `POST /movie/{id}/progreso` — Guarda el segundo actual de visualización del usuario.
* `POST /favorite/toggle/{id}` — Alterna el estado de una película en la lista de favoritos.
* `POST /auth/login` y `POST /auth/register` — Endpoints de autenticación de usuarios.

---

## 🧪 Pruebas Automatizadas

El proyecto incluye dos niveles de pruebas automatizadas:

### 1. Pruebas Unitarias y de Lógica de Negocio
Evalúan el modelo `Movie`, la normalización de rutas, el hashing con `bcrypt`, el filtrado regional y los endpoints HTTP clave:
```bash
python -m unittest discover tests -p "test_unit.py"
```

### 2. Prueba del Flujo Completo de Comunicación (Frontend <-> Backend <-> DB)
Verifica la integración real entre el backend y la base de datos (healthcheck, lectura de catálogo, login y persistencia):
```bash
python -m unittest tests/test_flow.py
```

### 3. Pruebas End-to-End (E2E) con Playwright
Valida las funcionalidades críticas directamente sobre el navegador (renderizado de login, login fallido, login exitoso con navegación al catálogo, detalle de película con reproductor, buscador y Swagger UI):
```bash
python -m unittest tests/test_e2e_playwright.py
```
*(Opcionalmente se puede ejecutar con `pytest tests/test_e2e_playwright.py`)*

---

## 👥 Historias de Usuario y Responsables

El trabajo fue distribuido de manera equitativa entre los integrantes del equipo. Para consultar los criterios de aceptación completos de cada historia, ver el documento [`docs/historias_de_usuario.md`](docs/historias_de_usuario.md).

| ID | Historia de Usuario | Responsable | Estado |
| :--- | :--- | :--- | :--- |
| **HU-01** | Catálogo principal con hero dinámico y filtrado por región | Miguel Ángel Salazar | Entregada |
| **HU-02** | Gestión de "Mi Lista" (agregar y remover películas favoritas) | Miguel Ángel Salazar | Entregada |
| **HU-03** | Contenerización y orquestación con Docker Compose | Juan Esteban Vallejo | Entregada |
| **HU-04** | Base de datos relacional y scripts de inicialización (`init.sql`) | Juan Esteban Vallejo | Entregada |
| **HU-05** | Autenticación de usuarios con contraseñas seguras (`bcrypt`) | Tomas sepulveda  | Entregada |
| **HU-06** | Perfil de usuario y actualización de planes de suscripción | Tomas sepulverda | Entregada |
| **HU-07** | Reproductor de video interactivo con guardado de progreso | Sebastián Villa | Entregada |
| **HU-08** | Calificaciones (Like/Dislike) y motor de búsqueda en tiempo real | Sebastián Villa | Entregada |

---

## 📦 Estructura del Repositorio

```
OTT-/
├── backend/                  # Código de la aplicación Flask
│   ├── config/               # Configuración de base de datos
│   ├── controllers/          # Controladores MVC (auth, home, movie, api, etc.)
│   ├── database/             # Scripts de base de datos auxiliares
│   ├── models/               # Modelos de dominio (Movie)
│   ├── services/             # Lógica de negocio (auth, movies, ratings, etc.)
│   ├── static/               # Activos estáticos (posters, videos, css, js)
│   ├── templates/            # Vistas Jinja2 (HTML)
│   ├── app.py                # Punto de entrada de la aplicación Flask y Swagger
│   ├── Dockerfile            # Dockerfile para Python 3.11-slim
│   └── requirements.txt      # Dependencias de Python
├── frontend/                 # Servicio de Frontend y Proxy Inverso
│   ├── static/               # Archivos estáticos servidos por Nginx
│   ├── nginx.conf.template   # Plantilla de configuración de Nginx
│   └── Dockerfile            # Dockerfile para Nginx Alpine
├── database/
│   └── init.sql              # Esquema de tablas y datos semilla de PostgreSQL
├── docs/
│   ├── historias_de_usuario.md # Documentación detallada de HU y responsables
│   ├── ficha_tecnica.md       # Ficha técnica del proyecto en Markdown
│   └── ficha_tecnica.csv      # Ficha técnica en formato de hoja de cálculo CSV
├── tests/
│   ├── test_unit.py          # Pruebas unitarias de modelos, seguridad y rutas
│   ├── test_flow.py          # Prueba del flujo de comunicación completo
│   └── test_e2e_playwright.py# Pruebas de navegador automatizadas con Playwright
├── docker-compose.yml        # Orquestación de servicios (db, backend, frontend)
├── .env.example              # Plantilla de variables de entorno
├── .gitignore                # Archivos y carpetas excluidas de Git
└── README.md                 # Documentación general del proyecto
```
