from flask import Blueprint, render_template, session, url_for, abort, redirect, request, jsonify


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

from services.favorite_service import es_favorito

# blueprint de peliculas (detalle, busqueda, likes, historial)
movie_bp = Blueprint(
    "movie",
    __name__,
    url_prefix="/movie"
)


# pagina de detalle de una pelicula con el reproductor
@movie_bp.route("/<int:movie_id>")
def detalle(movie_id):

    peliculas = listar_peliculas()
    pelicula = next((m for m in peliculas if m.id == movie_id), None)

    # si el id no existe en el catalogo, 404
    if pelicula is None:
        abort(404)

    recomendaciones = [m for m in peliculas if m.id != movie_id]

    likes = obtener_likes(movie_id)

    dislikes = obtener_dislikes(movie_id)

    minuto = 0
    favorito = False

    usuario = session.get("usuario")

    # el minuto guardado y el estado de favorito solo aplican si hay sesion
    if usuario is not None:

        minuto = obtener_historial(
            usuario["id"],
            movie_id
        )

        favorito = es_favorito(
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
        minuto=minuto,
        favorito=favorito
    )


# busca peliculas por titulo, categoria, descripcion o region
@movie_bp.route("/search")
def search():
    query = request.args.get("q", "").strip()
    peliculas = listar_peliculas()

    # si no hay texto buscado no mostramos resultados
    if query:
        lowercase_query = query.lower()
        resultados = [
            m for m in peliculas
            if lowercase_query in (m.titulo or "").lower()
            or lowercase_query in (m.categoria or "").lower()
            or lowercase_query in (m.descripcion or "").lower()
            or lowercase_query in (m.region or "").lower()
        ]
    else:
        resultados = []

    return render_template(
        "movie_search.html",
        current_user=session.get("usuario"),
        query=query,
        resultados=resultados,
        active_page="catalog"
    )


# marca like a una pelicula y regresa al detalle
@movie_bp.route("/<int:movie_id>/like")
def like(movie_id):

    usuario = session.get("usuario")

    # sin sesion no se puede calificar
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


# marca dislike a una pelicula y regresa al detalle
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


# guarda el minuto del video (lo llama el reproductor cada rato via fetch)
@movie_bp.route("/<int:movie_id>/progreso", methods=["POST"])
def progreso(movie_id):

    usuario = session.get("usuario")

    # sin sesion no guardamos progreso, 401 para que el js no reintente mal
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
