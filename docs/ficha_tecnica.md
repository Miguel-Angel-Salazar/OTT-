# FICHA TÉCNICA DEL PROYECTO — Gestión de la Configuración
## Proyecto Semestral: CINÉFILO (Plataforma OTT)
**Fecha de actualización:** Octubre 2026 — Segunda Entrega y Estado de Consolidación

---

### 1. Identificación y Contexto

| Campo | Información Registrada |
| :--- | :--- |
| **Nombre del proyecto \*** | **CINÉFILO** (Clon OTT MUBI) |
| **Semestre / Grupo \*** | 2026-2 / Gestión de la Configuración |
| **Contexto del proyecto \*** | Proyecto académico iniciado en *Paradigmas de Programación* y continuado en *Gestión de la Configuración* para su versionado, contenerización, automatización de pruebas y despliegue modular. |
| **Problema que aborda \*** | Implementar una arquitectura web desacoplada en tres capas (MVC), con persistencia relacional nativa en PostgreSQL, sesiones seguras mediante hashing criptográfico y renderizado del lado del servidor (SSR), eliminando dependencias externas cerradas y garantizando portabilidad mediante contenedores Docker. |
| **Estado actual \*** | **Funcional, Contenerizado y Probado al 100%** |
| **Descripción general \*** | Plataforma web de streaming de video bajo demanda con arquitectura contenerizada multi-servicio: frontend en Nginx (Reverse Proxy y caché de estáticos), backend en Python/Flask con arquitectura MVC y Swagger/OpenAPI, y base de datos relacional PostgreSQL con inicialización automatizada (`init.sql`) y catálogo de 20 producciones con video y metadatos reales. |
| **Usuarios objetivo / Actores** | • **Suscriptores:** Registro, inicio de sesión, navegación del catálogo, streaming con reanudación, lista de favoritos, calificaciones y gestión de suscripción.<br>• **Administradores / Evaluadores:** Inspección de salud del sistema (`/api/health`) y prueba interactiva de endpoints con Swagger UI (`/apidocs/`). |
| **Repositorio principal \*** | `https://github.com/Miguel-Angel-Salazar/OTT-` (rama `main`) |
| **Lenguajes y Tecnologías \*** | • **Backend:** Python 3.11, Flask 3.1.1, Jinja2 3.1.6, Flasgger 0.9.7.1, psycopg2-binary 2.9.10, bcrypt 4.3.0.<br>• **Frontend:** Nginx 1.25 Alpine, HTML5, CSS3 nativo (tokens de diseño en variables CSS), JavaScript ES6+ vanilla.<br>• **Base de Datos:** PostgreSQL 16 Alpine con inicialización automática (`database/init.sql`).<br>• **Infraestructura:** Docker Engine 24+, Docker Compose v2+.<br>• **Pruebas:** Python Unittest y Playwright 1.50+ (Chromium headless). |
| **Imágenes en Docker Hub** | • Backend: `juanexzz/ott-backend:latest`<br>• Frontend: `juanexzz/ott-frontend:latest`<br>• Base de datos: `postgres:16-alpine` |
| **Datos de prueba disponibles** | Sí: Base de datos relacional precargada con 20 películas/series completas (con posters y videos MP4 locales), usuarios de prueba (`admin@ott.com` y `demo@ott.com`) con contraseñas cifradas en bcrypt, historial de visualización y favoritos. |
| **Criterio de éxito del hito \*** | Garantizar la comunicación entre frontend, backend y base de datos, levantar la solución con `docker compose up`, exponer documentación Swagger/OpenAPI y validar el funcionamiento con pruebas unitarias y de Playwright. |

---

### 2. Integrantes y Responsabilidades

| # | Nombre Completo | Correo Institucional / Git | Rol Principal | Responsabilidades Asignadas |
| :-: | :--- | :--- | :--- | :--- |
| **1** | Miguel Ángel Salazar | `miguelangelguarnizosalazar@gmail.com` | Líder de Desarrollo / Backend | Arquitectura MVC, modelos de dominio, catálogo dinámico, filtrado regional y gestión de favoritos (HU-01, HU-02). |
| **2** | Juan Esteban Vallejo | `juanvallejo240@gmail.com` | DevOps / Infraestructura | Contenerización multi-servicio (Docker, Docker Compose), publicación en Docker Hub y esquema relacional PostgreSQL con `init.sql` (HU-03, HU-04). |
| **3** | Juan Esteban Echavarría Corrales | `juanestebanechavarria511@gmail.com` | Backend / Seguridad | Módulo de autenticación segura (bcrypt), manejo de sesiones HTTP, perfil de usuario y cambio de suscripción (HU-05, HU-06). |
| **4** | Sebastián Villa | `sebasviro567@gmail.com` | Fullstack / QA | Reproductor multimedia con persistencia de minuto, motor de búsqueda, calificaciones (Like/Dislike) y automatización de pruebas Playwright (HU-07, HU-08). |

---

### 3. Arquitectura y Componentes Mínimos

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

| Capa / Servicio | Tecnología | Contenedor / Imagen | Puerto | Función Principal |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend** | Nginx 1.25 Alpine | `ott-frontend` (`juanexzz/ott-frontend:latest`) | `80:80` | Proxy inverso hacia backend; entrega de archivos estáticos (CSS, JS, videos, posters) con compresión y caché. |
| **Backend / API** | Python 3.11 + Flask | `ott-backend` (`juanexzz/ott-backend:latest`) | `5000:5000` | Controlador central, renderizado SSR con Jinja2, especificación Swagger en `/apidocs/` y healthcheck en `/api/health`. |
| **Base de Datos** | PostgreSQL 16 Alpine | `ott-db` (`postgres:16-alpine`) | `5432:5432` | Persistencia relacional de usuarios, perfiles, películas, favoritos, historial y calificaciones, con volumen `postgres_data`. |

---

### 4. Funcionalidades y Deuda Técnica Resuelta

#### Funcionalidades Críticas Operativas
1. **Autenticación y Registro:** Cifrado con `bcrypt`, control de sesiones firmadas (`SECRET_KEY`), login/logout y control de acceso.
2. **Catálogo y Filtrado:** Catálogo de 20 producciones con filtrado por región del usuario (`LATAM`, `EUROPA`, `USA`, `GLOBAL`) y carrusel de Cine Colombiano.
3. **Reproductor y Reanudación:** Streaming de video MP4 con persistencia del progreso por usuario y película en `watch_history`.
4. **Favoritos y Calificaciones:** Guardado de "Mi Lista" y sistema acumulativo de Likes y Dislikes.
5. **Motor de Búsqueda:** Búsqueda en tiempo real por título, género, sinopsis y país.
6. **Documentación Swagger:** Interfaz OpenAPI interactiva para pruebas de endpoints.
7. **Flujo de Salud del Sistema:** Endpoint `/api/health` para validar conectividad integral cliente-servidor-base de datos.

#### Deuda Técnica Resuelta respecto a la Entrega 1
* **Migración de base de datos:** Se eliminó la dependencia de Supabase en la nube; el proyecto ahora corre 100% autónomo sobre PostgreSQL local en Docker.
* **Cine Colombiano poblado:** Se incorporaron 5 títulos colombianos reales con video y arte promocional (*Monos*, *El olvido que seremos*, *La vendedora de rosas*, *Pájaros de verano*, *El páramo*).
* **Desacople Frontend/Backend:** El frontend ahora cuenta con su propio Dockerfile con servidor Nginx optimizado, en lugar de servirse únicamente por Flask.
* **Pruebas Automatizadas:** Se construyó una suite de 20 pruebas automatizadas sin intervención manual.

---

### 5. Plan de Trabajo del Semestre — Estado de Entregables

| ID | Entregable / Funcionalidad | Responsable | Prioridad | Estado | % Avance | Observaciones de la Segunda Entrega |
| :-: | :--- | :--- | :-: | :-: | :-: | :--- |
| **F-01** | Control de versiones y flujo en Git | Miguel Salazar | Alta | **Completado** | 100% | Monorepo consolidado con historial ordenado en `main`. |
| **F-02** | Dockerfile del Backend Flask | Miguel Salazar / J. Vallejo | Alta | **Completado** | 100% | Imagen optimizada multi-capa con Python 3.11-slim. |
| **F-03** | Docker Compose para entorno local | Juan Esteban Vallejo | Alta | **Completado** | 100% | Orquestación completa de `frontend`, `backend` y `db` con redes y volúmenes. |
| **F-04** | Integridad y esquema relacional en BD | Juan Esteban Vallejo | Alta | **Completado** | 100% | Script `init.sql` con llaves foráneas, cascade y 20 títulos sembrados. |
| **F-05** | Validación y manejo seguro de datos | Juan Sebastián Villa | Alta | **Completado** | 100% | Manejo seguro de payload JSON en progreso y normalización de rutas. |
| **F-06** | Control de sesiones y autenticación | J. Echavarría Corrales | Media | **Completado** | 100% | Hashing criptográfico con `bcrypt` y sesiones de Flask firmadas. |
| **F-07** | Consultas SQL directas y eficientes | Miguel Salazar | Media | **Completado** | 100% | Conexión directa vía `psycopg2` sin dependencias de PostgREST. |
| **F-08** | Modelo de dominio `Movie` consistente | Juan Sebastián Villa | Media | **Completado** | 100% | Clase `Movie` con método `from_dict` y normalización de rutas estáticas. |
| **F-09** | Historial de reproducción persistente | Miguel Salazar | Media | **Completado** | 100% | Persistencia en `watch_history` y respaldo local de contingencia en JSON. |
| **F-10** | Vista de perfil y planes de suscripción | J. Echavarría Corrales | Media | **Completado** | 100% | Gestión de cuenta, cambio de contraseña y alternancia de plan en `/profile`. |
| **F-11** | Encuesta de onboarding | Juan Esteban Vallejo | Baja | **Completado** | 100% | Vista `/home/onboarding` disponible tras registro. |
| **F-12** | Poblar categoría "Cine Colombiano" | J. Echavarría / Tomás S. | Baja | **Completado** | 100% | 5 películas colombianas completamente integradas al catálogo. |
| **F-13** | Suite de pruebas automatizadas | J. Vallejo / S. Villa | Alta | **Completado** | 100% | 10 pruebas unitarias, 4 de flujo de integración y 6 E2E con Playwright. |
| **F-14** | Pipeline CI: lint, pruebas y build | Miguel Salazar | Alta | En diseño | 30% | Pruebas listas para integrarse en GitHub Actions en el siguiente hito. |
| **F-15** | Pipeline CD: publicación a Docker Hub | Miguel Salazar / J. Vallejo | Alta | En diseño | 30% | Imágenes publicadas manualmente; automatización programada. |
| **F-16** | Manifiestos y despliegue en Kubernetes / EKS | Juan Sebastián Villa | Alta | No iniciado | 0% | Programado para la entrega final del semestre. |
| **F-17** | Observabilidad, logging y healthcheck | Miguel Salazar | Media | En desarrollo | 50% | Endpoint `/api/health` implementado y logs de contenedores accesibles. |
| **F-18** | Actualización de Ficha Técnica | Juan Esteban Vallejo | Media | **Completado** | 100% | Documento alineado con la arquitectura contenerizada real. |

---

### 6. Evidencias de Verificación y Pruebas

Para corroborar la validez de los datos de esta ficha técnica, se ejecutaron las suites de pruebas automatizadas en el repositorio:
* **Pruebas Unitarias:** `python -m unittest discover tests -p "test_unit.py"` ➔ **10/10 OK** (0.7s).
* **Pruebas de Flujo Completo:** `python -m unittest tests/test_flow.py` ➔ **4/4 OK** (0.8s).
* **Pruebas E2E con Playwright:** `python -m unittest tests/test_e2e_playwright.py` ➔ **6/6 OK** (11.8s).
* **Total:** **20 pruebas automáticas superadas con éxito.**
