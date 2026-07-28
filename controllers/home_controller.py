from flask import Blueprint, render_template

# Blueprint del home
home_bp = Blueprint(
    "home",
    __name__,
    url_prefix="/home"
)


@home_bp.route("/")
def inicio():

    return render_template("home.html")


@home_bp.route("/onboarding")
def onboarding():

    return render_template("onboarding.html")