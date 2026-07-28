from flask import Blueprint, render_template, session, url_for, abort

# TODO: reemplazar por movie_service.py (consultando la tabla `movies` de
# Supabase) cuando ese servicio exista. Por ahora reusamos los mismos datos
# de muestra que ya usa home.html para no duplicar la lista.
from controllers.home_controller import PELICULAS_MOCK

# Blueprint de peliculas
movie_bp = Blueprint(
    "movie",
    __name__,
    url_prefix="/movie"
)


@movie_bp.route("/<int:movie_id>")
def detalle(movie_id):

    pelicula = next((m for m in PELICULAS_MOCK if m["id"] == movie_id), None)

    if pelicula is None:
        abort(404)

    recomendaciones = [m for m in PELICULAS_MOCK if m["id"] != movie_id]

    return render_template(
        "movie_detail.html",
        current_user=session.get("usuario"),
        navbar_variant="detail",
        back_url=url_for("home.inicio"),
        movie=pelicula,
        recomendaciones=recomendaciones,
    )
