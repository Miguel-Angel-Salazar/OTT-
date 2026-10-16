from config.db_config import get_connection


# revisa si esa pelicula ya esta en favoritos del usuario
def es_favorito(usuario_id, pelicula_id):

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT 1 FROM favorites WHERE usuario_id = %s AND pelicula_id = %s",
            (usuario_id, pelicula_id)
        )
        result = cur.fetchone()

        cur.close()
        conn.close()

        return result is not None

    except Exception as e:
        print(e)
        return False


# inserta la pelicula en favorites
def agregar_favorito(usuario_id, pelicula_id):

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO favorites (usuario_id, pelicula_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (usuario_id, pelicula_id)
        )

        conn.commit()
        cur.close()
        conn.close()

        return True

    except Exception as e:
        print(e)
        return False


# borra la pelicula de favorites
def eliminar_favorito(usuario_id, pelicula_id):

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM favorites WHERE usuario_id = %s AND pelicula_id = %s",
            (usuario_id, pelicula_id)
        )

        conn.commit()
        cur.close()
        conn.close()

        return True

    except Exception as e:
        print(e)
        return False


# si ya es favorito lo quita, si no lo agrega
def toggle_favorito(usuario_id, pelicula_id):

    if es_favorito(usuario_id, pelicula_id):

        return eliminar_favorito(usuario_id, pelicula_id)

    else:

        return agregar_favorito(usuario_id, pelicula_id)

# de la lista completa de peliculas, deja solo las que son favoritas del usuario
def obtener_favoritos(usuario_id, peliculas):

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT pelicula_id FROM favorites WHERE usuario_id = %s",
            (usuario_id,)
        )
        rows = cur.fetchall()

        cur.close()
        conn.close()

        ids = [fila["pelicula_id"] for fila in rows]

    except Exception as e:
        print(e)
        return []

    # funciona tanto si pelicula es un dict como si es un objeto Movie
    def _get_id(pelicula):
        if isinstance(pelicula, dict):
            return pelicula.get("id")
        return getattr(pelicula, "id", None)

    return [
        pelicula
        for pelicula in peliculas
        if _get_id(pelicula) in ids
    ]
