import sys
import unittest
from pathlib import Path

backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app import app
from services.auth_service import login_user
from services.movie_service import listar_peliculas


class TestFullCommunicationFlow(unittest.TestCase):
    """Flujo completo de prueba para verificar la comunicacion entre componentes:
    Frontend/Cliente -> Backend Flask -> Base de datos PostgreSQL.
    """

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_01_backend_to_database_health(self):
        # 1. Comprueba comunicacion directa backend -> base de datos mediante /api/health
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200, "El backend debe responder 200 en el healthcheck")
        data = response.get_json()
        self.assertEqual(data.get("status"), "ok")
        self.assertEqual(data.get("database"), "connected", "La base de datos debe reportar estado conectado")

    def test_02_database_seeding_movies_accessible(self):
        # 2. Comprueba que las peliculas semilla del init.sql esten cargadas en la BD
        peliculas = listar_peliculas()
        self.assertGreater(len(peliculas), 0, "La base de datos debe contener peliculas semilla")
        primer_titulo = peliculas[0].titulo
        self.assertTrue(len(primer_titulo) > 0)

    def test_03_auth_flow_with_seed_user(self):
        # 3. Comprueba el flujo de autenticacion consultando la tabla users y hash bcrypt
        usuario = login_user("demo@ott.com", "demo123")
        self.assertNotIsInstance(usuario, str, f"El login del usuario demo no debe retornar error: {usuario}")
        self.assertEqual(usuario.email, "demo@ott.com")

    def test_04_session_and_catalog_navigation_flow(self):
        # 4. Flujo simulado de usuario: login con credenciales -> sesion activa -> acceso a catalogo
        # POST login
        res_login = self.client.post("/auth/login", data={
            "email": "demo@ott.com",
            "password": "demo123"
        }, follow_redirects=True)
        self.assertEqual(res_login.status_code, 200)

        # Acceso al home con sesion establecida
        res_home = self.client.get("/home/")
        self.assertEqual(res_home.status_code, 200)
        self.assertIn(b"Cin", res_home.data)  # CINEFILO o Cine

        # Acceso al detalle de una pelicula existente
        res_detail = self.client.get("/movie/1")
        self.assertEqual(res_detail.status_code, 200)

        # Logout del usuario
        res_logout = self.client.get("/auth/logout", follow_redirects=True)
        self.assertEqual(res_logout.status_code, 200)


if __name__ == "__main__":
    unittest.main()
