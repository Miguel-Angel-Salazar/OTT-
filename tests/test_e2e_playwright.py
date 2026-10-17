import os
import sys
import time
import socket
import threading
import unittest
from pathlib import Path

# asegurar que la ruta del backend este en el path
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from playwright.sync_api import sync_playwright

BASE_URL = os.getenv("TEST_BASE_URL", "http://127.0.0.1:5000")


def is_server_running(host="127.0.0.1", port=5000):
    """Comprueba si ya hay un servidor escuchando en el puerto."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False


def start_test_server():
    """Inicia el servidor Flask en segundo plano si no esta corriendo."""
    if is_server_running("127.0.0.1", 5000):
        return None

    from app import app
    app.config["TESTING"] = True

    # servidor en hilo demonio para pruebas
    server_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False),
        daemon=True
    )
    server_thread.start()

    # esperar hasta 5 segundos a que levante
    for _ in range(25):
        if is_server_running("127.0.0.1", 5000):
            break
        time.sleep(0.2)

    return server_thread


class TestE2EPlaywright(unittest.TestCase):
    """Pruebas end-to-end con Playwright para validar las funcionalidades
    criticas de la plataforma OTT (Login, Catalogo, Detalle, Busqueda y Swagger).
    """

    @classmethod
    def setUpClass(cls):
        # asegurar que haya un servidor web respondiendo
        start_test_server()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def test_01_login_interface(self):
        # 1. Verifica carga de la interfaz de login y sus campos requeridos
        self.page.goto(f"{BASE_URL}/auth/login")
        self.assertTrue(self.page.is_visible("input[name='email']"), "El campo email debe ser visible")
        self.assertTrue(self.page.is_visible("input[name='password']"), "El campo password debe ser visible")
        self.assertTrue(self.page.is_visible("button[type='submit']"), "El boton de submit debe ser visible")

    def test_02_login_invalid_credentials(self):
        # 2. Verifica que credenciales invalidas muestren mensaje de error
        self.page.goto(f"{BASE_URL}/auth/login")
        self.page.fill("input[name='email']", "no_existe@ott.com")
        self.page.fill("input[name='password']", "clave_incorrecta")
        self.page.click("button[type='submit']")

        self.page.wait_for_load_state("networkidle")
        # debe permanecer en auth y mostrar feedback de error
        self.assertIn("/auth/login", self.page.url)

    def test_03_login_successful_and_home_catalog(self):
        # 3. Flujo de inicio de sesion con usuario demo y redireccion al home
        self.page.goto(f"{BASE_URL}/auth/login")
        self.page.fill("input[name='email']", "demo@ott.com")
        self.page.fill("input[name='password']", "demo123")
        self.page.click("button[type='submit']")

        # debe redirigir al catalogo
        self.page.wait_for_url("**/home/**", timeout=7000)
        self.assertIn("/home", self.page.url)

        # verificar que se renderice contenido del catalogo o hero
        self.page.wait_for_load_state("domcontentloaded")
        content = self.page.content()
        self.assertTrue("hero" in content.lower() or "película" in content.lower())

    def test_04_movie_detail_view(self):
        # 4. Verifica navegacion y renderizado de la pagina de detalle de pelicula
        self.page.goto(f"{BASE_URL}/movie/1")
        self.assertEqual(self.page.title() != "", True)
        # debe existir el contenedor o reproductor
        content = self.page.content()
        self.assertTrue("player" in content.lower() or "video" in content.lower() or "monos" in content.lower())

    def test_05_movie_search(self):
        # 5. Verifica busqueda de pelicula por query
        self.page.goto(f"{BASE_URL}/movie/search?q=Monos")
        self.page.wait_for_load_state("domcontentloaded")
        content = self.page.content()
        self.assertIn("Monos", content)

    def test_06_swagger_ui_loads(self):
        # 6. Verifica que la interfaz Swagger (OpenAPI) sea accesible en el navegador
        self.page.goto(f"{BASE_URL}/apidocs/")
        self.page.wait_for_load_state("domcontentloaded")
        self.assertIn("swagger", self.page.content().lower())


if __name__ == "__main__":
    unittest.main()
