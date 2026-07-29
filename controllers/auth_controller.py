from flask import Blueprint, render_template, request, redirect, url_for, session
from services.auth_service import register_user, login_user, obtener_perfil, enviar_correo_recuperacion, actualizar_password

# blueprint de autenticacion (login, registro, recuperar clave, logout)
auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)

# muestra el form de login y procesa el intento de inicio de sesion
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # si entra por url normal solo muestra el formulario
    if request.method == "GET":
        return render_template("auth/login.html", current_user=session.get("usuario"))

    email = request.form["email"]
    password = request.form["password"]

    usuario = login_user(email, password)

    # si login_user devolvio un usuario real (no un string de error) fue exitoso
    if not isinstance(usuario, str) and usuario is not None:

        # traemos nombre, region y suscripcion de la tabla profiles
        perfil = obtener_perfil(usuario.id)

        # guardamos lo minimo necesario en la sesion de flask
        session["usuario"] = {
        "id": usuario.id,
        "email": usuario.email,
        "nombre": perfil["nombre"] if perfil else usuario.email,
        "region": perfil["region"] if perfil else "",
        "suscripcion": perfil["suscripcion"] if perfil else "Sin plan",
        }

        return redirect(url_for("home.inicio"))

    # credenciales invalidas, se queda en el login mostrando el error
    return render_template(
        "auth/login.html",
        mensaje=usuario,
        current_user=session.get("usuario"),
    )

# muestra el form de registro y crea la cuenta nueva
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
# si entra por url solo muestra el formulario
    if request.method == "GET":
        return render_template("auth/register.html", current_user=session.get("usuario"))

    nombre = request.form["nombre"]
    email = request.form["email"]
    password = request.form["password"]
    region = request.form["region"]

    resultado = register_user(
    nombre,
    email,
    password,
    region,
)

    # si salio bien nos manda a la encuesta de generos, si no se queda
    # en el formulario mostrando el error
    if not isinstance(resultado, str) and resultado is not None:
        return redirect(url_for("home.onboarding"))

    return render_template(
    "auth/register.html",
    mensaje=resultado,
    current_user=session.get("usuario"),
)


# manda el correo con el link para recuperar la clave
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "GET":
        return render_template(
            "auth/forgot_password.html",
            current_user=session.get("usuario")
        )

    email = request.form["email"]

    mensaje = enviar_correo_recuperacion(email)

    return render_template(
        "auth/forgot_password.html",
        mensaje=mensaje,
        current_user=session.get("usuario")
    )


# pantalla que llega desde el link del correo para poner clave nueva
@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    if request.method == "GET":
        return render_template(
            "auth/reset_password.html",
            current_user=session.get("usuario")
        )

    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    # las dos claves deben coincidir antes de intentar el cambio
    if password != confirm_password:

        return render_template(
            "auth/reset_password.html",
            mensaje="Las contraseñas no coinciden.",
            current_user=session.get("usuario")
        )

    mensaje = actualizar_password(password)

    return render_template(
        "auth/reset_password.html",
        mensaje=mensaje,
        current_user=session.get("usuario")
    )


# borra la sesion y manda de vuelta al login
@auth_bp.route("/logout")
def logout():

    session.pop("usuario", None)
    return redirect(url_for("auth.login"))
