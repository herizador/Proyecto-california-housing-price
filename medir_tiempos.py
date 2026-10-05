"""Medición del tiempo de respuesta del servicio desplegado.

Solo tienes que poner la URL de tu servicio en BASE_URL y ejecutar el script.
Autores: <nombre1>, <nombre2>

Nota: en el plan gratuito de Render el servicio se "duerme" tras un rato sin
tráfico, así que la primera petición puede tardar mucho más (arranque en frío).
Anótalo en la memoria.
"""
import sys
import time
import requests

# TODO: URL pública de tu servicio en Render (sin barra final)
BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "https://<tu-servicio>.onrender.com"
TIMEOUT = 60  # segundos

SAMPLE = {
    "MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98, "AveBedrms": 1.02,
    "Population": 322.0, "AveOccup": 2.56, "Latitude": 37.88, "Longitude": -122.23,
}

# (método, ruta, cuerpo JSON). Puedes añadir más peticiones.
REQUESTS = [
    ("GET", "/", None),
    ("GET", "/", None),
    ("POST", "/predict", SAMPLE),
    ("POST", "/predict", {**SAMPLE, "MedInc": 3.0}),
    ("POST", "/predict", {**SAMPLE, "Latitude": 34.05, "Longitude": -118.24}),
    ("POST", "/predict", {"MedInc": 1.0}),  # cuerpo inválido: error 422
]


def measure(method: str, path: str, body: dict | None) -> tuple[int, float]:
    """Hace una petición y devuelve (código HTTP, tiempo en milisegundos)."""
    start = time.perf_counter()
    response = requests.request(method, BASE_URL + path, json=body, timeout=TIMEOUT)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return response.status_code, elapsed_ms


def main():
    print("| # | Petición | Código | Tiempo (ms) |")
    print("|---|----------|--------|-------------|")
    for i, (method, path, body) in enumerate(REQUESTS, start=1):
        status, ms = measure(method, path, body)
        print(f"| {i} | {method} {path} | {status} | {ms:.0f} |")


if __name__ == "__main__":
    main()
