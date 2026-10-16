import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# carga las variables de entorno del .env
load_dotenv()

# cadena de conexion a PostgreSQL
# ejemplo: postgresql://usuario:contraseña@localhost:5432/ott_db
DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    """Abre y devuelve una conexión nueva a PostgreSQL."""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
