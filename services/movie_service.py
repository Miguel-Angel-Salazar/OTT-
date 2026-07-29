from config.supabase_config import supabase
from models.movie import Movie


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
        return []