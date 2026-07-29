from flask import Blueprint, render_template, session
from services.favorite_service import obtener_favoritos
from services.movie_service import listar_peliculas

# blueprint del home (catalogo principal)
home_bp = Blueprint(
    "home",
    __name__,
    url_prefix="/home"
)


# pantalla principal: hero + carruseles de peliculas
@home_bp.route("/")
def inicio():

    peliculas = listar_peliculas()
    usuario = session.get("usuario")

    # si el usuario tiene region en su perfil, filtramos el catalogo por esa region
    user_region = (usuario.get("region") if usuario else "") or ""
    user_region = user_region.strip()

    if usuario and user_region:
        peliculas = [
            m for m in peliculas
            if m.region and m.region.strip().lower() == user_region.lower()
        ]

    # la primera pelicula del listado es la destacada del hero
    destacada = peliculas[0] if peliculas else None
    colombianas = [m for m in peliculas if "Colombiano" in (m.categoria or "")]

    mi_lista = []

    # solo si hay sesion buscamos los favoritos del usuario
    if usuario:
        mi_lista = obtener_favoritos(
            usuario["id"],
            peliculas
        )
    print("Favoritos:", mi_lista)

    # ver si la destacada ya esta en mi lista, para pintar el corazon lleno
    destacada_favorito = False
    if destacada:
        destacada_favorito = any(m.id == destacada.id for m in mi_lista)

    return render_template(
        "home.html",
        active_page="home",
        current_user=usuario,
        destacada=destacada,
        destacada_favorito=destacada_favorito,
        recomendadas=peliculas,
        mi_lista=mi_lista,
        cine_colombiano=colombianas,
    )


# encuesta de generos que se muestra despues de registrarse
@home_bp.route("/onboarding")
def onboarding():

    return render_template("onboarding.html")


# centro de ayuda: contactos de soporte del equipo
@home_bp.route("/ayuda")
def ayuda():

    return render_template(
        "help.html",
        current_user=session.get("usuario")
    )
