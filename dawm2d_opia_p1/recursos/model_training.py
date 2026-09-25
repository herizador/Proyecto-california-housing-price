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
    raise NotImplementedError


def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """TODO: trata los valores nulos del DataFrame (descártalos con
    dropna() o rellénalos con fillna(), según lo que decidas) y
    devuelve el DataFrame resultante."""
    raise NotImplementedError


def plot_decision_tree(model):
    """TODO: dibuja el árbol del `model` ya entrenado con plot_tree()
    y guarda la imagen en un .png."""
    raise NotImplementedError


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
    """TODO: guarda el modelo entrenado en `path` usando joblib.dump()."""
    raise NotImplementedError


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
    """Visualización: dibuja el árbol de decisión del modelo entrenado."""
    model = build_model()
    plot_decision_tree(model)


def main():
    model = build_model()
    # save_model(model)  # TODO: descomenta cuando hayas completado el stub


if __name__ == "__main__":
    # validate_data()  # TODO: descomenta cuando hayas completado los stubs
    # plot_data()  # TODO: descomenta cuando hayas completado plot_decision_tree
    main()
