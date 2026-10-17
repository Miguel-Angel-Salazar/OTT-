import sys
import unittest
from pathlib import Path

# agregar la carpeta backend al path para poder importar modulos
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

import bcrypt
from models.movie import Movie
from app import app


class TestMovieModel(unittest.TestCase):
    """Pruebas unitarias para la creacion y normalizacion del modelo Movie."""

    def test_from_dict_instantiation(self):
        # verifica que se mapeen correctamente todos los atributos desde un diccionario
        data = {
            "id": 1,
            "titulo": "Monos",
            "descripcion": "Pelicula colombiana",
            "categoria": "Drama, Cine Colombiano",
            "region": "LATAM",
            "imagen_url": "images/posters/monos.jpg",
            "video_url": "/static/videos/monos.mp4",
            "hero_url": None,
            "tipo": "Película"
        }
        movie = Movie.from_dict(data)

        self.assertEqual(movie.id, 1)
        self.assertEqual(movie.titulo, "Monos")
        self.assertEqual(movie.categoria, "Drama, Cine Colombiano")
        self.assertEqual(movie.region, "LATAM")
        # debe normalizar la ruta relativa agregando /static/images/
        self.assertTrue(movie.imagen_url.startswith("/static/images/"))
        # si hero_url es None, debe tomar la de imagen_url
        self.assertEqual(movie.hero_url, movie.imagen_url)

    def test_normalize_legacy_picture_paths(self):
        # los registros antiguos con 'picture' o 'pictures' deben mapearse a 'images'
        data = {
            "id": 2,
            "titulo": "Test Legacy",
            "imagen_url": "/static/pictures/poster.jpg"
        }
        movie = Movie.from_dict(data)
        self.assertIn("/static/images/poster.jpg", movie.imagen_url)


class TestAuthSecurity(unittest.TestCase):
    """Pruebas unitarias para el algoritmo de hash y verificacion con bcrypt."""

    def test_password_hashing_and_verification(self):
        password = "mi_clave_secreta_123"
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

        # la clave correcta debe validar en true
        is_valid = bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
        self.assertTrue(is_valid)

        # una clave diferente debe fallar
        is_invalid = bcrypt.checkpw("otra_clave".encode("utf-8"), hashed.encode("utf-8"))
        self.assertFalse(is_invalid)


class TestCatalogLogic(unittest.TestCase):
    """Pruebas unitarias para la logica de filtrado por region y categorias."""

    def setUp(self):
        self.sample_movies = [
            Movie(1, "Monos", "...", "Drama, Cine Colombiano", "LATAM", "/img1.jpg", "/vid1.mp4"),
            Movie(2, "Dark", "...", "Ciencia Ficcion", "EUROPA", "/img2.jpg", "/vid2.mp4"),
            Movie(3, "Interestelar", "...", "Ciencia Ficcion", "USA", "/img3.jpg", "/vid3.mp4"),
            Movie(4, "Contenido Mundial", "...", "Documental", "GLOBAL", "/img4.jpg", "/vid4.mp4"),
        ]

    def test_filter_by_user_region(self):
        user_region = "LATAM"
        filtradas = [
            m for m in self.sample_movies
            if m.region and (m.region.strip().lower() == user_region.lower() or m.region.strip().upper() == "GLOBAL")
        ]
        titulos = [m.titulo for m in filtradas]
        self.assertIn("Monos", titulos)
        self.assertIn("Contenido Mundial", titulos)
        self.assertNotIn("Dark", titulos)

    def test_filter_colombian_cinema_case_insensitive(self):
        colombianas = [
            m for m in self.sample_movies
            if "colombian" in (m.categoria or "").lower()
        ]
        self.assertEqual(len(colombianas), 1)
        self.assertEqual(colombianas[0].titulo, "Monos")


class TestFlaskEndpoints(unittest.TestCase):
    """Pruebas de integracion HTTP sobre los endpoints clave del backend."""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_root_redirects_to_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/auth/login", response.headers["Location"])

    def test_login_page_renders_form(self):
        response = self.client.get("/auth/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"email", response.data.lower())
        self.assertIn(b"password", response.data.lower())

    def test_register_page_renders_form(self):
        response = self.client.get("/auth/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"nombre", response.data.lower())

    def test_swagger_docs_accessible(self):
        # verificar que la documentacion OpenAPI/Swagger cargue
        response = self.client.get("/apidocs/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"swagger", response.data.lower())

    def test_api_movies_returns_json(self):
        response = self.client.get("/api/movies")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        json_data = response.get_json()
        self.assertIn("total", json_data)
        self.assertIn("peliculas", json_data)


if __name__ == "__main__":
    unittest.main()
