from config.supabase_config import supabase


# register

def register_user(nombre, email, password, region):

    try:

        # crear usuario en Supabase Auth
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

        # guarda informacion adicional
        supabase.table("profiles").insert(
            {
                "id": response.user.id,
                "nombre": nombre,
                "region": region
            }
        ).execute()

        return "Cuenta creada correctamente. Revisa tu correo para verificarla."

    except Exception as e:

        print("ERROR REGISTER:", e)
        return f"Error: {str(e)}"



# login
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

    except Exception as e:

        print("ERROR LOGIN:", e)
        return str(e)