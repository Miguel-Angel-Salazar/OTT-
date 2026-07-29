from config.supabase_config import supabase




def es_favorito(usuario_id, pelicula_id):

    response = (
        supabase.table("favorites")
        .select("*")
        .eq("usuario_id", usuario_id)
        .eq("pelicula_id", pelicula_id)
        .execute()
    )

    return len(response.data) > 0


def agregar_favorito(usuario_id, pelicula_id):

    supabase.table("favorites").insert(
        {
            "usuario_id": usuario_id,
            "pelicula_id": pelicula_id
        }
    ).execute()


def eliminar_favorito(usuario_id, pelicula_id):

    (
        supabase.table("favorites")
        .delete()
        .eq("usuario_id", usuario_id)
        .eq("pelicula_id", pelicula_id)
        .execute()
    )


def toggle_favorito(usuario_id, pelicula_id):

    if es_favorito(usuario_id, pelicula_id):

        eliminar_favorito(usuario_id, pelicula_id)

    else:

        agregar_favorito(usuario_id, pelicula_id)

def obtener_favoritos(usuario_id, peliculas):

    response = (
        supabase.table("favorites")
        .select("pelicula_id")
        .eq("usuario_id", usuario_id)
        .execute()
    )

    ids = [fila["pelicula_id"] for fila in response.data]

    return [
        pelicula
        for pelicula in peliculas
        if pelicula["id"] in ids
    ]