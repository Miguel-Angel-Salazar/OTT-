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
        hero_url=None
    ):

        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.categoria = categoria
        self.region = region
        self.imagen_url = imagen_url
        self.video_url = video_url
        self.hero_url = hero_url or imagen_url
        