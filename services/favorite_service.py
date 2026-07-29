from config.supabase_config import supabase


# revisa si esa pelicula ya esta en favoritos del usuario
def es_favorito(usuario_id, pelicula_id):

    try:
        response = (
            supabase.table("favorites")
            .select("*")
            .eq("usuario_id", usuario_id)
            .eq("pelicula_id", pelicula_id)
            .execute()
        )

        return len(response.data) > 0

    except Exception as e:
        print(e)
        return False


# inserta la pelicula en favorites
def agregar_favorito(usuario_id, pelicula_id):

    try:
        supabase.table("favorites").insert(
            {
                "usuario_id": usuario_id,
                "pelicula_id": pelicula_id
            }
        ).execute()

        return True

    except Exception as e:
        print(e)
        return False


# borra la pelicula de favorites
def eliminar_favorito(usuario_id, pelicula_id):

    try:
        (
            supabase.table("favorites")
            .delete()
            .eq("usuario_id", usuario_id)
            .eq("pelicula_id", pelicula_id)
            .execute()
        )

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
        response = (
            supabase.table("favorites")
            .select("pelicula_id")
            .eq("usuario_id", usuario_id)
            .execute()
        )

        ids = [fila["pelicula_id"] for fila in response.data]

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
