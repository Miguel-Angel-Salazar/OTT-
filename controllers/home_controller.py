from flask import Blueprint, render_template, session
from services.favorite_service import obtener_favoritos
from data.mock_movies import PELICULAS_MOCK

# Blueprint del home
home_bp = Blueprint(
    "home",
    __name__,
    url_prefix="/home"
)

# TODO: reemplazar por movie_service.listar_peliculas() (tabla `movies` de
# Supabase) cuando ese servicio exista. Estos son datos de muestra solo para
# poder maquetar/ver el catálogo mientras el backend de películas no existe.
# `hero_url` no es una columna real de `movies` (el esquema solo tiene
# `imagen_url`) — se agrega aquí únicamente para el banner grande del home.
# `video_url` sí es columna real, pero como no tenemos videos propios subidos
# todavía, las 6 apuntan al mismo video de muestra de dominio público
# (Big Buck Bunny) solo para poder probar el reproductor.


@home_bp.route("/")
def inicio():

    destacada = PELICULAS_MOCK[0]
    colombianas = [m for m in PELICULAS_MOCK if "Colombiano" in m["categoria"]]

    usuario = session.get("usuario")

    mi_lista = []

    if usuario:
        mi_lista = obtener_favoritos(
        usuario["id"],
        PELICULAS_MOCK
    )

    return render_template(
        "home.html",
        active_page="home",
        current_user=usuario,
        destacada=destacada,
        recomendadas=PELICULAS_MOCK,
        mi_lista=mi_lista,
        cine_colombiano=colombianas,
    )


@home_bp.route("/onboarding")
def onboarding():

    return render_template("onboarding.html")