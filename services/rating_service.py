from config.supabase_config import supabase


# guarda o actualiza el like/dislike del usuario para esa pelicula
# valor 1 = like, valor -1 = dislike

def calificar_pelicula(usuario_id, pelicula_id, valor):

    try:

        # revisa si el usuario ya habia calificado esta pelicula
        existente = (
            supabase.table("ratings")
            .select("id")
            .eq("usuario_id", usuario_id)
            .eq("pelicula_id", pelicula_id)
            .execute()
        )

        if existente.data:

            # ya existe, solo actualizamos el valor
            supabase.table("ratings").update(
                {
                    "valor": valor
                }
            ).eq(
                "usuario_id",
                usuario_id
            ).eq(
                "pelicula_id",
                pelicula_id
            ).execute()

        else:

            # primera vez que califica, insertamos
            supabase.table("ratings").insert(
                {
                    "usuario_id": usuario_id,
                    "pelicula_id": pelicula_id,
                    "valor": valor
                }
            ).execute()

        return True

    except Exception as e:

        print(e)

        return False


# cuenta cuantos likes tiene la pelicula

def obtener_likes(pelicula_id):

    try:

        response = (
            supabase.table("ratings")
            .select("*", count="exact")
            .eq("pelicula_id", pelicula_id)
            .eq("valor", 1)
            .execute()
        )

        return response.count

    except Exception:

        return 0


# cuenta cuantos dislikes tiene la pelicula

def obtener_dislikes(pelicula_id):

    try:

        response = (
            supabase.table("ratings")
            .select("*", count="exact")
            .eq("pelicula_id", pelicula_id)
            .eq("valor", -1)
            .execute()
        )

        return response.count

    except Exception:

        return 0
