# Aplicación Streamlit para el precio de casas en California

<!-- TODO: texto de 5-10 líneas: qué hace la aplicación, qué dos servicios la forman (la API FastAPI y la interfaz Streamlit) y cómo se conectan -->

Autores: <nombre1>, <nombre2>

## Servicios desplegados en Render

| Servicio | Qué es | URL |
|----------|--------|-----|
| API | FastAPI con el modelo (`app.py`) | TODO |
| Interfaz | Streamlit (`streamlit_app.py`), que llama a la API | TODO |

## Cómo ejecutarla en local

<!-- TODO: comandos para instalar las dependencias y arrancar la API y la interfaz (en dos terminales), y qué URL de la API usar en la barra lateral -->

## Despliegue en Render

<!-- TODO: para cada servicio, el Build Command y el Start Command que has usado, y dónde cambias la URL de la API en la interfaz -->

## Documentación de la API

URL base: <https://tu-servicio-api.onrender.com>

### `POST /predict`

<!-- TODO: una o dos frases: qué recibe este endpoint y qué devuelve -->

**Ejemplo de petición**

```json
TODO: pega aquí una petición real (JSON con las 8 variables)
```

**Ejemplo de respuesta correcta (200)**

```json
TODO: pega aquí la respuesta real de la API
```

**Errores**

| Código | Cuándo ocurre | Qué muestra la aplicación |
|--------|---------------|---------------------------|
| 422 | Falta un campo o tiene un tipo incorrecto | TODO |
| Sin respuesta | La API no está disponible o tarda demasiado | TODO |
