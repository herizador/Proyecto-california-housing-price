# Configuracion de la pagina.
from turtle import st

st.set_page_config(page_title="Precio de casas en California")

# Titulo y autores.
AUTORES = "Achraf y Ismael"
st.title("Precio de casas en California")
st.caption(f"{AUTORES} - P3")

# Descripcion de la aplicacion.
st.write("Introduce los datos de la zona y estima el precio medio de sus viviendas.")

# Campo para introducir el ingreso medio.
med_inc = st.number_input(
    "Ingreso medio de la zona (decenas de miles de $)",
    min_value=0.0,
    max_value=15.0,
    value=3.5,
    step=0.1,
)

# Campo para introducir el numero medio de habitaciones.
ave_rooms = st.number_input(
    "Numero medio de habitaciones por vivienda",
    min_value=1.0,
    max_value=15.0,
    value=5.2,
    step=0.1,
)