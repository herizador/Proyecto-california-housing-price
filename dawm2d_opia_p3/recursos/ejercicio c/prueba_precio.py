def format_price(med_house_val: float) -> str:
    precio = med_house_val * 100_000
    return f"${precio:,.0f}"


# Valor de ejemplo devuelto por la API.
valor_api = 4.53

# Transformacion del valor a dolares.
precio_formateado = format_price(valor_api)

print("Valor devuelto por la API:", valor_api)
print("Precio formateado:", precio_formateado)