# Importamos las librerias necesarias.
import logging
import time

import requests
import streamlit as st

# 1. URL pública de tu API de FastAPI en Render
API_URL = "https://proyecto-california-housing-price.onrender.com"

# 2. Petición POST con datos en formato JSON al endpoint /predict
endpoint = f"{API_URL.rstrip('/')}/predict"
response = requests.post(endpoint, json=payload, timeout=90)

# Configuramos el sistema de logs para mostrar informacion en la terminal.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("app")

# Nombre de los autores que apareceran en la interfaz.
AUTORES = "Achraf y Ismael"

# Tiempo maximo de espera para recibir una respuesta de la API (90 segundos).
TIMEOUT = 90

# Lista con los nombres de las 8 variables que necesita el modelo.
FEATURE_NAMES = [
    "MedInc", "HouseAge", "AveRooms", "AveBedrms",
    "Population", "AveOccup", "Latitude", "Longitude",
]

# Valores por defecto para las variables que no introduce el usuario.
DEFAULTS = {
    "HouseAge": 29.0,
    "AveBedrms": 1.05,
    "Population": 1166.0,
    "AveOccup": 2.8,
    "Latitude": 34.26,
    "Longitude": -118.49,
}


# Comprueba si faltan variables obligatorias en el diccionario recibido.
def find_missing(payload: dict) -> list[str]:
    # Recorre las 8 variables y devuelve aquellas que no existen
    # en el diccionario o cuyo valor es None.
    return [nombre for nombre in FEATURE_NAMES if payload.get(nombre) is None]


# Convierte el valor devuelto por el modelo a un precio en dolares.
def format_price(med_house_val: float) -> str:
    # Multiplica el resultado por 100.000 porque el modelo
    # devuelve el precio en cientos de miles de dolares.
    precio = med_house_val * 100_000

    # Devuelve el precio con separadores de miles y sin decimales.
    return f"${precio:,.0f}"


# ---------------------------- INTERFAZ ----------------------------

# Configura el titulo de la pagina de Streamlit.
st.set_page_config(page_title="Precio de casas en California")

# Muestra el titulo principal de la aplicacion.
st.title("Precio de casas en California")

# Muestra los autores y el nombre de la practica.
st.caption(f"{AUTORES} - P3")

# Muestra una breve descripcion de la aplicacion.
st.write("Introduce los datos de la zona y estima el precio medio de sus viviendas.")

# -------------------------- BARRA LATERAL --------------------------

# Permite introducir o modificar la URL de la API.
# rstrip elimina la barra final para evitar duplicarla en la peticion.
api_url = st.sidebar.text_input("URL de la API", API_URL).rstrip("/")

# Casilla para simular que falta la variable HouseAge.
simulate_missing = st.sidebar.checkbox("Prueba: omitir HouseAge de la peticion")

# Casilla para saltarse la validacion local y probar el error 422.
skip_validation = st.sidebar.checkbox(
    "Prueba: saltar la validacion local (provoca un 422 de la API)"
)

# ------------------------ DATOS DE ENTRADA ------------------------

# Campo para introducir el ingreso medio de la zona.
med_inc = st.number_input(
    "Ingreso medio de la zona (decenas de miles de $)",
    min_value=0.0, max_value=15.0, value=3.5, step=0.1,
)

# Campo para introducir el numero medio de habitaciones por vivienda.
ave_rooms = st.number_input(
    "Numero medio de habitaciones por vivienda",
    min_value=1.0, max_value=15.0, value=5.2, step=0.1,
)

# ----------------------- ENVIO DE LA PETICION -----------------------

# Ejecuta el codigo cuando el usuario pulsa el boton.
if st.button("Estimar precio"):

    # Crea el diccionario con las variables por defecto y las introducidas.
    payload = {
        **DEFAULTS,
        "MedInc": med_inc,
        "AveRooms": ave_rooms,
    }

    # Elimina HouseAge si esta activada la prueba de datos incompletos.
    if simulate_missing:
        payload.pop("HouseAge", None)

    # -------------------------- VALIDACION --------------------------

    # Comprueba si falta alguna de las 8 variables obligatorias.
    missing = find_missing(payload)

    # Si se activa la prueba, permite enviar los datos incompletos a la API.
    if skip_validation and missing:
        logger.warning("Validacion local saltada (prueba). Faltan: %s", missing)

    # Si faltan variables y no se salta la validacion, muestra un error.
    elif missing:
        logger.warning("Peticion no enviada, faltan: %s", missing)
        st.error(f"Faltan variables obligatorias: {', '.join(missing)}")
        st.stop()

    # Comprueba que se haya configurado correctamente la URL de la API.
    if "<" in api_url:
        st.error("Configura la URL de la API (TODO 0 o barra lateral).")
        st.stop()

    # ---------------------- CONEXION CON LA API ----------------------

    try:
        # Guarda el instante en el que comienza la peticion.
        start = time.perf_counter()

        # Muestra un mensaje mientras se espera la respuesta de la API.
        with st.spinner("Consultando la API (la primera vez puede tardar mas de un minuto)..."):

            # Envia los datos mediante una peticion POST al endpoint /predict.
            # json convierte el diccionario en un cuerpo JSON.
            # timeout establece el tiempo maximo de espera.
            response = requests.post(
                api_url + "/predict",
                json=payload,
                timeout=TIMEOUT
            )

            # Calcula el tiempo que ha tardado la peticion en milisegundos.
            elapsed_ms = (time.perf_counter() - start) * 1000


    # Captura errores de comunicacion, como falta de conexion o timeout.
    except requests.RequestException as exc:

        # Registra el error en la terminal.
        logger.error("Fallo de comunicacion con %s: %s", api_url, exc)

        # Muestra un mensaje de error al usuario.
        st.error("No se pudo conectar con la API. Comprueba la URL y que el servidor este funcionando.")


    # Se ejecuta cuando la peticion se ha realizado correctamente.
    else:

        # Registra el codigo HTTP y el tiempo de respuesta.
        logger.info("POST %s/predict -> HTTP %s en %.0f ms", api_url, response.status_code, elapsed_ms)

        # Comprueba si la API ha devuelto una respuesta correcta (HTTP 200).
        if response.status_code == 200:
            # Obtiene el valor de MedHouseVal de la respuesta JSON.
            med_house_val = response.json()["MedHouseVal"]

            # Transforma el valor recibido a dolares y muestra el resultado.
            st.metric("Precio estimado", format_price(med_house_val))

            # Muestra tambien el valor original devuelto por la API.
            st.caption(f"Valor original devuelto por la API: {med_house_val}")


        else:

            # Muestra el codigo HTTP y el detalle del error devuelto por la API.
            st.error(
                f"Error de la API (HTTP {response.status_code}): "
                f"{response.text}"

            )