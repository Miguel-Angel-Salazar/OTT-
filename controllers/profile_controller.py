from flask import Blueprint, render_template, session, redirect, url_for, request
from services.profile_service import actualizar_suscripcion, cambiar_password

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

        # cambiar contraseña

        if "current_password" in request.form:

            current_password = request.form["current_password"]
            new_password = request.form["new_password"]
            confirm_password = request.form["confirm_password"]

            if new_password != confirm_password:

                return render_template(
                    "profile.html",
                    current_user=session["usuario"],
                    mensaje_password="Las contraseñas no coinciden."
                )

            if current_password == new_password:

                return render_template(
                    "profile.html",
                    current_user=session["usuario"],
                    mensaje_password="La nueva contraseña debe ser diferente a la actual."
                )

            mensaje = cambiar_password(
                usuario["email"],
                current_password,
                new_password
            )

            return render_template(
                "profile.html",
                current_user=session["usuario"],
                mensaje_password=mensaje
            )

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