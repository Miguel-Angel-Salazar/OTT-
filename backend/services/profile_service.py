import bcrypt
from config.db_config import get_connection


# cambia el plan de suscripcion del usuario en la tabla profiles
def actualizar_suscripcion(user_id, nuevo_plan):

    try:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE profiles SET suscripcion = %s WHERE id = %s",
            (nuevo_plan, user_id)
        )

        conn.commit()

        print(f"Suscripcion actualizada a '{nuevo_plan}' para usuario {user_id}")

        cur.close()
        conn.close()

        return True

    except Exception as e:

        print(e)

        return False


# cambia la contraseña del perfil (pide la clave actual primero)

def cambiar_password(email, current_password, new_password):

    try:

        conn = get_connection()
        cur = conn.cursor()

        # traemos el hash actual para verificar la clave
        cur.execute(
            "SELECT id, password_hash FROM users WHERE email = %s",
            (email,)
        )
        user = cur.fetchone()

        if user is None:
            cur.close()
            conn.close()
            return "Usuario no encontrado."

        # reautenticamos con la clave actual para confirmar que si es el dueño
        if not bcrypt.checkpw(
            current_password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        ):
            cur.close()
            conn.close()
            return "La contraseña actual es incorrecta."

        # hashear la nueva contraseña y actualizar
        new_hash = bcrypt.hashpw(
            new_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cur.execute(
            "UPDATE users SET password_hash = %s WHERE id = %s",
            (new_hash, user["id"])
        )

        conn.commit()
        cur.close()
        conn.close()

        return "Contraseña actualizada correctamente."

    except Exception as e:

        print(e)

        return "Ocurrió un error al cambiar la contraseña."
