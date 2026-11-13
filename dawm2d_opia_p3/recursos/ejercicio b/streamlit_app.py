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