"""API mínima para probar la práctica 3 en local.

Es la versión básica de la práctica 2: sin descarga del modelo ni despliegue.
Necesita modelo_california.pkl en la misma carpeta que este fichero.

Ejecución:
    pip install -r requirements.txt
    uvicorn app:app --reload
La API queda en http://localhost:8000 (documentación interactiva en /docs).
"""
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

model = joblib.load("modelo_california.pkl")

app = FastAPI(title="Precio de casas en California")


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


@app.get("/")
def health():
    """Health-check: confirma que el servicio está funcionando."""
    return {"status": "ok"}


@app.post("/predict")
def predict(features: HouseFeatures):
    """Devuelve el precio medio estimado (en cientos de miles de dólares)."""
    X = pd.DataFrame([features.model_dump()])
    return {"MedHouseVal": float(model.predict(X)[0])}
