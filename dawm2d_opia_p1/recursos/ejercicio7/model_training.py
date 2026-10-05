"""Plantilla: predicción del precio de casas en California.

Completa las partes marcadas con TODO. No cambies la estructura general.
Autores: <nombre1>, <nombre2>
"""
import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree

TARGET = "MedHouseVal"
RANDOM_STATE = 42
TEST_SIZE = 0.2
MAX_DEPTH = 5
MODEL_PATH = "modelo_california.pkl"


def check_nulls(df: pd.DataFrame):
    """TODO: muestra por pantalla el número de valores nulos por columna."""
    # df.isnull() genera una tabla de Trues/Falses donde True indica celda vacía.
    # .sum() suma esos Trues por cada columna.
    nulos = df.isnull().sum()
    print("Valores nulos por columna:")
    print(nulos)


def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """TODO: trata los valores nulos del DataFrame (descártalos con
    dropna() o rellénalos con fillna(), según lo que decidas) y
    devuelve el DataFrame resultante."""
    # dropna() elimina todas las filas que contengan al menos un valor nulo
    df_limpio = df.dropna()
    return df_limpio


def plot_decision_tree(X, y, max_depth=None):
    """
    Valida max_depth, entrena un árbol de decisión y guarda su representación gráfica.
    """
    # 1\. Definimos un límite razonable y un valor por defecto seguro
    MAXIMO_PERMITIDO = 5
    VALOR_POR_DEFECTO = 3

    # 2\. Estructura de control (if / elif / else) para validar max_depth
    if max_depth is None or max_depth <= 0:
      print(f"Aviso: 'max_depth' no indicado o inválido. Se usará el valor por defecto ({VALOR_POR_DEFECTO}).")
      profundidad_valida = VALOR_POR_DEFECTO
    elif max_depth > MAXIMO_PERMITIDO:
      print(f"Aviso: 'max_depth' ({max_depth}) supera el límite razonable de {MAXIMO_PERMITIDO}. Se ajusta a {MAXIMO_PERMITIDO}.")
      profundidad_valida = MAXIMO_PERMITIDO
    else:
      profundidad_valida = max_depth


    # 3\. Entrenar el modelo con la profundidad ya validada
    modelo = DecisionTreeRegressor(max_depth=profundidad_valida, random_state=42)
    modelo.fit(X, y)

    # 4\. Dibujar y guardar la imagen del árbol
    plt.figure(figsize=(20, 10))
    plot_tree(
        modelo,
        feature_names=X.columns,
        filled=True,
        fontsize=10
    )

    nombre_archivo = "arbol_decision.png"
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Árbol entrenado con max_depth={profundidad_valida} y guardado en '{nombre_archivo}'.")


def compute_errors(y_true, y_pred, print_errors: bool = True) -> tuple[float, float]:
    """Calcula el MAE y el MSE entre los valores reales y las predicciones.

    Si `print_errors` es True (por defecto), los muestra por pantalla.
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    if print_errors:
        print(f"MAE: {mae:.4f}")
        print(f"MSE: {mse:.4f}")
    return mae, mse


def save_model(model, path: str = MODEL_PATH):
    """Guarda el modelo entrenado en `path` usando joblib.dump()."""
    joblib.dump(model, path)
    print(f"Modelo guardado correctamente en: {path}")

def validate_data():
    """Exploración y validación de los datos."""
    df = fetch_california_housing(as_frame=True).frame
    check_nulls(df)
    df = handle_nulls(df)


def build_model():
    """Carga los datos, entrena el modelo, muestra sus errores y lo devuelve."""
    df = fetch_california_housing(as_frame=True).frame

    X = df.drop(columns=[TARGET])
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    model = DecisionTreeRegressor(max_depth=MAX_DEPTH, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    compute_errors(y_test, y_pred)

    return model


def plot_data():
    """
    Visualización: obtiene los datos y dibuja el árbol con la profundidad validada.
    """
    # 1\. Cargamos el dataset para tener X e y
    housing = fetch_california_housing(as_frame=True)
    X = housing.data
    y = housing.target

    # 2\. Llamamos a plot\_decision\_tree pasándole X, y y la profundidad deseada
    plot_decision_tree(X, y, max_depth=3)


def main():
    model = build_model()
    save_model(model)  # TODO: descomenta cuando hayas completado el stub


if __name__ == "__main__":
    validate_data()  # TODO: descomenta cuando hayas completado los stubs
    #plot_data()  # TODO: descomenta cuando hayas completado plot_decision_tree
    #main()
