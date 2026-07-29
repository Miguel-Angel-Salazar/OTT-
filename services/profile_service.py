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


# cambiar contraseña

def cambiar_password(email, current_password, new_password):

    try:

        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": current_password
            }
        )

        if response.user is None:

            return "La contraseña actual es incorrecta."

        response = supabase.auth.update_user(
            {
                "password": new_password
            }
        )

        if response.user is None:

            return "No se pudo actualizar la contraseña."

        return "Contraseña actualizada correctamente."

    except Exception as e:

        print(e)

        return "Ocurrió un error al cambiar la contraseña."