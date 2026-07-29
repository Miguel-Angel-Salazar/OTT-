from flask import Blueprint
from flask import session
from flask import redirect
from flask import url_for
from flask import request

from services.favorite_service import toggle_favorito

# blueprint de favoritos (agregar/quitar de mi lista)
favorite_bp = Blueprint(
    "favorite",
    __name__,
    url_prefix="/favorite"
)


# agrega o quita una pelicula de mi lista y vuelve a donde estaba
# (este boton lo usan tanto el hero del home como el detalle de pelicula)
@favorite_bp.route("/toggle/<int:pelicula_id>", methods=["POST"])
def toggle(pelicula_id):

    usuario = session.get("usuario")

    # sin sesion no se puede tener favoritos
    if usuario is None:

        return redirect(url_for("auth.login"))

    toggle_favorito(
        usuario["id"],
        pelicula_id
    )

    # volvemos a la pagina de donde vino el form, si no hay referer caemos al detalle
    return redirect(
        request.referrer or url_for(
            "movie.detalle",
            movie_id=pelicula_id
        )
    )
