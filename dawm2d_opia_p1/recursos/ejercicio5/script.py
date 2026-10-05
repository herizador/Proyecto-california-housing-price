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
