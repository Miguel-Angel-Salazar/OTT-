from config.supabase_config import supabase


# crea la cuenta en supabase auth y guarda el registro en profiles

def register_user(nombre, email, password, region):

    try:

        # crear usuario en supabase auth
        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {
                    "email_redirect_to": "http://127.0.0.1:5000/auth/login"
                }
            }
        )

        # verificar que el usuario se creo
        if response.user is None:
            return "No se pudo crear la cuenta."

        # guarda informacion adicional (nombre, region) en la tabla profiles
        supabase.table("profiles").insert(
            {
                "id": response.user.id,
                "nombre": nombre,
                "region": region
            }
        ).execute()

        # devolvemos el usuario (no un mensaje) para que el controller sepa
        # que si funciono, igual que hace login_user
        return response.user

    except Exception as e:

        print("ERROR REGISTER:", e)
        return f"Error: {str(e)}"



# valida el email y clave contra supabase auth

def login_user(email, password):

    try:

        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )

        # credenciales invalidas
        if response.user is None:
            return None

        return response.user

    except Exception as e:

        print("ERROR LOGIN:", e)
        return str(e)


# perfil (nombre, region, suscripcion) - la tabla profiles, no viene en el
# objeto de supabase auth
def obtener_perfil(usuario_id):

    try:

        response = (
            supabase.table("profiles")
            .select("nombre, region, suscripcion")
            .eq("id", usuario_id)
            .single()
            .execute()
        )

        return response.data

    except Exception as e:

        print("ERROR PERFIL:", e)
        return None

# manda el correo de recuperacion de clave (lo maneja supabase auth)

def enviar_correo_recuperacion(email):

    try:

        supabase.auth.reset_password_for_email(
            email,
            {
                "redirect_to": "http://127.0.0.1:5000/auth/reset-password"
            }
        )

        # siempre devolvemos el mismo mensaje, asi no se sabe si el correo existe o no
        return "Si el correo está registrado, recibirás un enlace para recuperar tu contraseña."

    except Exception as e:

        print("ERROR RECUPERACION:", e)
        return f"Error: {str(e)}"



# cambia la clave del usuario que ya viene autenticado por el link del correo

def actualizar_password(password):

    try:

        response = supabase.auth.update_user(
            {
                "password": password
            }
        )

        if response.user is None:
            return "No se pudo actualizar la contraseña."

        return "Contraseña actualizada correctamente."

    except Exception as e:

        print("ERROR CAMBIO PASSWORD:", e)
        return f"Error: {str(e)}"
