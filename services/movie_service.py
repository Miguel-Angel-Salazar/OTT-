from config.supabase_config import supabase
from models.movie import Movie


# trae todas las peliculas de la tabla movies y las pasa a objetos Movie
def listar_peliculas():
    try:
        response = (
            supabase
            .table("movies")
            .select("*")
            .execute()
        )

        data = response.data or []
        return [Movie.from_dict(fila) for fila in data]
    except Exception:
        # si supabase falla devolvemos catalogo vacio en vez de tronar la pagina
        return []
