"""
Manejo de archivos: guardado/lectura de historial y configuración (JSON).
Usa try/except para manejo de errores.
"""

import json
import os
from typing import Any, Dict, List

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_history() -> List[Dict[str, Any]]:
    ensure_data_dir()
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # archivo corrupto -> renombrar y devolver lista vacía
        try:
            os.rename(HISTORY_FILE, HISTORY_FILE + ".bak")
        except Exception:
            pass
        return []

def save_history(entry: Dict[str, Any]):
    ensure_data_dir()
    history = load_history()
    history.append(entry)
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Error guardando historial:", e)
