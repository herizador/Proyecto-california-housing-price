import os
import joblib
import requests

def download_model(url: str = MODEL_URL, path: str = MODEL_PATH):
    """Descarga el modelo desde la URL raw de GitHub y lo guarda en disco en modo binario."""

    response = requests.get(url, timeout=DOWNLOAD_TIMEOUT)
    response.raise_for_status() # Lanza una excepción si ocurre un error HTTP (ej. 404 o 500)

    with open(path, "wb") as f:
        f.write(response.content)

    print(f"Modelo descargado correctamente desde Github y gurdado en {path}")


def load_model(path: str = MODEL_PATH):
    """Carga el modelo. Si no existe en local, lo descarga antes de GitHub."""
    if not os.path.exists(path):
        print(f"{path} no encontrado en local, descargando...")
        download_model()
    return joblib.load(path)