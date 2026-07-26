import os

from dotenv import load_dotenv
from flask import Flask, redirect

from controllers.auth_controller import auth_bp

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(auth_bp)


@app.route("/")
def inicio():
    return redirect("/auth/login")


if __name__ == "__main__":
    app.run(debug=True)