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
| **Seguridad** | bcrypt + K8s Secrets | 4.3.0 | Hashing criptográfico de contraseñas, usuario no-root y Secrets |
| **Contenedores** | Docker + Docker Compose | v24+ / v2+ | Imágenes multi-capa con etiquetas por versión (`v1.0.0`) y SHA |
| **Orquestación Cloud** | Kubernetes (Minikube) | v1.36+ / v1.39+ | `Namespace`, `ConfigMap`, `Secret`, `PVC`, `StatefulSet`, `Deployments` y `Services` |
| **CI/CD Automatizado** | GitHub Actions | Workflows v4 | Ejecución automática de pruebas con PostgreSQL, control de fallos y build Docker |
| **Pruebas Automatizadas**| Pytest / Playwright / Unittest | 9.x / 1.50+ | Pruebas unitarias, integración y de navegador E2E (20 casos) |

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

### Método 1: Despliegue en Kubernetes / Minikube (Entrega Final DevOps)

**Requisitos:** Docker Desktop / Engine, `minikube` y `kubectl`.

1. **Iniciar el clúster de Minikube y verificar estado (`D4`):**
   ```bash
   minikube start --driver=docker
   minikube status
   kubectl config current-context
   ```

2. **(Opcional) Construir y cargar imágenes locales en Minikube (`D3`):**
   *(Si no tienes conexión a internet o deseas probar cambios locales antes de subirlos a Docker Hub)*
   ```bash
   docker build -t juanexzz/ott-backend:v1.0.0 -t juanexzz/ott-backend:latest ./backend
   docker build -t juanexzz/ott-frontend:v1.0.0 -t juanexzz/ott-frontend:latest ./frontend
   minikube image load juanexzz/ott-backend:latest
   minikube image load juanexzz/ott-frontend:latest
   ```

3. **Aplicar todos los manifiestos declarativos de Kubernetes (`D4`, `D6`, `D7`):**
   ```bash
   kubectl apply -f k8s/
   ```
   Esto crea en orden dentro del namespace `ott-platform`:
   * [`k8s/01-namespace.yaml`](k8s/01-namespace.yaml) — Namespace aislado `ott-platform`.
   * [`k8s/02-configmap-and-secret.yaml`](k8s/02-configmap-and-secret.yaml) — `ConfigMap` (`ott-config`, `ott-db-init` con `init.sql`) y `Secret` (`ott-secrets` con credenciales y `SECRET_KEY`).
   * [`k8s/03-postgres.yaml`](k8s/03-postgres.yaml) — `PersistentVolumeClaim` (`postgres-pvc` de 1Gi), `StatefulSet` (`ott-db`) con probes `pg_isready` y `Service` `ClusterIP` (`5432`).
   * [`k8s/04-backend.yaml`](k8s/04-backend.yaml) — `Deployment` (`ott-backend`) con `readinessProbe` y `livenessProbe` hacia `/api/health`, límites de CPU/Memoria y `Service` `ClusterIP` (`5000`).
   * [`k8s/05-frontend.yaml`](k8s/05-frontend.yaml) — `Deployment` (`ott-frontend`) con probes HTTP y `Service` `NodePort` (`80:30080`).

4. **Verificar recursos saludables y observabilidad (`D4`, `D8`):**
   ```bash
   kubectl get all,pvc,cm,secret -n ott-platform
   kubectl get pods -n ott-platform -o wide
   kubectl logs -n ott-platform deployment/ott-backend
   kubectl describe deployment ott-backend -n ott-platform
   ```

5. **Exponer y abrir la aplicación Web desde Minikube (`D5`):**
   ```bash
   # Opción A: Túnel directo con port-forward (Recomendado en Windows)
   kubectl port-forward svc/ott-frontend -n ott-platform 8080:80
   # Abrir en el navegador: http://localhost:8080
   # Swagger UI:           http://localhost:8080/apidocs/
   # Healthcheck JSON:     http://localhost:8080/api/health

   # Opción B: Servicio nativo de Minikube
   minikube service ott-frontend -n ott-platform
   ```

---

### Método 2: Con Docker Compose (Entorno Contenerizado Local)

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

5. **Comandos útiles de administración:**
   - **Ver logs en tiempo real:** `docker compose logs -f`
   - **Detener los servicios:** `docker compose down`
   - **Reiniciar y restablecer la base de datos a cero:** `docker compose down -v`

---

### Método 3: Ejecución Local en Desarrollo (Sin Docker)

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

El proyecto incluye tres niveles de pruebas automatizadas con un total de 20 casos de prueba automatizados (100% pasando):

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

### 4. Ejecución de la Suite Completa (20/20 pruebas)
Para ejecutar todas las pruebas (unitarias, integración y E2E) con reporte detallado:
```bash
pytest -v
```

---

## 👥 Historias de Usuario y Responsables

El trabajo fue distribuido de manera equitativa entre los integrantes del equipo. Para consultar los criterios de aceptación completos de cada historia, ver el documento [`docs/historias_de_usuario.md`](docs/historias_de_usuario.md).

| ID | Historia de Usuario | Responsable | Estado |
| :--- | :--- | :--- | :--- |
| **HU-01** | Catálogo principal con hero dinámico y filtrado por región | Miguel Ángel Salazar | Entregada |
| **HU-02** | Gestión de "Mi Lista" (agregar y remover películas favoritas) | Miguel Ángel Salazar | Entregada |
| **HU-03** | Contenerización y orquestación con Docker Compose | Juan Esteban Vallejo | Entregada |
| **HU-04** | Base de datos relacional y scripts de inicialización (`init.sql`) | Juan Esteban Vallejo | Entregada |
| **HU-05** | Autenticación de usuarios con contraseñas seguras (`bcrypt`) | Tomás Sepúlveda | Entregada |
| **HU-06** | Perfil de usuario y actualización de planes de suscripción | Tomás Sepúlveda | Entregada |
| **HU-07** | Reproductor de video interactivo con guardado de progreso | Sebastián Villa | Entregada |
| **HU-08** | Calificaciones (Like/Dislike) y motor de búsqueda en tiempo real | Sebastián Villa | Entregada |

---

## 📑 Documentación y Entregables del Proyecto

Para la revisión académica y entrega final, la documentación del proyecto se encuentra consolidada en la carpeta `docs/`:

* **Ficha Técnica Oficial (Excel):** [`docs/Ficha_Tecnica_Proyecto_Cinefilo.xlsx`](docs/Ficha_Tecnica_Proyecto_Cinefilo.xlsx) — Libro con información técnica consolidada, integrantes, arquitectura multicontenedor y plan de HU.
* **Ficha Técnica (Markdown):** [`docs/ficha_tecnica.md`](docs/ficha_tecnica.md)
* **Ficha Técnica (CSV):** [`docs/ficha_tecnica.csv`](docs/ficha_tecnica.csv)
* **Historias de Usuario y Criterios de Aceptación:** [`docs/historias_de_usuario.md`](docs/historias_de_usuario.md)
* **Guía de Sustentación Final y Checklist DevOps:** [`docs/guia_sustentacion_final.md`](docs/guia_sustentacion_final.md)

---

## 🔄 Cadena de Entrega Continua (CI/CD) y Trazabilidad (`D2`, `D3`, `D6`)

El repositorio cuenta con el pipeline automatizado [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml) que conecta cada cambio desde Git hasta el clúster:

```
[ git push / PR ]
       │
       ▼
[ Job 1: CI - Pruebas Unitarias e Integración ]
  • Levanta contenedor de servicio postgres:16-alpine
  • Carga esquema y semillas (database/init.sql)
  • Ejecuta test_unit.py (10 pruebas) + test_flow.py (4 pruebas)
  • Control de fallos: si una prueba falla, bloquea el Job 2
       │
       ▼ (needs: unit-and-integration-tests)
[ Job 2: Build, Tagging Trazable & Docker Hub ]
  • Genera etiquetas trazables: v1.0.0, sha-<commit>, latest
  • Construye juanexzz/ott-backend y juanexzz/ott-frontend
  • Publica en Docker Hub y valida manifiestos en k8s/
       │
       ▼
[ Despliegue Declarativo en Minikube (k8s/) ]
  • kubectl apply -f k8s/ reconcilia el estado deseado en el clúster
```

Para comprobar la correspondencia exacta de la imagen desplegada en vivo (`D6`):
```bash
git rev-parse --short HEAD
kubectl get pods -n ott-platform -o jsonpath="{range .items[*]}{.metadata.name}{'\t'}{.spec.containers[*].image}{'\t'}{.status.containerStatuses[*].imageID}{'\n'}{end}"
```

---

## 📦 Estructura del Repositorio

```
OTT-/
├── .github/
│   └── workflows/
│       └── ci-cd.yml         # Pipeline CI/CD en GitHub Actions (Tests + Docker Build/Push)
├── k8s/                      # Manifiestos declarativos de Kubernetes (Minikube)
│   ├── 01-namespace.yaml     # Namespace aislado ott-platform
│   ├── 02-configmap-and-secret.yaml # ConfigMaps (config + init.sql) y Secrets
│   ├── 03-postgres.yaml      # PVC (1Gi), StatefulSet y Service de PostgreSQL 16
│   ├── 04-backend.yaml       # Deployment (probes + resources) y Service de Flask
│   └── 05-frontend.yaml      # Deployment (probes + resources) y Service NodePort de Nginx
├── backend/                  # Código de la aplicación Flask
│   ├── config/               # Configuración de base de datos
│   ├── controllers/          # Controladores MVC (auth, home, movie, api, etc.)
│   ├── database/             # Scripts de base de datos auxiliares
│   ├── models/               # Modelos de dominio (Movie)
│   ├── services/             # Lógica de negocio (auth, movies, ratings, etc.)
│   ├── static/               # Activos estáticos (posters, videos, css, js)
│   ├── templates/            # Vistas Jinja2 (HTML)
│   ├── app.py                # Punto de entrada de la aplicación Flask y Swagger
│   ├── Dockerfile            # Dockerfile con Python 3.11-slim, usuario no-root y HEALTHCHECK
│   └── requirements.txt      # Dependencias de Python
├── frontend/                 # Servicio de Frontend y Proxy Inverso
│   ├── static/               # Archivos estáticos servidos por Nginx
│   ├── nginx.conf.template   # Plantilla de configuración de Nginx
│   └── Dockerfile            # Dockerfile para Nginx 1.25-alpine con HEALTHCHECK
├── database/
│   ├── init.sql              # Esquema de tablas y datos semilla de PostgreSQL
│   └── watch_history_local.json # Historial de reproducción inicial y respaldo local
├── docs/
│   ├── guia_sustentacion_final.md # Guion paso a paso de Pitch + Demo + Checklist Excel
│   ├── historias_de_usuario.md # Documentación detallada de HU y responsables
│   ├── ficha_tecnica.md       # Ficha técnica del proyecto en Markdown
│   ├── ficha_tecnica.csv      # Ficha técnica en formato de hoja de cálculo CSV
│   └── Ficha_Tecnica_Proyecto_Cinefilo.xlsx # Ficha técnica oficial en formato Excel
├── tests/
│   ├── test_unit.py          # Pruebas unitarias de modelos, seguridad y rutas
│   ├── test_flow.py          # Prueba del flujo de comunicación completo
│   └── test_e2e_playwright.py# Pruebas de navegador automatizadas con Playwright
├── docker-compose.yml        # Orquestación de servicios (db, backend, frontend)
├── .env.example              # Plantilla de variables de entorno
├── .gitignore                # Archivos y carpetas excluidas de Git
└── README.md                 # Documentación general del proyecto
```
