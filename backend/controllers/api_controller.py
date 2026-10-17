from flask import Blueprint, jsonify, request
from config.db_config import get_connection
from services.movie_service import listar_peliculas

# blueprint para endpoints API y verificacion de salud
api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/health", methods=["GET"])
def health():
    """Comprueba el estado del backend y la conexion con la base de datos PostgreSQL.
    ---
    tags:
      - Sistema
    summary: Verificacion de estado del servicio
    description: Ejecuta una consulta de prueba hacia la base de datos PostgreSQL para verificar conectividad.
    responses:
      200:
        description: Servicio operativo y conectado correctamente a la base de datos.
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
            database:
              type: string
              example: connected
            message:
              type: string
              example: Backend y base de datos comunicandose correctamente.
      500:
        description: Error de comunicacion con la base de datos.
        schema:
          type: object
          properties:
            status:
              type: string
              example: error
            database:
              type: string
              example: disconnected
            error:
              type: string
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 AS test;")
        cur.fetchone()
        cur.close()
        conn.close()

        return jsonify({
            "status": "ok",
            "database": "connected",
            "message": "Backend y base de datos comunicandose correctamente."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "database": "disconnected",
            "error": str(e)
        }), 500


@api_bp.route("/movies", methods=["GET"])
def get_movies():
    """Obtiene el catalogo completo de peliculas en formato JSON.
    ---
    tags:
      - Catalogo
    summary: Listado de peliculas
    description: Devuelve todas las peliculas disponibles con sus atributos principales.
    responses:
      200:
        description: Listado de peliculas obtenido exitosamente.
        schema:
          type: object
          properties:
            total:
              type: integer
              example: 20
            peliculas:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  titulo:
                    type: string
                  categoria:
                    type: string
                  region:
                    type: string
    """
    peliculas = listar_peliculas()
    data = [
        {
            "id": m.id,
            "titulo": m.titulo,
            "descripcion": m.descripcion,
            "categoria": m.categoria,
            "region": m.region,
            "imagen_url": m.imagen_url,
            "video_url": m.video_url,
            "tipo": m.tipo
        }
        for m in peliculas
    ]
    return jsonify({
        "total": len(data),
        "peliculas": data
    }), 200


@api_bp.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie_detail(movie_id):
    """Obtiene los detalles de una pelicula por su identificador.
    ---
    tags:
      - Catalogo
    summary: Detalle de pelicula
    parameters:
      - name: movie_id
        in: path
        type: integer
        required: true
        description: ID de la pelicula a consultar
    responses:
      200:
        description: Detalle de la pelicula encontrada.
      404:
        description: Pelicula no encontrada.
    """
    peliculas = listar_peliculas()
    pelicula = next((m for m in peliculas if m.id == movie_id), None)

    if not pelicula:
        return jsonify({"error": "Pelicula no encontrada"}), 404

    return jsonify({
        "id": pelicula.id,
        "titulo": pelicula.titulo,
        "descripcion": pelicula.descripcion,
        "categoria": pelicula.categoria,
        "region": pelicula.region,
        "imagen_url": pelicula.imagen_url,
        "video_url": pelicula.video_url,
        "hero_url": pelicula.hero_url,
        "tipo": pelicula.tipo
    }), 200
