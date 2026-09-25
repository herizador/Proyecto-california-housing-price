import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing

california = fetch_california_housing(as_frame=True)
df = california.frame

print("Valores nulos por columna:\n", df.isnull().sum())

plt.hist(df['MedHouseVal'], bins=50, edgecolor='black', color='skyblue')
plt.title('Distribución de MedHouseVal [Autor: Achraf y Mateo P1]')
plt.xlabel('Precio (en $100,000s)')
plt.ylabel('Frecuencia')
plt.savefig('recursos/histograma_TuNombre_P1.png')
plt.show()