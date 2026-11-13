# 1. URL pública de tu API de FastAPI en Render
API_URL = "https://proyecto-california-housing-price.onrender.com"

# 2. Petición POST con datos en formato JSON al endpoint /predict
endpoint = f"{API_URL.rstrip('/')}/predict"
response = requests.post(endpoint, json=payload, timeout=90)