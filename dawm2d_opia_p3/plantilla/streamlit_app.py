"""Plantilla: aplicación Streamlit conectada a tu servicio de IA.

Completa SOLO las partes marcadas con TODO (del 0 al 6; el 5 tiene subapartados
a y b). El resto ya está hecho.
Este es el único fichero de código que tienes que completar (además del README).
Autores: <nombre1>, <nombre2>

Qué hace la app: el usuario introduce 2 variables (ingreso medio y número de
habitaciones); la app completa el resto con valores por defecto, comprueba que
están las 8 variables, llama a la API (POST /predict), transforma la respuesta
a dólares y la muestra.

Dónde está cada apartado:
    a) Conexión ............. TODO 0: URL de la API; TODO 1: la petición POST
    b) Datos de entrada ..... TODO 2: find_missing()
    c) Datos de salida ...... TODO 3: format_price(); TODO 4: mostrar el precio
    d) Interfaz ............. TODO 6: campo de número de habitaciones
    e) Control de errores ... TODO 5a: fallo de comunicación; TODO 5b: respuesta de error
       (la documentación de la API va en el README)

Ejecución en local (con la API en marcha):
    pip install -r requirements.txt
    streamlit run streamlit_app.py
Los mensajes de log salen en la terminal desde la que lanzas Streamlit.
La URL de la API se puede cambiar en la barra lateral. Por defecto (API_URL)
es http://localhost:8000; para el despliegue, API_URL debe ser la URL pública
de tu API en Render (ver TODO 0): es la que usará la app desplegada.

Despliegue en Render (segundo Web Service, además del de la API):
    Build Command:  pip install -r requirements.txt
    Start Command:  streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true

Capturas (memoria): deben incluir el nombre del autor y la palabra P3
(ej: Juan Perez P3). Rellena AUTORES más abajo para que salga en la interfaz.

Pruebas desde la barra lateral (para la memoria, apartados b y e):
    - Marcar "omitir HouseAge"                         -> validación local: no se envía nada.
    - Marcar "omitir HouseAge" + "saltar la validación" -> la API responde 422.
    - Cambiar la URL de la API por una incorrecta       -> fallo de comunicación.

Contrato de la API:
    POST /predict, cuerpo JSON con las 8 variables:
        MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup,
        Latitude, Longitude
    200  {"MedHouseVal": 4.53}  -> precio en CIENTOS DE MILES de dólares
    422  {"detail": [...]}      -> falta un campo o tiene un tipo incorrecto
    500  texto "Internal Server Error" (¡no es JSON!)
"""
import logging
import time

import requests
import streamlit as st

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("app")

# Nombres que aparecerán en la interfaz (necesario para las capturas).
AUTORES = "<nombre1>, <nombre2>"

# TODO 0 (apartado a): URL pública de tu API en Render (sin barra final).
# Por defecto la app usa la API en local. Antes de desplegar en Render,
# sustituye <tu-servicio-api> por el nombre de tu servicio, comenta la línea
# de localhost y descomenta la de Render: es la que usará la app desplegada.
API_URL = "http://localhost:8000"
# API_URL = "https://<tu-servicio-api>.onrender.com"
# Segundos de espera. Con dos servicios dormidos en Render (la API y esta app),
# el arranque en frío puede tardar más de un minuto.
TIMEOUT = 90

# Las 8 variables que necesita el modelo.
FEATURE_NAMES = [
    "MedInc", "HouseAge", "AveRooms", "AveBedrms",
    "Population", "AveOccup", "Latitude", "Longitude",
]

# Variables que NO se piden al usuario (valores aproximados de la mediana del
# dataset de California Housing).
DEFAULTS = {
    "HouseAge": 29.0,
    "AveBedrms": 1.05,
    "Population": 1166.0,
    "AveOccup": 2.8,
    "Latitude": 34.26,
    "Longitude": -118.49,
}


def find_missing(payload: dict) -> list[str]:
    """Devuelve las variables de FEATURE_NAMES que faltan en `payload`.

    TODO 2 (apartado b): una variable falta si su clave no está en el
    diccionario o si vale None.
    Pista: recorre FEATURE_NAMES y comprueba `payload.get(nombre) is None`.
    Ojo: no uses `if not valor`, porque 0.0 es un valor válido.
    """
    raise NotImplementedError("Completa el TODO 2: find_missing()")


def format_price(med_house_val: float) -> str:
    """Convierte la salida del modelo a un texto legible en dólares.

    TODO 3 (apartado c): la variable objetivo está en cientos de miles de
    dólares, así que 4.53 debe convertirse en "$453,000".
    Pistas: multiplica por 100_000; para el texto usa un f-string con el
    formato de miles de Python, f"${precio:,.0f}".
    """
    raise NotImplementedError("Completa el TODO 3: format_price()")


# ---------------------------------------------------------------- Interfaz --
st.set_page_config(page_title="Precio de casas en California")
st.title("Precio de casas en California")
st.caption(f"{AUTORES} - P3")
st.write("Introduce los datos de la zona y estima el precio medio de sus viviendas.")

# Barra lateral: permite cambiar de servidor y provocar errores de prueba.
api_url = st.sidebar.text_input("URL de la API", API_URL).rstrip("/")
simulate_missing = st.sidebar.checkbox("Prueba: omitir HouseAge de la petición")
skip_validation = st.sidebar.checkbox(
    "Prueba: saltar la validación local (provoca un 422 de la API)"
)

# Variables clave que introduce el usuario.
med_inc = st.number_input(
    "Ingreso medio de la zona (decenas de miles de $)",
    min_value=0.0, max_value=15.0, value=3.5, step=0.1,
)
# Hasta que completes el TODO 6, AveRooms usa un valor por defecto fijo
# (mediana aproximada del dataset), así la petición lleva las 8 variables.
ave_rooms = 5.2
# TODO 6 (apartado d): sustituye el valor fijo de arriba por un campo de entrada
# para el número de habitaciones: asigna a `ave_rooms` un st.number_input,
# copiando el de ingreso medio, con
#   etiqueta "Número medio de habitaciones por vivienda",
#   min_value=1.0, max_value=15.0, value=5.2, step=0.1
# (el payload de abajo ya usa `ave_rooms`; no hay que tocarlo).

if st.button("Estimar precio"):
    payload = {
        **DEFAULTS,
        "MedInc": med_inc,
        "AveRooms": ave_rooms,
    }
    if simulate_missing:  # solo para la prueba de errores
        payload.pop("HouseAge", None)

    # Apartado b: validar los datos ANTES de enviarlos.
    # Con la casilla "saltar la validación" la petición sale incompleta y es
    # la API quien la rechaza (422), para probar el control de errores (5b).
    missing = find_missing(payload)
    if skip_validation and missing:
        logger.warning("Validación local saltada (prueba). Faltan: %s", missing)
    elif missing:
        logger.warning("Petición no enviada, faltan: %s", missing)
        st.error(f"Faltan variables obligatorias: {', '.join(missing)}")
        st.stop()

    if "<" in api_url:  # sigue el valor de ejemplo de Render: falta el TODO 0
        st.error("Configura la URL de la API (TODO 0 o barra lateral).")
        st.stop()

    try:
        start = time.perf_counter()
        with st.spinner("Consultando la API (la primera vez puede tardar más de un minuto)..."):
            # TODO 1 (apartado a): envía `payload` como JSON a la API con una
            # petición POST al endpoint /predict y guarda la respuesta en
            # `response`. Pista: requests.post(api_url + "/predict",
            # json=payload, timeout=TIMEOUT). Borra la línea de abajo.
            raise NotImplementedError("Completa el TODO 1: la petición POST")
        elapsed_ms = (time.perf_counter() - start) * 1000
    except requests.RequestException as exc:
        logger.error("Fallo de comunicación con %s: %s", api_url, exc)
        # TODO 5a (apartado e): sustituye el mensaje por uno claro para el
        # usuario (qué ha pasado y qué puede hacer). Este único except cubre
        # cualquier fallo de comunicación (sin conexión, timeout...).
        st.error("TODO 5a: no se pudo contactar con la API.")
    else:
        logger.info("POST %s/predict -> HTTP %s en %.0f ms", api_url, response.status_code, elapsed_ms)
        if response.status_code == 200:
            med_house_val = response.json()["MedHouseVal"]
            # Valor SIN formatear (cientos de miles de $), para poder probar la
            # app antes de hacer el apartado c.
            st.metric("Valor devuelto por la API (sin formatear)", med_house_val)
            # TODO 4 (apartados c y d): muestra el precio ya formateado.
            # Pista: sustituye la línea st.metric de arriba por
            # st.metric("Precio estimado", format_price(med_house_val))
            # (o st.success). Opcional: deja un st.caption con el valor crudo
            # de la API (entregable del apartado c).
        else:
            # TODO 5b (apartado e): muestra UN solo st.error claro para
            # cualquier código distinto de 200 (422, 500...): indica el código
            # y el detalle con response.text (no llames a response.json():
            # en un 500 el cuerpo NO es JSON). Borra la línea de abajo.
            raise NotImplementedError("Completa el TODO 5b: respuesta de error")
