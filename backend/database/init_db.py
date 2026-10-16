"""
Script para inicializar la base de datos PostgreSQL.

Uso:
    python database/init_db.py

Requisitos:
    - PostgreSQL instalado y corriendo
    - Archivo .env con DATABASE_URL configurado

Ejemplo de DATABASE_URL:
    postgresql://usuario:contraseña@localhost:5432/ott_db
"""

import os
import sys
from pathlib import Path

# agrega la raiz del proyecto al path para poder importar config
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import psycopg2
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def create_database():
    """Crea la base de datos si no existe."""
    # extrae el nombre de la bd del URL
    # formato: postgresql://user:pass@host:port/dbname
    db_name = DATABASE_URL.rsplit("/", 1)[-1]
    base_url = DATABASE_URL.rsplit("/", 1)[0] + "/postgres"

    try:
        conn = psycopg2.connect(base_url)
        conn.autocommit = True
        cur = conn.cursor()

        # revisa si la base de datos ya existe
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))

        if not cur.fetchone():
            cur.execute(f'CREATE DATABASE "{db_name}"')
            print(f"  Base de datos '{db_name}' creada.")
        else:
            print(f"  Base de datos '{db_name}' ya existe.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"  No se pudo crear la BD automaticamente: {e}")
        print(f"   Creala manualmente con: CREATE DATABASE {db_name}")


def create_tables():
    """Ejecuta el schema.sql para crear las tablas."""
    schema_path = Path(__file__).parent / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(schema_sql)
    conn.commit()

    cur.close()
    conn.close()

    print("  Tablas creadas correctamente.")


if __name__ == "__main__":

    if not DATABASE_URL:
        print("Error: DATABASE_URL no esta configurada en el archivo .env")
        print("   Ejemplo: DATABASE_URL=postgresql://usuario:password@localhost:5432/ott_db")
        sys.exit(1)

    print("Inicializando base de datos...")
    create_database()
    create_tables()
    print("Base de datos lista!")
