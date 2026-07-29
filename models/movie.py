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
        def normalize_static_path(url):
            if not url:
                return url
            if url.startswith('http'):
                return url
            if url.startswith('static/') or url.startswith('/static/'):
                normalized = '/' + url.lstrip('/')
                # Some records may still use older directory names - map them
                # to the current `static/images/` location used in the repo.
                normalized = normalized.replace('/static/pictures/', '/static/images/')
                normalized = normalized.replace('/static/picture/', '/static/images/')
                return normalized
            if SUPABASE_URL:
                return f"{SUPABASE_URL.rstrip('/')}/storage/v1/object/public/movies/{url.lstrip('/')}"
            return url

        imagen = normalize_static_path(data.get("imagen_url"))
        hero = normalize_static_path(data.get("hero_url")) if data.get("hero_url") else imagen

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
