# 🎯 Guía de Sustentación Final — Proyecto DevOps: CINÉFILO (OTT)

Este documento está estructurado exactamente según el libro de calificación **`ENTREGA FINAL · PROYECTO DEVOPS`** (Parte I: Elevator Pitch 20% + Parte II: Demostración Técnica 80% + Checklist de Evidencias).

---

## 🎙️ PARTE I: Elevator Pitch (4 a 5 minutos — 20% de la nota)

### 1. Problema y Motivación (`P1` — 5% · ~1 min)
* **¿Qué problema real resolvemos?** Las plataformas comerciales de streaming concentran su catálogo en producciones masivas y relegan el cine independiente y el **Cine Colombiano y Latinoamericano**. Además, a nivel técnico, la versión inicial del proyecto dependía de servicios externos cerrados en la nube (Supabase) y se ejecutaba de forma monolítica manual, lo que generaba fallos de entorno (*"en mi máquina sí funciona"*), latencia externa y falta de reproducibilidad.
* **¿Quiénes son los destinatarios?**
  1. **Usuarios / Cinéfilos:** Estudiantes y espectadores que buscan un catálogo curado por región (`LATAM`, `EUROPA`, `USA`), con énfasis en cine colombiano (*Monos*, *El olvido que seremos*, *La vendedora de rosas*, *Pájaros de verano*, *El páramo*), reproducción con guardado automático del segundo exacto, lista de favoritos y calificaciones.
  2. **Equipo de Ingeniería / Operación:** Desarrolladores que requieren levantar toda la plataforma con un solo comando declarativo sin depender de cuentas externas.

### 2. Propuesta de Valor y Alcance (`P2` — 5% · ~1 min)
* **Solución:** **CINÉFILO**, una plataforma OTT inspirada en MUBI, 100% autónoma y contenerizada en 3 capas:
  * **Frontend / Reverse Proxy (`Nginx 1.25-alpine`):** Entrega de pósters y 20 videos MP4 locales con caché de 30 días y enrutamiento inverso hacia el backend.
  * **Backend / API (`Python 3.11 + Flask 3.1.1 + Flasgger`):** Arquitectura MVC en Blueprints, contraseñas cifradas con `bcrypt`, sesiones firmadas, healthcheck en `/api/health` y documentación interactiva OpenAPI en `/apidocs/`.
  * **Base de Datos Propia (`PostgreSQL 16-alpine`):** Esquema relacional de 6 tablas (`users`, `profiles`, `movies`, `favorites`, `watch_history`, `ratings`) autoinicializado con `init.sql`.
* **Límites honestos del alcance:** El streaming sirve archivos MP4 progresivos desde Nginx (no transcodificación adaptativa HLS en vivo), y la entrega en Kubernetes utiliza manifiestos declarativos versionados en Git (`k8s/`) aplicados sobre Minikube.

### 3. Justificación Técnica y Prácticas DevOps (`P3` — 5% · ~1.5 min)
* **¿Por qué esta arquitectura y cadena DevOps aportan valor real al producto?**
  * **Desacople Nginx + Flask:** Antes Flask servía los videos MP4 bloqueando hilos de Python. Al separar Nginx en su propio contenedor/pod, los activos multimedia se sirven con caché nativa y Flask solo procesa lógica de negocio y API.
  * **Integración Continua (GitHub Actions + 20 Pruebas):** Cada `push` o `PR` levanta un contenedor efímero de PostgreSQL 16, inyecta `init.sql` y corre las pruebas unitarias (`test_unit.py`) y de flujo (`test_flow.py`). Si alguien rompe el login o una consulta SQL, el Job 1 falla y **bloquea automáticamente** la construcción de imágenes (Job 2).
  * **Kubernetes (Minikube) con Probes y Persistencia:** En Kubernetes, PostgreSQL corre como `StatefulSet` con un `PersistentVolumeClaim` (`postgres-pvc`), garantizando que si el pod de base de datos se reinicia, los usuarios registrados y el minuto de reproducción **no se pierden**. Además, `readinessProbe` y `livenessProbe` sobre `/api/health` aseguran autorrecuperación (*self-healing*).

### 4. Distribución de Roles para la Defensa (`P4` y `D9` — 5% + 4%)
* **Integrante 1 (Miguel Ángel Salazar):** Pitch + Arquitectura y Git (`D1`) + CI en GitHub Actions (`D2`).
* **Integrante 2 (Juan Esteban Vallejo):** Dockerfiles, Seguridad y Docker Hub (`D3`, `D7`) + Trazabilidad (`D6`).
* **Integrante 3 (Sebastián Villa):** Despliegue en Minikube (`D4`) + Observabilidad y Diagnóstico de Fallos (`D8`).
* **Integrante 4 (Tomás Sepúlveda):** Flujo Funcional E2E en vivo: UI → API → PostgreSQL y caso de error (`D5`).

---

## 💻 PARTE II: Demostración Técnica Paso a Paso (15 a 20 minutos — 80% de la nota)

> **Preparación antes de pasar al frente:** Tener abierto el navegador en el repositorio GitHub (`Actions` y código), Docker Hub (`juanexzz/ott-backend` y `juanexzz/ott-frontend`), y una terminal PowerShell ubicada en `C:\Users\User\ott_confi\OTT-`.

---

### Bloque 1: Arquitectura y Repositorio Git (`D1` — 8%)
1. Mostrar la estructura limpia del proyecto y el historial de commits:
   ```powershell
   git status
   git log --oneline -n 8
   ```
2. Mostrar las carpetas clave: `backend/`, `frontend/`, `database/init.sql`, `tests/`, `.github/workflows/ci-cd.yml` y `k8s/`.

---

### Bloque 2: CI Automatizada, Pruebas y Control de Fallos (`D2` — 12%)
1. **Abrir en GitHub la pestaña Actions** (`.github/workflows/ci-cd.yml`) y señalar los 2 Jobs encadenados con `needs: unit-and-integration-tests`:
   * **Job 1 (`unit-and-integration-tests`):** Levanta un servicio `postgres:16-alpine`, ejecuta `database/init.sql` y corre las pruebas.
   * **Job 2 (`docker-build-and-traceability`):** Solo se ejecuta si `if: success()` del Job 1 se cumple (demostrando la política de control de fallos que previene promocionar código roto).
2. **Ejecutar las pruebas en vivo en la terminal** para mostrar el test runner y qué cubren:
   ```powershell
   .\.venv\Scripts\python.exe -m unittest discover tests -p "test_unit.py" -v
   ```
   *Explicar:* `test_unit.py` prueba instanciación del modelo `Movie`, normalización de rutas, hashing `bcrypt`, filtrado por región (`LATAM`/`GLOBAL`) y endpoints HTTP; `test_flow.py` verifica `/api/health`, películas semilla, login con `demo@ott.com` y navegación autenticada.

---

### Bloque 3: Dockerfiles, Buenas Prácticas y Docker Hub (`D3` y `D7` — 8% + 5%)
1. Mostrar [`backend/Dockerfile`](../backend/Dockerfile) y [`frontend/Dockerfile`](../frontend/Dockerfile) destacando las 4 buenas prácticas que pide la rúbrica:
   * **Orden de capas:** Primero `COPY requirements.txt .` y `pip install` antes de `COPY . .` para aprovechar la caché de Docker.
   * **Usuario no privilegiado (Seguridad `D3`/`D7`):** Creación y uso de `USER appuser` en el backend para no ejecutar el contenedor como `root`.
   * **Secretos fuera de la imagen (`D7`):** Ningún Dockerfile contiene contraseñas ni archivos `.env` (excluidos en `.dockerignore` y `.gitignore`).
   * **Healthcheck y etiquetas OCI (`LABEL`):** Versión `1.0.0` y chequeo nativo contra `/api/health`.
2. Mostrar las imágenes locales y en Docker Hub (`juanexzz/ott-backend` y `juanexzz/ott-frontend`):
   ```powershell
   docker images | Select-String "ott"
   ```

---

### Bloque 4: Despliegue en Minikube / Kubernetes (`D4` — 14%)
1. **Comprobar que Minikube está activo y el contexto apunta a `minikube`:**
   ```powershell
   minikube status
   kubectl config current-context
   ```
2. **Mostrar los 5 manifiestos versionados en `k8s/` y aplicarlos:**
   ```powershell
   Get-ChildItem k8s/
   kubectl apply -f k8s/
   ```
   *Explicar rápidamente cada archivo:*
   * `01-namespace.yaml`: Namespace `ott-platform`.
   * `02-configmap-and-secret.yaml`: `ConfigMap` (`BACKEND_URL`, `POSTGRES_DB`, `init.sql`) y `Secret` (`DATABASE_URL`, `POSTGRES_PASSWORD`, `SECRET_KEY`).
   * `03-postgres.yaml`: `PersistentVolumeClaim` (`postgres-pvc` 1Gi) + `StatefulSet` `ott-db` + `Service` `ClusterIP:5432`.
   * `04-backend.yaml`: `Deployment` `ott-backend` con `readinessProbe` y `livenessProbe` en `/api/health` y límites de CPU/Memoria + `Service` `ClusterIP:5000`.
   * `05-frontend.yaml`: `Deployment` `ott-frontend` + `Service` `NodePort` (`80:30080`).
3. **Verificar que todos los Pods, Services y PVC están saludables (`Running` / `Bound`):**
   ```powershell
   kubectl get pods,svc,deploy,statefulset,pvc -n ott-platform -o wide
   ```

---

### Bloque 5: Trazabilidad de Entrega (`D6` — 10%)
Demostrar cómo se conecta el **Commit de Git → Imagen/Tag → Manifiesto K8s → Pod en ejecución**:
```powershell
# 1. Ver el commit actual en Git
git rev-parse --short HEAD

# 2. Ver exactamente qué imagen e ImageID están corriendo en cada Pod de Minikube
kubectl get pods -n ott-platform -o custom-columns="POD:.metadata.name,STATUS:.status.phase,IMAGE:.spec.containers[*].image,IMAGE_ID:.status.containerStatuses[*].imageID"
```
*Explicar la diferencia entre CI y CD/GitOps:*
* **CI (GitHub Actions):** Valida el código con pruebas automatizadas y empaqueta el artefacto inmutable (imagen Docker etiquetada con versión y SHA).
* **Estado Declarativo / GitOps (`k8s/`):** La carpeta `k8s/` en Git es la **única fuente de verdad** del estado deseado del clúster; `kubectl apply -f k8s/` reconcilia el estado real de Minikube con lo declarado en Git.

---

### Bloque 6: Flujo Funcional E2E Real en Minikube y Caso de Error (`D5` — 14%)
1. **Abrir el túnel hacia el Service del Frontend en Minikube (si no está abierto en otra terminal):**
   ```powershell
   # Ejecutar en segundo plano o en una segunda pestaña de PowerShell:
   kubectl port-forward svc/ott-frontend -n ott-platform 8090:80
   ```
2. **Probar API y Swagger UI desde Minikube:**
   * Abrir en el navegador:
     * **Healthcheck JSON:** `http://localhost:8090/api/health` → Muestra `{"database": "connected", "status": "ok"}`.
     * **Swagger UI:** `http://localhost:8090/apidocs/` → Probar en vivo `GET /api/movies`.
3. **Demostrar el Caso de Error Manejado (`D5`):**
   * **Error en API (404 controlado):** Abrir o ejecutar `curl.exe -i http://localhost:8090/api/movies/999` → Devuelve `HTTP/1.1 404 NOT FOUND` con `{"error": "Pelicula no encontrada"}`.
   * **Error en UI (Validación de credenciales):** En `http://localhost:8090/auth/login`, ingresar `demo@ott.com` con contraseña incorrecta `clave_mala` → La interfaz muestra alerta de error sin caerse.
4. **Demostrar Flujo Completo UI → API → BD y Persistencia (`D5`):**
   * Iniciar sesión con **`demo@ott.com`** / **`demo123`**.
   * Entrar a la película **"Monos"** (`/movie/1`), hacer clic en **"+ Mi Lista"** (Favoritos) o **"Me gusta" (Like)** y reproducir unos segundos del video.
   * **Comprobar en vivo dentro del Pod de PostgreSQL en Minikube** que el dato quedó persistido realmente en la base de datos:
     ```powershell
     kubectl exec -n ott-platform ott-db-0 -- psql -U ott_user -d ott_db -c "SELECT u.email, m.titulo, f.pelicula_id FROM favorites f JOIN users u ON u.id = f.usuario_id JOIN movies m ON m.id = f.pelicula_id;"
     kubectl exec -n ott-platform ott-db-0 -- psql -U ott_user -d ott_db -c "SELECT u.email, m.titulo, w.minuto FROM watch_history w JOIN users u ON u.id = w.usuario_id JOIN movies m ON m.id = w.pelicula_id;"
     ```

---

### Bloque 7: Observabilidad, Diagnóstico y Autorrecuperación en Vivo (`D8` — 5%)
1. **Inspeccionar logs y eventos de los pods:**
   ```powershell
   kubectl logs -n ott-platform deployment/ott-backend --tail=20
   kubectl describe deployment ott-backend -n ott-platform
   ```
2. **Simular un incidente en vivo (caída del Pod del Backend) y demostrar autorrecuperación de Kubernetes:**
   ```powershell
   # Eliminar el pod del backend intencionalmente
   kubectl delete pod -n ott-platform -l app=ott-backend

   # Observar cómo el ReplicaSet crea un nuevo pod inmediatamente y las probes verifican su salud
   kubectl get pods -n ott-platform -w
   ```
   *(Presionar `Ctrl+C` tras ver que el nuevo pod pasa a `1/1 Running` en pocos segundos y comprobar que los datos en PostgreSQL siguen intactos).*

---

## ✅ Checklist Oficial de Evidencias (Hoja «Checklist de evidencias» del Excel)

| Fase | Evidencia solicitada | Estado | Enlace / Comando Exacto / Observación | Criterios |
| :--- | :--- | :-: | :--- | :---: |
| **Antes de iniciar** | Repositorio(s) Git accesibles | **Sí** | `https://github.com/Miguel-Angel-Salazar/OTT-` · `git log --oneline -n 10` | D1 |
| **Antes de iniciar** | Arquitectura visible | **Sí** | Diagrama en `README.md`: `ott-frontend` (Nginx:80) ↔ `ott-backend` (Flask:5000) ↔ `ott-db` (Postgres:5432) | D1 |
| **CI** | Workflow GitHub Actions | **Sí** | `.github/workflows/ci-cd.yml` (ejecución automática en push/PR a `main`) | D2 |
| **CI** | Pruebas unitarias | **Sí** | `python -m unittest discover tests -p "test_unit.py" -v` (10 unitarias + 4 de flujo + 6 E2E = 20 pruebas) | D2 |
| **CI** | Control de fallos | **Sí** | En `.github/workflows/ci-cd.yml`: `needs: unit-and-integration-tests` + `if: success()` bloquea el build si falla un test | D2 |
| **Imagen** | Dockerfiles de web y API | **Sí** | `backend/Dockerfile` (Python 3.11-slim, `USER appuser`, `HEALTHCHECK`) y `frontend/Dockerfile` (Nginx 1.25-alpine) | D3 |
| **Imagen** | DockerHub | **Sí** | `juanexzz/ott-backend:v1.0.0` (`latest`) y `juanexzz/ott-frontend:v1.0.0` (`latest`) | D3 |
| **Despliegue** | Minikube activo | **Sí** | `minikube status` ; `kubectl config current-context` (`minikube`) | D4 |
| **Despliegue** | Manifiestos versionados | **Sí** | Carpeta `k8s/` (`01-namespace`, `02-configmap-and-secret`, `03-postgres`, `04-backend`, `05-frontend`) | D4, D6 |
| **Despliegue** | Recursos saludables | **Sí** | `kubectl get pods,svc,deploy,statefulset,pvc -n ott-platform` (`1/1 Running`, PVC `Bound`) | D4, D8 |
| **E2E** | Web accesible desde Minikube | **Sí** | `kubectl port-forward svc/ott-frontend -n ott-platform 8090:80` → `http://localhost:8090` | D5 |
| **E2E** | Operación UI → API → BD | **Sí** | Login con `demo@ott.com`, agregar favorito/progreso y verificar con `kubectl exec -n ott-platform ott-db-0 -- psql ...` | D5 |
| **E2E** | Caso de error real | **Sí** | `curl.exe -i http://localhost:8090/api/movies/999` (404 JSON) y login con clave inválida en `/auth/login` | D5, D8 |
| **Cadena de entrega** | Commit → workflow → tag | **Sí** | `git rev-parse --short HEAD` asociado al job de GitHub Actions y etiqueta `v1.0.0` / `sha-<commit>` | D2, D3, D6 |
| **Cadena de entrega** | Tag → manifiesto → pod | **Sí** | `kubectl describe pod -n ott-platform -l app=ott-backend` muestra imagen e ImageID exactos | D4, D6 |
| **GitOps (si aplica)** | Estado deseado y reconciliación | **Sí** | Estado declarativo en `k8s/` versionado en Git como fuente de verdad; reconciliado en Minikube con `kubectl apply -f k8s/` | D6 |
| **Operación** | Logs y diagnóstico | **Sí** | `kubectl logs -n ott-platform deploy/ott-backend` y prueba de resiliencia con `kubectl delete pod -n ott-platform -l app=ott-backend` | D8 |
| **Seguridad** | Secretos no expuestos | **Sí** | `.env` en `.gitignore`, plantilla `.env.example`, `Secret` `ott-secrets` en K8s y usuario `appuser` no-root | D7 |
| **Cierre** | Reproducibilidad | **Sí** | Documentado paso a paso en `README.md` tanto para Kubernetes (`Minikube`) como para `Docker Compose` | D1, D9 |
| **Pitch** | Problema, usuarios y valor | **Sí** | Guion estructurado en la Parte I de este documento (`P1`, `P2`, `P3`, `P4`) | P1–P4 |
