from config.db_config import get_connection


# guarda o actualiza el like/dislike del usuario para esa pelicula
# valor 1 = like, valor -1 = dislike

def calificar_pelicula(usuario_id, pelicula_id, valor):

    try:

        conn = get_connection()
        cur = conn.cursor()

        # usa UPSERT para insertar o actualizar en una sola operacion
        cur.execute("""
            INSERT INTO ratings (usuario_id, pelicula_id, valor)
            VALUES (%s, %s, %s)
            ON CONFLICT (usuario_id, pelicula_id)
            DO UPDATE SET valor = EXCLUDED.valor
        """, (usuario_id, pelicula_id, valor))

        conn.commit()
        cur.close()
        conn.close()

        return True

    except Exception as e:

        print(e)

        return False


# cuenta cuantos likes tiene la pelicula

def obtener_likes(pelicula_id):

    try:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT COUNT(*) AS total FROM ratings WHERE pelicula_id = %s AND valor = 1",
            (pelicula_id,)
        )
        result = cur.fetchone()

        cur.close()
        conn.close()

        return result["total"] if result else 0

    except Exception:

        return 0


# cuenta cuantos dislikes tiene la pelicula

def obtener_dislikes(pelicula_id):

    try:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT COUNT(*) AS total FROM ratings WHERE pelicula_id = %s AND valor = -1",
            (pelicula_id,)
        )
        result = cur.fetchone()

        cur.close()
        conn.close()

        return result["total"] if result else 0

    except Exception:

        return 0
