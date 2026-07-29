from config.supabase_config import supabase


# guardar historial

def guardar_historial(usuario_id, pelicula_id, minuto):

    try:

        existe = (
            supabase.table("watch_history")
            .select("id")
            .eq("usuario_id", usuario_id)
            .eq("pelicula_id", pelicula_id)
            .execute()
        )

        if existe.data:

            supabase.table("watch_history").update(
                {
                    "minuto": minuto
                }
            ).eq(
                "usuario_id",
                usuario_id
            ).eq(
                "pelicula_id",
                pelicula_id
            ).execute()

        else:

            supabase.table("watch_history").insert(
                {
                    "usuario_id": usuario_id,
                    "pelicula_id": pelicula_id,
                    "minuto": minuto
                }
            ).execute()

        return True

    except Exception as e:

        print(e)

        return False


# obtener historial

def obtener_historial(usuario_id, pelicula_id):

    try:

        respuesta = (
            supabase.table("watch_history")
            .select("minuto")
            .eq("usuario_id", usuario_id)
            .eq("pelicula_id", pelicula_id)
            .single()
            .execute()
        )

        if respuesta.data:

            return respuesta.data["minuto"]

        return 0

    except Exception:

        return 0