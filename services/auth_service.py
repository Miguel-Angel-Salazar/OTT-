from config.supabase_config import supabase


def register_user(nombre, email, password, region):
    try:

        # Crear usuario en Supabase Auth
        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password
            }
        )

        # Si no se creó el usuario
        if response.user is None:
            return "No se pudo crear la cuenta."

        # Guardar información adicional en nuestra tabla profiles
        supabase.table("profiles").insert(
            {
                "id": response.user.id,
                "nombre": nombre,
                "region": region
            }
        ).execute()

        return "Cuenta creada correctamente. Revisa tu correo para verificarla."

    except Exception as e:
        return f"Error: {str(e)}"

def login_user(email, password):

    try:

        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )

        if response.user is None:
            return None

        return response.user

    except Exception:

        return None