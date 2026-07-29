from flask import Blueprint, render_template, session, redirect, url_for, request
from services.profile_service import actualizar_suscripcion

profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/profile"
)


@profile_bp.route("/", methods=["GET", "POST"])
def profile():

    usuario = session.get("usuario")

    if usuario is None:
        return redirect(url_for("auth.login"))
        
    if request.method == "POST":

        print("Entró al POST")

        nuevo_plan = request.form["plan"]

    # Validamos que el plan sea uno permitido
        if nuevo_plan not in ["Basica", "Premium"]:
            return redirect(url_for("profile.profile"))

        print("Plan:", nuevo_plan)

        if actualizar_suscripcion(
            usuario["id"],
            nuevo_plan
        ):

            print("Actualizado")

            session["usuario"]["suscripcion"] = nuevo_plan

        else:

            print("No actualizado")

        return redirect(url_for("profile.profile"))
    
    return render_template(
        "profile.html",
        current_user=session["usuario"]
    )