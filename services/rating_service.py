from config.supabase_config import supabase


# like o dislike

def calificar_pelicula(usuario_id, pelicula_id, valor):

    try:

        existente = (
            supabase.table("ratings")
            .select("id")
            .eq("usuario_id", usuario_id)
            .eq("pelicula_id", pelicula_id)
            .execute()
        )

        if existente.data:

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


# obtener cantidad de likes

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


# obtener cantidad de dislikes

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