import os

from dotenv import load_dotenv
from flask import Flask, redirect, url_for

# blueprints de cada modulo de la app
from controllers.auth_controller import auth_bp
from controllers.home_controller import home_bp
from controllers.movie_controller import movie_bp
from controllers.profile_controller import profile_bp
from controllers.favorite_controller import favorite_bp


# carga las variables del .env (supabase, secret key, etc)
load_dotenv()

app = Flask(__name__)

# clave para firmar la sesion de flask
app.secret_key = os.getenv("SECRET_KEY")

# registrar cada blueprint en la app
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(favorite_bp)

@app.route("/")
def inicio():
    """Redirige al módulo de autenticación."""
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True)
