import os

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask, redirect, url_for

# blueprints de cada modulo de la app
from controllers.auth_controller import auth_bp
from controllers.home_controller import home_bp
from controllers.movie_controller import movie_bp
from controllers.profile_controller import profile_bp
from controllers.favorite_controller import favorite_bp
from controllers.api_controller import api_bp


# carga las variables del .env (base de datos, secret key, etc)
load_dotenv()

app = Flask(__name__)

# clave para firmar la sesion de flask
app.secret_key = os.getenv("SECRET_KEY", "dev_secret_key_mubi_ott")

# configuracion de Swagger / OpenAPI
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API Plataforma OTT - Clon de MUBI",
        "description": "Documentación interactiva OpenAPI de los endpoints del backend para la plataforma de streaming.",
        "version": "1.0.0",
        "contact": {
            "name": "Equipo OTT (Paradigmas de Programación)"
        }
    }
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# registrar cada blueprint en la app
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(favorite_bp)
app.register_blueprint(api_bp)

@app.route("/")
def inicio():
    """Redirige al módulo de autenticación."""
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", os.getenv("FLASK_RUN_PORT", 5000)))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")
    app.run(host=host, port=port, debug=debug)
