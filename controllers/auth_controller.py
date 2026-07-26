from flask import Blueprint, render_template

# creamos el Blueprint de autenticacion
auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)

#mostrar el login
@auth_bp.route("/login")
def login():
    return render_template("login.html")

#mostrar el registro
@auth_bp.route("/register")
def register():
    return render_template("register.html")