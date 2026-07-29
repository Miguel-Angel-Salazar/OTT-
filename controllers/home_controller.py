from flask import Blueprint, render_template, session
from services.favorite_service import obtener_favoritos
from models.movie import Movie

# Lista de películas construida a partir de archivos estáticos usando la clase `Movie`.
PELICULAS = [
    Movie(
        id=1,
        titulo="Narcos - Demo",
        descripcion="Episodio demo para pruebas de reproductor.",
        categoria="Colombiano",
        region="Colombia",
        imagen_url="/static/images/posters/narcos.jpg",
        video_url="/static/videos/narcos.mp4",
        hero_url="/static/images/posters/narcos.jpg",
    ),
    Movie(
        id=2,
        titulo="Breaking Bad - Demo",
        descripcion="Video de muestra para pruebas.",
        categoria="Drama",
        region="USA",
        imagen_url="/static/images/posters/breaking_bad.jpg",
        video_url="/static/videos/narcos.mp4",
    ),
    Movie(
        id=3,
        titulo="Dark - Demo",
        descripcion="Video de ejemplo.",
        categoria="Suspenso",
        region="Alemania",
        imagen_url="/static/images/posters/dark.jpg",
        video_url="/static/videos/narcos.mp4",
    ),
    Movie(
        id=4,
        titulo="La Casa de Papel - Demo",
        descripcion="Prueba de reproductor con subtítulos.",
        categoria="Acción",
        region="España",
        imagen_url="/static/images/posters/la_casa_de_papel.jpg",
        video_url="/static/videos/narcos.mp4",
    ),
    Movie(
        id=5,
        titulo="Peaky Blinders - Demo",
        descripcion="Video de prueba.",
        categoria="Drama",
        region="Reino Unido",
        imagen_url="/static/images/posters/peaky_blinders.jpg",
        video_url="/static/videos/narcos.mp4",
    ),
    Movie(
        id=6,
        titulo="Avatar - Demo",
        descripcion="Entrada de ejemplo.",
        categoria="Aventura",
        region="Internacional",
        imagen_url="/static/images/posters/avatar.jpg",
        video_url="/static/videos/narcos.mp4",
    ),
]

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

    destacada = PELICULAS[0]
    colombianas = [m for m in PELICULAS if "Colombiano" in m.categoria]

    usuario = session.get("usuario")

    mi_lista = []

    if usuario:
        mi_lista = obtener_favoritos(
            usuario["id"],
            PELICULAS
        )
    print("Favoritos:", mi_lista)
    
    return render_template(
        "home.html",
        active_page="home",
        current_user=usuario,
        destacada=destacada,
        recomendadas=PELICULAS,
        mi_lista=mi_lista,
        cine_colombiano=colombianas,
    )


@home_bp.route("/onboarding")
def onboarding():

    return render_template("onboarding.html")