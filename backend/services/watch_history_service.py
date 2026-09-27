from config.db_config import get_connection
import json
from pathlib import Path


# archivo local de respaldo por si la bd falla (para desarrollo/pruebas)
LOCAL_DB_PATH = Path("database") / "watch_history_local.json"


# lee el json local del historial
def _load_local_history():
    try:
        if not LOCAL_DB_PATH.exists():
            return []
        with LOCAL_DB_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


# guarda el json local del historial
def _save_local_history(data):
    try:
        LOCAL_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOCAL_DB_PATH.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


# guarda en que minuto/segundo se quedo el usuario viendo la pelicula
def guardar_historial(usuario_id, pelicula_id, minuto):

    try:
        conn = get_connection()
        cur = conn.cursor()

        # usa UPSERT para insertar o actualizar en una sola operacion
        cur.execute("""
            INSERT INTO watch_history (usuario_id, pelicula_id, minuto)
            VALUES (%s, %s, %s)
            ON CONFLICT (usuario_id, pelicula_id)
            DO UPDATE SET minuto = EXCLUDED.minuto
        """, (usuario_id, pelicula_id, minuto))

        conn.commit()
        cur.close()
        conn.close()

        return True

    except Exception as e:
        # si la bd fallo, guardamos en el json local para no perder el progreso
        try:
            data = _load_local_history()
            # buscamos si ya habia un registro
            found = False
            for item in data:
                if item.get("usuario_id") == usuario_id and item.get("pelicula_id") == pelicula_id:
                    item["minuto"] = minuto
                    found = True
                    break
            if not found:
                data.append({"usuario_id": usuario_id, "pelicula_id": pelicula_id, "minuto": minuto})
            _save_local_history(data)
            return True
        except Exception:
            print(e)
            return False


# trae el minuto en el que se quedo el usuario en esa pelicula
def obtener_historial(usuario_id, pelicula_id):

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT minuto FROM watch_history WHERE usuario_id = %s AND pelicula_id = %s",
            (usuario_id, pelicula_id)
        )
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return row["minuto"]

        return 0

    except Exception:
        # si la bd fallo, revisamos el respaldo local
        try:
            data = _load_local_history()
            for item in data:
                if item.get("usuario_id") == usuario_id and item.get("pelicula_id") == pelicula_id:
                    return int(item.get("minuto", 0))
            return 0
        except Exception:
            return 0
