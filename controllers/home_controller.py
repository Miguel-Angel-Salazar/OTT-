from flask import Blueprint, render_template, session

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
PELICULAS_MOCK = [
    {
        "id": 1,
        "titulo": "Las Sombras del Olvido",
        "descripcion": "En los callejones de una Bogotá convulsa, una pintora halla en los muros de la ciudad los retratos de quienes la historia decidió borrar.",
        "categoria": "Drama · Cine Colombiano",
        "region": "LATAM",
        "imagen_url": "https://images.unsplash.com/photo-1675726205553-4e348f24da2c?w=400&h=600&fit=crop&auto=format",
        "hero_url": "https://images.unsplash.com/photo-1661124280301-ca0e33ceb438?w=1920&h=900&fit=crop&auto=format",
    },
    {
        "id": 2,
        "titulo": "El Último Encuadre",
        "descripcion": "Un fotógrafo de guerra regresa a su ciudad natal con una cámara que ya no puede levantar.",
        "categoria": "Drama · Independiente",
        "region": "LATAM",
        "imagen_url": "https://images.unsplash.com/photo-1453396450673-3fe83d2db2c4?w=400&h=600&fit=crop&auto=format",
        "hero_url": "https://images.unsplash.com/photo-1514900389014-caae55f63513?w=1920&h=900&fit=crop&auto=format",
    },
    {
        "id": 3,
        "titulo": "Tierra Adentro",
        "descripcion": "Dos hermanas emprenden un viaje hacia las montañas de Boyacá en busca de su madre desaparecida.",
        "categoria": "Drama · Cine Colombiano",
        "region": "LATAM",
        "imagen_url": "https://images.unsplash.com/photo-1629278357549-b413116d211c?w=400&h=600&fit=crop&auto=format",
        "hero_url": "https://images.unsplash.com/photo-1661124280301-ca0e33ceb438?w=1920&h=900&fit=crop&auto=format",
    },
    {
        "id": 4,
        "titulo": "La Oscuridad Necesaria",
        "descripcion": "Un detective retirado recibe una llamada que lo regresa a un caso cerrado veinte años atrás.",
        "categoria": "Thriller · Noir",
        "region": "USA",
        "imagen_url": "https://images.unsplash.com/photo-1637059880830-59a90102de77?w=400&h=600&fit=crop&auto=format",
        "hero_url": "https://images.unsplash.com/photo-1514900389014-caae55f63513?w=1920&h=900&fit=crop&auto=format",
    },
    {
        "id": 5,
        "titulo": "Reminiscencias",
        "descripcion": "Una bailarina que pierde la memoria reconstruye su identidad a través de los movimientos que su cuerpo todavía recuerda.",
        "categoria": "Drama · Romance",
        "region": "EUROPA",
        "imagen_url": "https://images.unsplash.com/photo-1759354192456-71975b190c51?w=400&h=600&fit=crop&auto=format",
        "hero_url": "https://images.unsplash.com/photo-1661124280301-ca0e33ceb438?w=1920&h=900&fit=crop&auto=format",
    },
    {
        "id": 6,
        "titulo": "El Silencio Habla",
        "descripcion": "Tres comunidades rurales colombianas filmadas durante cuatro años.",
        "categoria": "Documental · Cine Colombiano",
        "region": "LATAM",
        "imagen_url": "https://images.unsplash.com/photo-1774016591258-f86e81cb1474?w=400&h=600&fit=crop&auto=format",
        "hero_url": "https://images.unsplash.com/photo-1514900389014-caae55f63513?w=1920&h=900&fit=crop&auto=format",
    },
]


@home_bp.route("/")
def inicio():

    destacada = PELICULAS_MOCK[0]
    colombianas = [m for m in PELICULAS_MOCK if "Colombiano" in m["categoria"]]

    return render_template(
        "home.html",
        active_page="home",
        current_user=session.get("usuario"),
        destacada=destacada,
        recomendadas=PELICULAS_MOCK,
        mi_lista=PELICULAS_MOCK[2:5],
        cine_colombiano=colombianas,
    )


@home_bp.route("/onboarding")
def onboarding():

    return render_template("onboarding.html")