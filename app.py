"""Plantilla: servicio web para el modelo de precios de casas en California.

Solo tienes que completar las partes marcadas con TODO.
El resto del código ya está hecho.
Autores: <nombre1>, <nombre2>

Ejecución en local (con modelo_california.pkl generado en el ejercicio 1):
    uvicorn app:app --reload
Comando de arranque en Render (Start Command):
    uvicorn app:app --host 0.0.0.0 --port $PORT
"""
import os
from contextlib import asynccontextmanager

import joblib
import pandas as pd
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MODEL_PATH = "modelo_california.pkl"
# TODO: URL "raw" del modelo en TU repositorio de GitHub. Formato:
# https://raw.githubusercontent.com/<usuario>/<repositorio>/main/modelo_california.pkl
MODEL_URL = "https://raw.githubusercontent.com/<usuario>/<repositorio>/main/modelo_california.pkl"
DOWNLOAD_TIMEOUT = 30  # segundos

# El modelo se carga al arrancar y se guarda aquí.
state = {"model": None}


class HouseFeatures(BaseModel):
    """Variables de entrada del modelo (una zona censal)."""
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


def download_model(url: str = MODEL_URL, path: str = MODEL_PATH):
    """Descarga el modelo desde `url` y lo guarda en `path`.

    Pistas: usa requests.get(url, timeout=DOWNLOAD_TIMEOUT), comprueba el
    resultado con response.raise_for_status() y escribe response.content en
    el fichero abriéndolo en modo binario ("wb").
    """
    # TODO: implementa la descarga
    raise NotImplementedError("Completa download_model()")


def load_model(path: str = MODEL_PATH):
    """Carga el modelo. Si no existe en local, lo descarga antes de GitHub."""
    if not os.path.exists(path):
        print(f"{path} no encontrado en local, descargando...")
        download_model()
    return joblib.load(path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Se ejecuta una vez al arrancar el servicio."""
    state["model"] = load_model()
    yield


app = FastAPI(title="Precio de casas en California", lifespan=lifespan)


@app.get("/")
def health():
    """Health-check: confirma que el servicio está funcionando."""
    return {"status": "ok"}


@app.post("/predict")
def predict(features: HouseFeatures):
    """Devuelve el precio medio estimado (en cientos de miles de dólares)."""
    model = state["model"]
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")
    X = pd.DataFrame([features.model_dump()])
    prediction = model.predict(X)[0]
    return {"MedHouseVal": float(prediction)}
