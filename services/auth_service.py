import bcrypt
from types import SimpleNamespace
from config.db_config import get_connection


# crea la cuenta en la tabla users y guarda el registro en profiles

def register_user(nombre, email, password, region):

    try:

        conn = get_connection()
        cur = conn.cursor()

        # verificar si el correo ya esta registrado
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))

        if cur.fetchone():
            cur.close()
            conn.close()
            return "El correo ya está registrado."

        # hashear la contraseña con bcrypt
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # crear usuario en la tabla users
        cur.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id",
            (email, password_hash)
        )
        user_row = cur.fetchone()
        user_id = user_row["id"]

        # guarda informacion adicional (nombre, region) en la tabla profiles
        cur.execute(
            "INSERT INTO profiles (id, nombre, region) VALUES (%s, %s, %s)",
            (user_id, nombre, region)
        )

        conn.commit()
        cur.close()
        conn.close()

        # devolvemos un objeto con id y email para que el controller sepa
        # que si funciono, igual que hacia con supabase
        return SimpleNamespace(id=user_id, email=email)

    except Exception as e:

        print("ERROR REGISTER:", e)
        return f"Error: {str(e)}"



# valida el email y clave contra la tabla users con bcrypt

def login_user(email, password):

    try:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, email, password_hash FROM users WHERE email = %s",
            (email,)
        )
        user = cur.fetchone()

        cur.close()
        conn.close()

        # si no existe el usuario
        if user is None:
            return "Credenciales inválidas."

        # verificar la contraseña con bcrypt
        if not bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        ):
            return "Credenciales inválidas."

        return SimpleNamespace(id=user["id"], email=user["email"])

    except Exception as e:

        print("ERROR LOGIN:", e)
        return str(e)


# perfil (nombre, region, suscripcion) de la tabla profiles
def obtener_perfil(usuario_id):

    try:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT nombre, region, suscripcion FROM profiles WHERE id = %s",
            (usuario_id,)
        )
        perfil = cur.fetchone()

        cur.close()
        conn.close()

        return dict(perfil) if perfil else None

    except Exception as e:

        print("ERROR PERFIL:", e)
        return None


# la recuperacion de clave por correo requiere configurar SMTP.
# por ahora devolvemos un mensaje informativo.

def enviar_correo_recuperacion(email):

    return (
        "La recuperación de contraseña por correo no está disponible "
        "en este momento. Contacte al administrador."
    )


# el cambio de clave desde un link externo requiere un flujo con tokens.
# por ahora se puede cambiar desde el perfil con la clave actual.

def actualizar_password(password):

    return (
        "La recuperación de contraseña por enlace no está disponible "
        "en este momento. Use la opción de cambiar contraseña desde su perfil."
    )
