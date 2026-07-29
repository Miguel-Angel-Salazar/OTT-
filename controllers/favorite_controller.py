from flask import Blueprint
from flask import session
from flask import redirect
from flask import url_for

from services.favorite_service import toggle_favorito

favorite_bp = Blueprint(
    "favorite",
    __name__,
    url_prefix="/favorite"
)


@favorite_bp.route("/toggle/<int:pelicula_id>", methods=["POST"])
def toggle(pelicula_id):

    usuario = session.get("usuario")

    if usuario is None:

        return redirect(url_for("auth.login"))

    toggle_favorito(
        usuario["id"],
        pelicula_id
    )

    return redirect(
        url_for(
            "movie.detalle",
            movie_id=pelicula_id
        )
    )