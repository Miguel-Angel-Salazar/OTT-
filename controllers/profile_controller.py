from flask import Blueprint, render_template, session, redirect, url_for, request
from services.profile_service import actualizar_suscripcion, cambiar_password

# blueprint de perfil (datos de cuenta, suscripcion, cambio de clave)
profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/profile"
)


# pantalla de cuenta: ver datos, cambiar plan, cambiar clave
@profile_bp.route("/", methods=["GET", "POST"])
def profile():

    usuario = session.get("usuario")

    # sin sesion no hay perfil que mostrar
    if usuario is None:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        # este form trae current_password, es el de cambiar contraseña
        if "current_password" in request.form:

            current_password = request.form["current_password"]
            new_password = request.form["new_password"]
            confirm_password = request.form["confirm_password"]

            # la nueva clave y su confirmacion deben coincidir
            if new_password != confirm_password:

                return render_template(
                    "profile.html",
                    current_user=session["usuario"],
                    mensaje_password="Las contraseñas no coinciden."
                )

            # no dejamos poner la misma clave que ya tenia
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

        # si no trae current_password, es el form de cambiar de plan
        nuevo_plan = request.form["plan"]

        # validamos que el plan sea uno permitido
        if nuevo_plan not in ["Basica", "Premium"]:
            return redirect(url_for("profile.profile"))

        print("Plan:", nuevo_plan)

        if actualizar_suscripcion(
            usuario["id"],
            nuevo_plan
        ):

            print("Actualizado")

            # actualizamos tambien la sesion para que el navbar refleje el plan nuevo
            session["usuario"]["suscripcion"] = nuevo_plan

        else:

            print("No actualizado")

        return redirect(url_for("profile.profile"))

    # si entra por get solo muestra la info actual
    return render_template(
        "profile.html",
        current_user=session["usuario"]
    )
