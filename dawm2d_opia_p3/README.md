# Aplicación Streamlit para el precio de casas en California

Esta aplicación permite estimar el precio medio de las viviendas en California mediante un modelo de Machine Learning.
La interfaz está desarrollada con Streamlit y permite introducir el ingreso medio y el número de habitaciones de una zona.
Los datos restantes se completan automáticamente con valores por defecto.
La aplicación envía los datos mediante una petición HTTP POST en formato JSON.
La API, desarrollada con FastAPI, recibe los datos y realiza la predicción.
Finalmente, Streamlit muestra el precio estimado en dólares.

**Autores:** Achraf y Ismael

## Servicios desplegados en Render

| Servicio | Qué es | URL |
|----------|--------|-----|
| API | FastAPI con el modelo (`app.py`) | https://proyecto-california-housing-price.onrender.com |
| Interfaz | Streamlit (`streamlit_app.py`), que llama a la API | TODO: URL de Streamlit en Render |

## Cómo ejecutarla en local

1. Crear un entorno virtual e instalar las dependencias:

```bash
python -m venv .venv
```

Activar el entorno virtual:

```bash
# Windows
.venv\Scripts\activate

# Linux
source .venv/bin/activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

2. Arrancar la API en una primera terminal:

```bash
uvicorn app:app --reload
```

3. Arrancar Streamlit en una segunda terminal:

```bash
streamlit run streamlit_app.py
```

4. Abrir la interfaz en:

```text
http://localhost:8501
```

En la barra lateral, configurar la URL de la API como:

```text
http://127.0.0.1:8000
```

## Despliegue en Render

Se han desplegado dos servicios independientes en Render.

### Servicio API (FastAPI)

**Build Command:**

```bash
pip install -r requirements.txt
```

**Start Command:**

```bash
uvicorn app:app --host 0.0.0.0 --port $PORT
```

### Servicio Interfaz (Streamlit)

**Build Command:**

```bash
pip install -r requirements.txt
```

**Start Command:**

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port $PORT
```

La conexión entre ambos servicios se configura en la barra lateral de Streamlit, en el campo **URL de la API**, introduciendo la dirección pública del servicio FastAPI:

```text
https://proyecto-california-housing-price.onrender.com
```

## Documentación de la API

URL base: <https://proyecto-california-housing-price.onrender.com>

Documentación interactiva: <https://proyecto-california-housing-price.onrender.com/docs>

### `POST /predict`

Este endpoint recibe mediante JSON las ocho variables necesarias para realizar la predicción del precio medio de las viviendas. Devuelve el resultado en el campo `MedHouseVal`, expresado en cientos de miles de dólares.

**Ejemplo de petición**

```json
{
  "MedInc": 3.5,
  "HouseAge": 29.0,
  "AveRooms": 5.2,
  "AveBedrms": 1.05,
  "Population": 1166.0,
  "AveOccup": 2.8,
  "Latitude": 34.26,
  "Longitude": -118.49
}
```

**Ejemplo de respuesta correcta (200)**

```json
{
"MedHouseVal": 1.5126018234536092
}
```

Nota: `0.0` es un valor de ejemplo para mostrar la estructura de la respuesta, no una predicción real. El resultado real se obtiene al realizar la petición a la API.

**Errores**

| Código | Cuándo ocurre | Qué muestra la aplicación |
|--------|---------------|---------------------------|
| 422 | Falta un campo o tiene un tipo incorrecto | Muestra el código HTTP y el detalle del error devuelto por la API. |
| Sin respuesta | La API no está disponible o supera los 90 segundos de espera | Muestra un mensaje indicando que no se ha podido conectar con la API. |