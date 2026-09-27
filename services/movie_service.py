from config.db_config import get_connection
from models.movie import Movie


# trae todas las peliculas de la tabla movies y las pasa a objetos Movie
def listar_peliculas():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM movies")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [Movie.from_dict(dict(fila)) for fila in rows]

    except Exception:
        # si la bd falla devolvemos catalogo vacio en vez de tronar la pagina
        return []
