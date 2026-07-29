from config.supabase_config import supabase
import json
from pathlib import Path


# archivo local de respaldo por si supabase falla (para desarrollo/pruebas)
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
        # revisa si ya hay un registro de este usuario con esta pelicula
        existe = (
            supabase.table("watch_history")
            .select("id")
            .eq("usuario_id", usuario_id)
            .eq("pelicula_id", pelicula_id)
            .execute()
        )

        if existe.data:
            supabase.table("watch_history").update({"minuto": minuto}).eq(
                "usuario_id", usuario_id
            ).eq("pelicula_id", pelicula_id).execute()
        else:
            supabase.table("watch_history").insert(
                {
                    "usuario_id": usuario_id,
                    "pelicula_id": pelicula_id,
                    "minuto": minuto,
                }
            ).execute()

        return True

    except Exception as e:
        # si supabase fallo, guardamos en el json local para no perder el progreso
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
        respuesta = (
            supabase.table("watch_history")
            .select("minuto")
            .eq("usuario_id", usuario_id)
            .eq("pelicula_id", pelicula_id)
            .single()
            .execute()
        )

        if respuesta.data:
            return respuesta.data["minuto"]

        return 0

    except Exception:
        # si supabase fallo, revisamos el respaldo local
        try:
            data = _load_local_history()
            for item in data:
                if item.get("usuario_id") == usuario_id and item.get("pelicula_id") == pelicula_id:
                    return int(item.get("minuto", 0))
            return 0
        except Exception:
            return 0
