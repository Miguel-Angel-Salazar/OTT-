from flask import Blueprint, render_template, session
from services.favorite_service import obtener_favoritos
from services.movie_service import listar_peliculas

# Blueprint del home
home_bp = Blueprint(
    "home",
    __name__,
    url_prefix="/home"
)




@home_bp.route("/")
def inicio():

    peliculas = listar_peliculas()
    usuario = session.get("usuario")
    user_region = (usuario.get("region") if usuario else "") or ""
    user_region = user_region.strip()

    if usuario and user_region:
        peliculas = [
            m for m in peliculas
            if m.region and m.region.strip().lower() == user_region.lower()
        ]

    destacada = peliculas[0] if peliculas else None
    colombianas = [m for m in peliculas if "Colombiano" in (m.categoria or "")]

    mi_lista = []

    if usuario:
        mi_lista = obtener_favoritos(
            usuario["id"],
            peliculas
        )
    print("Favoritos:", mi_lista)
    
    return render_template(
        "home.html",
        active_page="home",
        current_user=usuario,
        destacada=destacada,
        recomendadas=peliculas,
        mi_lista=mi_lista,
        cine_colombiano=colombianas,
    )


@home_bp.route("/onboarding")
def onboarding():

    return render_template("onboarding.html")