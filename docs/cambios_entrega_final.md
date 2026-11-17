# Revisión y cambios para la Entrega Final · Proyecto DevOps

Documento de apoyo para la sustentación de **Gestión de la Configuración** (Universidad de Medellín).
Explica qué se revisó contra el libro de calificación *ENTREGA FINAL · PROYECTO DEVOPS*, qué se corrigió, qué queda pendiente y cómo presentar.

- **Repositorio:** https://github.com/Miguel-Angel-Salazar/OTT-
- **Fecha de la revisión:** 17 de noviembre de 2026
- **Responsable de los cambios:** Tomás Sepúlveda Giraldo (`Sepu2412`)

---

## 1. Qué pide el profesor

| Bloque | Peso | Qué se debe demostrar |
| :-- | :-: | :-- |
| Parte I · Elevator pitch | 20 % | Problema, propuesta de valor, justificación y comunicación |
| Parte II · Demo técnica | 80 % | CI + pruebas, Docker Hub, Minikube, flujo E2E, trazabilidad y operación |

Reglas que más afectan la nota:

- Se evalúa **evidencia ejecutable y trazable**, no solo diapositivas o capturas.
- Jenkins y GitOps **no son obligatorios** si no estaban en el alcance aprobado; hay que explicar los límites con honestidad.
- **No mostrar contraseñas ni tokens.** No se aceptan flujos simulados presentados como reales.
- Probar antes de la defensa y tener respaldo de evidencia por si falla algo externo (internet, Docker Hub).

---

## 2. Resultado de la revisión, criterio por criterio

| Criterio | Qué evidencia tiene el repo | Estado |
| :-- | :-- | :-: |
| P1–P4 · Pitch | Guion en `docs/guia_sustentacion_final.md` (Parte I) y presentación en diapositivas | Cumple |
| D1 · Arquitectura y Git | Estructura `backend/`, `frontend/`, `database/`, `tests/`, `k8s/`, historial de commits | Cumple |
| D2 · CI, pruebas y control de fallos | `.github/workflows/ci-cd.yml` con 2 jobs (`needs` + `if: success()`), 10 pruebas unitarias y 4 de integración | **Fallaba** (corregido, ver sección 3) |
| D3 · Dockerfiles y Docker Hub | Capas ordenadas, usuario `appuser`, `HEALTHCHECK`, etiquetas OCI; imágenes `juanexzz/ott-backend` y `juanexzz/ott-frontend` | Cumple. Falta configurar secretos para que CI publique solo |
| D4 · Minikube | 5 manifiestos en `k8s/`: Namespace, ConfigMap/Secret, PostgreSQL StatefulSet + PVC, Deployments y Services con probes | Cumple |
| D5 · Flujo E2E y caso de error | Login → favorito/progreso → consulta en `ott-db-0`; `/api/movies/999` devuelve 404 y login inválido muestra alerta | Cumple |
| D6 · Trazabilidad | Tags `v1.0.0` y `sha-<commit>`, comando `kubectl get pods ... imageID` | Cumple; reforzado con validación y resumen en CI |
| D7 · Seguridad | `.env` ignorado, `.env.example`, Secret de Kubernetes, contenedor sin root | Cumple con una advertencia (ver sección 5) |
| D8 · Observabilidad y operación | `kubectl logs`, `describe`, borrado de pod y autorrecuperación | Cumple |
| D9 · Roles | Reparto de integrantes en la guía de sustentación | Cumple |

---

## 3. Problema encontrado: el pipeline de CI fallaba

La única ejecución de GitHub Actions (commit `af2de33`, 12 de noviembre) terminó en **Failure**.

**Causa probable:** el paso *Publicar en Docker Hub* tenía esta condición:

```yaml
if: ${{ secrets.DOCKERHUB_USERNAME != '' && secrets.DOCKERHUB_TOKEN != '' }}
```

GitHub Actions **no permite usar `secrets` dentro de un `if:` de un paso**. Eso invalida el archivo del workflow y la ejecución falla antes de correr las pruebas. Mostrar un pipeline en rojo en la defensa afecta directamente D2 (12 %).

> Nota: no fue posible abrir los logs de esa ejecución para confirmarlo al 100 %. Si después del cambio el Job 1 sigue en rojo, el problema ya estaría en una prueba y hay que leer ese log.

---

## 4. Cambios realizados

### 4.1 `.github/workflows/ci-cd.yml`

1. **Secretos como variables de entorno del job.** El Job 2 ahora declara:
   ```yaml
   env:
     DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
     DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
   ```
   y el paso de publicación usa `if: ${{ env.DOCKERHUB_USERNAME != '' && env.DOCKERHUB_TOKEN != '' }}`. El `docker login` lee `$DOCKERHUB_TOKEN` desde el entorno, así el token nunca aparece escrito en el log.
2. **Validación de manifiestos de Kubernetes.** El Job 2 lee todos los YAML de `k8s/`, imprime cada recurso (`Kind/nombre`) y falla si alguno está mal formado.
3. **Coherencia entre CI y despliegue.** Se verifica que `k8s/04-backend.yaml` y `k8s/05-frontend.yaml` usen exactamente la imagen `v1.0.0` que el pipeline construyó. Si alguien cambia la versión en un lado y no en el otro, el pipeline falla.
4. **Resumen de trazabilidad.** Al final del Job 2 se escribe en el *Summary* de GitHub Actions una tabla con commit, rama, imágenes (`v1.0.0` y `sha-<commit>`), manifiestos y si se publicó en Docker Hub. Es la evidencia directa para D6.

### 4.2 `docs/guia_sustentacion_final.md`

- Bloque 2: se añadió la explicación de la validación de manifiestos.
- Bloque 5: se añadió el paso de mostrar el *Summary* del run como evidencia de trazabilidad.

### 4.3 `README.md`

- El encabezado decía solo "Paradigmas de Programación". Ahora menciona también **Gestión de la Configuración (Entrega Final DevOps)**.

### 4.4 Presentación

Se preparó una presentación de 15 diapositivas, con notas del orador y los comandos exactos:

| # | Diapositiva | Criterio |
| :-: | :-- | :-- |
| 1 | Portada y equipo | — |
| 2 | El problema | P1 |
| 3 | Propuesta de valor y alcance | P2 |
| 4 | Arquitectura (Nginx → Flask → PostgreSQL en Minikube) | D1 |
| 5 | Por qué cada práctica DevOps | P3 |
| 6 | Quién defiende qué | P4, D9 |
| 7 | Inicio de la demo: de un commit a un pod | — |
| 8 | CI, pruebas y control de fallos | D1, D2 |
| 9 | Imágenes y Docker Hub | D3, D7 |
| 10 | Despliegue en Minikube | D4 |
| 11 | Flujo E2E y caso de error | D5 |
| 12 | Trazabilidad commit → pod | D6 |
| 13 | Operación y seguridad | D7, D8 |
| 14 | Límites honestos | Integridad |
| 15 | Preguntas | — |

---

## 5. Pendientes antes del examen

1. **Configurar los secretos de Docker Hub** (lo hace quien administre el repo):
   *Settings → Secrets and variables → Actions → New repository secret*
   - `DOCKERHUB_USERNAME` = `juanexzz`
   - `DOCKERHUB_TOKEN` = un *Access Token* de Docker Hub (no la contraseña)

   Sin ellos el pipeline pasa igual, pero no publica las imágenes; el Summary lo indica.
2. **Confirmar el pipeline en verde.** Hacer push o ejecutar *Run workflow* en Actions y verificar que los 2 jobs terminen bien.
3. **Ensayar la demo completa en Minikube** siguiendo `docs/guia_sustentacion_final.md` y tomar capturas de respaldo.
4. **No abrir en pantalla `k8s/02-configmap-and-secret.yaml`.** Tiene credenciales de desarrollo en texto plano (`ott_password`, `SECRET_KEY`). Si el profesor pregunta, explicarlo como límite (diapositiva 14) y proponer Sealed Secrets o crear el Secret desde un `.env` fuera de Git.

---

## 6. Límites que se deben reconocer en la defensa

| Límite actual | Siguiente paso propuesto |
| :-- | :-- |
| No hay Jenkins ni operador GitOps (Argo CD); el despliegue es `kubectl apply -f k8s/` | Argo CD vigilando la carpeta `k8s/` |
| El Secret de `k8s/` tiene valores de desarrollo versionados | Sealed Secrets o Secret creado desde un `.env` externo |
| Los manifiestos usan `v1.0.0` fijo, no el SHA de cada commit | Que CI actualice el tag del manifiesto por commit |
| Las 6 pruebas E2E con Playwright solo se corren en local | Ejecutarlas en CI contra un clúster `kind` |
| Streaming MP4 progresivo, sin HLS adaptativo | Transcodificación HLS si el proyecto crece |

---

## 7. Comandos clave para la demo

```powershell
# D1 · Repositorio
git log --oneline -n 8

# D2 · Pruebas
python -m unittest discover tests -p "test_unit.py" -v

# D4 · Minikube
minikube status
kubectl apply -f k8s/
kubectl get pods,svc,deploy,statefulset,pvc -n ott-platform

# D5 · E2E
kubectl port-forward svc/ott-frontend -n ott-platform 8090:80
curl.exe -i http://localhost:8090/api/movies/999

# D6 · Trazabilidad
git rev-parse --short HEAD
kubectl get pods -n ott-platform -o custom-columns="POD:.metadata.name,IMAGE:.spec.containers[*].image,IMAGE_ID:.status.containerStatuses[*].imageID"

# D8 · Operación
kubectl logs -n ott-platform deployment/ott-backend --tail=20
kubectl delete pod -n ott-platform -l app=ott-backend
kubectl get pods -n ott-platform -w
```
