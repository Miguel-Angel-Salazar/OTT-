from config.supabase_config import supabase


def actualizar_suscripcion(user_id, nuevo_plan):

    try:

        respuesta = supabase.table("profiles").update(
            {
                "suscripcion": nuevo_plan
            }
        ).eq(
            "id",
            user_id
        ).execute()

        print(respuesta)

        return True

    except Exception as e:

        print(e)

        return False