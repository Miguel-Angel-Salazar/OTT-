from config.supabase_config import SUPABASE_URL


class Movie:

    def __init__(
        self,
        id,
        titulo,
        descripcion,
        categoria,
        region,
        imagen_url,
        video_url,
        hero_url=None,
        tipo=None,
    ):

        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.categoria = categoria
        self.region = region
        self.imagen_url = imagen_url
        self.video_url = video_url
        self.hero_url = hero_url or imagen_url
        self.tipo = tipo

    @classmethod
    def from_dict(cls, data):
        imagen = data.get("imagen_url")
        # normalize imagen_url:
        # - if absolute (http...) keep as-is
        # - if points to local static files (starts with 'static/'), serve from /static/
        # - otherwise assume it's a Supabase storage object path and build public URL
        if imagen:
            if imagen.startswith('http'):
                pass
            elif imagen.startswith('static/') or imagen.startswith('/static/'):
                imagen = '/' + imagen.lstrip('/')
            elif SUPABASE_URL:
                imagen = f"{SUPABASE_URL.rstrip('/')}/storage/v1/object/public/movies/{imagen.lstrip('/')}"

        hero = data.get("hero_url") or imagen

        return cls(
            id=data.get("id"),
            titulo=data.get("titulo"),
            descripcion=data.get("descripcion"),
            categoria=data.get("categoria"),
            region=data.get("region"),
            imagen_url=imagen,
            video_url=data.get("video_url"),
            hero_url=hero,
            tipo=data.get("tipo"),
        )

    def __repr__(self):
        return f"<Movie id={self.id} titulo={self.titulo!r}>"
