# Despliegue de California Housing Price en Render

## 1. Crear una cuenta en Render

1. Acceder a [Render](https://render.com/).
2. Crear una cuenta o iniciar sesión.
3. Conectar la cuenta de GitHub con Render.

## 2. Conectar el repositorio

1. Abrir el panel de Render.
2. Seleccionar **New > Web Service**.
3. Elegir el repositorio público [Proyecto-california-housing-price](https://github.com/herizador/Proyecto-california-housing-price).
4. Seleccionar la rama que contiene el código de la aplicación.

## 3. Configurar el servicio

Configurar el entorno de ejecución y los comandos según los archivos del proyecto:

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`

## 4. Desplegar la aplicación

1. Pulsar **Create Web Service**.
2. Esperar a que Render instale las dependencias y complete el despliegue.
3. Revisar los registros (**Logs**) si aparece algún error.
4. Comprobar que el servicio queda activo y que la documentación de la API carga correctamente.

## 5. URL de la aplicación

La aplicación desplegada está disponible en:

**[https://proyecto-california-housing-price.onrender.com/docs](https://proyecto-california-housing-price.onrender.com/docs)**

## 6. Actualizar la aplicación

Cuando se envían nuevos cambios a la rama conectada de GitHub, Render puede iniciar un nuevo despliegue automáticamente, según la configuración del servicio.

## 7. Documentación de la API

La API permite estimar el valor medio de una vivienda en California mediante un modelo de Machine Learning.

### Endpoint de predicción

- **Método:** `POST`
- **Ruta:** `/predict`
- **Formato:** JSON
- **URL completa:** `https://proyecto-california-housing-price.onrender.com/predict`

### Ejemplo de petición

Se envían las ocho variables que necesita el modelo:

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

### Ejemplo de respuesta correcta

Código HTTP: `200 OK`

```json
{
  "MedHouseVal": 4.53
}
```

El valor `MedHouseVal` representa cientos de miles de dólares. Por tanto, un resultado de `4.53` equivale a **453.000 $**.

### Respuestas de error

La API puede devolver diferentes códigos HTTP:

| Código | Descripción |
|---|---|
| 422 | Los datos enviados no son válidos o faltan variables obligatorias. |
| 500 | Se ha producido un error interno en el servidor. |

Ejemplo de respuesta de error:

```json
{
  "detail": "Error en los datos enviados"
}
```

La aplicación Streamlit controla los errores de conexión y las respuestas HTTP de error, mostrando mensajes informativos al usuario.

## 8. Repositorio

Código fuente del proyecto: [https://github.com/herizador/Proyecto-california-housing-price](https://github.com/herizador/Proyecto-california-housing-price)