from config.supabase_config import supabase
from models.movie import Movie


def listar_peliculas():

    response = (
        supabase
        .table("movies")
        .select("*")
        .execute()
    )

    peliculas = []

    for fila in response.data:

        peliculas.append(
            Movie(
                id=fila["id"],
                titulo=fila["titulo"],
                descripcion=fila["descripcion"],
                categoria=fila["categoria"],
                region=fila["region"],
                imagen_url=fila["imagen_url"],
                video_url=fila["video_url"]
            )
        )

    return peliculas