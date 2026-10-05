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