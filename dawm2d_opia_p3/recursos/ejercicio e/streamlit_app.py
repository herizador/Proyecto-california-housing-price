try:
    # Envia los datos a la API.
    response = requests.post(
        api_url + "/predict",
        json=payload,
        timeout=TIMEOUT
    )

except requests.RequestException as exc:
    # Registra el error en la terminal.
    logger.error("Fallo de comunicacion con %s: %s", api_url, exc)

    # Muestra un mensaje al usuario.
    st.error(
        "No se pudo conectar con la API. "
        "Comprueba la URL y que el servidor este funcionando."
    )

else:
    # Comprueba si la respuesta es correcta.
    if response.status_code == 200:
        med_house_val = response.json()["MedHouseVal"]
        st.metric("Precio estimado", format_price(med_house_val))
        st.caption(f"Valor original devuelto por la API: {med_house_val}")

    else:
        # Muestra el codigo HTTP y el detalle del error.
        st.error(
            f"Error de la API (HTTP {response.status_code}): "
            f"{response.text}"
        )