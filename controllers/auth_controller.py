from flask import Blueprint, render_template, request, redirect, url_for, session
from services.auth_service import register_user, login_user, obtener_perfil

# creamos el Blueprint de autenticacion
auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)

#mostrar el login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # url
    if request.method == "GET":
        return render_template("auth/login.html", current_user=session.get("usuario"))

    email = request.form["email"]
    password = request.form["password"]

    usuario = login_user(email, password)

    # devolvió un usuario
    if not isinstance(usuario, str) and usuario is not None:

        perfil = obtener_perfil(usuario.id)

        # guardamos lo minimo necesario en la sesion de Flask
        session["usuario"] = {
            "id": usuario.id,
            "email": usuario.email,
            "nombre": perfil["nombre"] if perfil else usuario.email,
            "suscripcion": perfil["suscripcion"] if perfil else "Sin plan",
        }

        return redirect(url_for("home.inicio"))

    # erro
    return render_template(
        "auth/login.html",
        mensaje=usuario,
        current_user=session.get("usuario"),
    )
#mostrar el registro
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
# Si entra desde la URL
    if request.method == "GET":
        return render_template("auth/register.html", current_user=session.get("usuario"))

    nombre = request.form["nombre"]
    email = request.form["email"]
    password = request.form["password"]
    region = request.form["region"]

    mensaje = register_user(
    nombre,
    email,
    password,
    region,
)

    return render_template(
    "auth/register.html",
    mensaje=mensaje,
    current_user=session.get("usuario"),
)


#cerrar la sesion
@auth_bp.route("/logout")
def logout():

    session.pop("usuario", None)
    return redirect(url_for("auth.login"))