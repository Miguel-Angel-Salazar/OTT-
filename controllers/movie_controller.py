from flask import Blueprint, render_template, session, url_for, abort, redirect, request, jsonify

# TODO: reemplazar por movie_service.py (consultando la tabla `movies` de
# Supabase) cuando ese servicio exista. Por ahora reusamos los mismos datos
# de muestra que ya usa home.html para no duplicar la lista.
from services.movie_service import listar_peliculas

from services.rating_service import (
    calificar_pelicula,
    obtener_likes,
    obtener_dislikes
)

from services.watch_history_service import (
    guardar_historial,
    obtener_historial
)

# Blueprint de peliculas
movie_bp = Blueprint(
    "movie",
    __name__,
    url_prefix="/movie"
)


@movie_bp.route("/<int:movie_id>")
def detalle(movie_id):

    peliculas = listar_peliculas()
    pelicula = next((m for m in peliculas if m.id == movie_id), None)

    if pelicula is None:
        abort(404)

    recomendaciones = [m for m in peliculas if m.id != movie_id]

    likes = obtener_likes(movie_id)

    dislikes = obtener_dislikes(movie_id)

    minuto = 0

    usuario = session.get("usuario")

    if usuario is not None:

        minuto = obtener_historial(
            usuario["id"],
            movie_id
        )

    return render_template(
        "movie_detail.html",
        current_user=session.get("usuario"),
        navbar_variant="detail",
        back_url=url_for("home.inicio"),
        movie=pelicula,
        recomendaciones=recomendaciones,
        likes=likes,
        dislikes=dislikes,
        minuto=minuto
    )


@movie_bp.route("/<int:movie_id>/like")
def like(movie_id):

    usuario = session.get("usuario")

    if usuario is None:

        return redirect(url_for("auth.login"))

    calificar_pelicula(
        usuario["id"],
        movie_id,
        1
    )

    return redirect(
        url_for(
            "movie.detalle",
            movie_id=movie_id
        )
    )


@movie_bp.route("/<int:movie_id>/dislike")
def dislike(movie_id):

    usuario = session.get("usuario")

    if usuario is None:

        return redirect(url_for("auth.login"))

    calificar_pelicula(
        usuario["id"],
        movie_id,
        -1
    )

    return redirect(
        url_for(
            "movie.detalle",
            movie_id=movie_id
        )
    )


# guardar historial

@movie_bp.route("/<int:movie_id>/progreso", methods=["POST"])
def progreso(movie_id):

    usuario = session.get("usuario")

    if usuario is None:

        return jsonify(
            {
                "ok": False
            }
        ), 401

    datos = request.get_json()

    minuto = datos["minuto"]

    guardar_historial(
        usuario["id"],
        movie_id,
        minuto
    )

    return jsonify(
        {
            "ok": True
        }
    )