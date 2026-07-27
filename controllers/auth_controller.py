from flask import Blueprint, render_template, request
from services.auth_service import register_user, login_user
# creamos el Blueprint de autenticacion
auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)

#mostrar el login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    email = request.form["email"]
    password = request.form["password"]

    usuario = login_user(
        email,
        password
    )

    if usuario:

        return render_template("home.html")

    return render_template(
        "login.html",
        mensaje="Correo o contraseña incorrectos."
    )

#mostrar el registro
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
# Si entra desde la URL
    if request.method == "GET":
        return render_template("register.html")

    # Si presiona el botón "Crear cuenta"
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
    "register.html",
    mensaje=mensaje
)