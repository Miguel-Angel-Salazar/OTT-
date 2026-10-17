# Historias de Usuario - Plataforma OTT (Clon MUBI)
## Materia: Paradigmas de Programación — Entrega 2 y Final

Este documento detalla las Historias de Usuario (HU) desarrolladas para la plataforma, especificando el rol, la necesidad, el criterio de aceptación y el estudiante responsable de cada funcionalidad.

---

### Resumen de Asignación por Integrante

| ID | Historia de Usuario | Responsable | Estado |
| :--- | :--- | :--- | :--- |
| **HU-01** | Catálogo principal y filtrado por región | Miguel Ángel Salazar | Entregada |
| **HU-02** | Gestión de favoritos ("Mi Lista") | Miguel Ángel Salazar | Entregada |
| **HU-03** | Contenerización y orquestación con Docker Compose | Juan Esteban Vallejo | Entregada |
| **HU-04** | Base de datos relacional y scripts de inicialización (`init.sql`) | Juan Esteban Vallejo | Entregada |
| **HU-05** | Autenticación y registro con contraseñas seguras (bcrypt) | Tomás Sepúlveda | Entregada |
| **HU-06** | Perfil de usuario y actualización de suscripción | Tomás Sepúlveda | Entregada |
| **HU-07** | Reproductor de video con guardado de progreso | Sebastián Villa | Entregada |
| **HU-08** | Calificaciones (Like/Dislike) y búsqueda en tiempo real | Sebastián Villa | Entregada |

---

### Detalle de Historias de Usuario

#### HU-01: Catálogo principal y filtrado por región
* **Responsable:** Miguel Ángel Salazar
* **Descripción:** Como usuario autenticado, quiero ver una cartelera principal con una película destacada (hero) y carruseles organizados por categorías, filtrados de acuerdo con mi región geográfica o contenido global.
* **Criterios de Aceptación:**
  1. Si el usuario tiene una región asignada (ej. `LATAM`), el catálogo prioriza o filtra los títulos pertenecientes a esa región y los marcados como `GLOBAL`.
  2. Si no hay sesión iniciada, se muestra el catálogo general disponible.
  3. La primera película del listado debe presentarse como película destacada en el banner principal con su título, sinopsis y opción de reproducción.

#### HU-02: Gestión de favoritos ("Mi Lista")
* **Responsable:** Miguel Ángel Salazar
* **Descripción:** Como suscriptor de la plataforma, quiero agregar o remover películas a mi lista personal para encontrarlas fácilmente en la pantalla de inicio.
* **Criterios de Aceptación:**
  1. El botón de favoritos debe permitir alternar (toggle) el estado: si ya está agregada, la quita; si no, la inserta en la tabla `favorites`.
  2. El carrusel "Mi Lista" en el home solo debe mostrar los títulos marcados por el usuario en sesión.
  3. Los usuarios no autenticados son redirigidos a iniciar sesión al intentar interactuar con el botón de favoritos.

#### HU-03: Contenerización y orquestación con Docker Compose
* **Responsable:** Juan Esteban Vallejo
* **Descripción:** Como desarrollador y evaluador del proyecto, quiero levantar toda la plataforma (frontend, backend y base de datos) con un único comando para garantizar portabilidad y paridad entre entornos.
* **Criterios de Aceptación:**
  1. El archivo `docker-compose.yml` debe definir los servicios `db` (PostgreSQL 16), `backend` (Flask en Python 3.11) y `frontend` (Nginx Alpine).
  2. El frontend debe actuar como proxy inverso redirigiendo peticiones dinámicas al backend y sirviendo activos estáticos con caché.
  3. Las imágenes deben estar publicadas en Docker Hub para permitir despliegues directos sin compilación local obligatoria.

#### HU-04: Base de datos relacional y scripts de inicialización (`init.sql`)
* **Responsable:** Juan Esteban Vallejo
* **Descripción:** Como administrador de la plataforma, quiero que la base de datos se configure de manera automática con su esquema relacional y datos de prueba al primer arranque.
* **Criterios de Aceptación:**
  1. El script `database/init.sql` crea las tablas maestras: `users`, `profiles`, `movies`, `favorites`, `watch_history` y `ratings` con sus llaves foráneas y restricciones `ON DELETE CASCADE`.
  2. Se deben precargar al menos 20 títulos clasificados por región, género y tipo (Película/Serie).
  3. Se deben precargar cuentas de prueba (`admin@ott.com`, `demo@ott.com`) con hashes válidos y datos de ejemplo en favoritos e historial.

#### HU-05: Autenticación y registro con contraseñas seguras (bcrypt)
* **Responsable:** Tomás Sepúlveda
* **Descripción:** Como visitante, quiero registrarme e iniciar sesión de manera segura para acceder a las funciones exclusivas para miembros.
* **Criterios de Aceptación:**
  1. Las contraseñas deben cifrarse usando `bcrypt` antes de almacenarse en la base de datos.
  2. Las credenciales incorrectas deben presentar un mensaje amigable en pantalla sin exponer detalles internos.
  3. Al iniciar sesión correctamente se genera una cookie de sesión firmada con `SECRET_KEY` que almacena id, correo, nombre y plan del usuario.

#### HU-06: Perfil de usuario y actualización de suscripción
* **Responsable:** Tomás Sepúlveda
* **Descripción:** Como usuario registrado, quiero consultar los datos de mi cuenta y cambiar mi plan de suscripción (Básica o Premium) para acceder a distintos beneficios.
* **Criterios de Aceptación:**
  1. La ruta `/profile/` permite ver el correo, nombre y plan actual almacenados en la tabla `profiles`.
  2. El usuario puede cambiar su suscripción entre planes permitidos y el cambio debe persistirse en la BD y actualizarse en la sesión activa.
  3. Incluye opción para cambio de contraseña validando primero la contraseña actual del usuario.

#### HU-07: Reproductor de video interactivo con guardado de progreso
* **Responsable:** Sebastián Villa
* **Descripción:** Como espectador, quiero que el reproductor recuerde el minuto en el que dejé una película o serie para poder reanudarla después sin buscar manualmente.
* **Criterios de Aceptación:**
  1. La vista `/movie/<id>` integra un reproductor HTML5 con controles personalizados (play/pause, barra de progreso, volumen, pantalla completa).
  2. Mediante peticiones asíncronas periódicas a `/movie/<id>/progreso`, el cliente envía el segundo actual de reproducción y se persiste en `watch_history`.
  3. Si la base de datos no está disponible, el backend cuenta con respaldo local en archivo JSON para no perder el avance del usuario.

#### HU-08: Calificaciones (Like/Dislike) y búsqueda en tiempo real
* **Responsable:** Sebastián Villa
* **Descripción:** Como usuario, quiero calificar los contenidos que veo y disponer de un buscador ágil para encontrar títulos por nombre, género o país.
* **Criterios de Aceptación:**
  1. Los endpoints `/movie/<id>/like` y `/movie/<id>/dislike` registran o actualizan la calificación del usuario en una sola operación (`ON CONFLICT DO UPDATE`).
  2. La vista de detalle muestra el conteo total acumulado de likes y dislikes.
  3. La ruta `/movie/search` permite filtrar películas comparando la consulta contra título, categoría, descripción y región de forma insensible a mayúsculas.
