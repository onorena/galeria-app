# decision_aprendida.py — una regla aprendida de datos (árbol de decisión, scikit-learn)
import numpy as np


def ejemplos(visitantes, filas=10000, semilla=7):
    # Situaciones de la galería y lo que hizo un visitante que se equivoca el 10 % de las
    # veces.
    rng = np.random.default_rng(semilla)
    n = rng.choice(list(visitantes), filas)                  # tamaño de la galería en 
    # cada ejemplo
    mi = rng.integers(1, n)                                  # gente en mi sala; en la 
    # otra hay n - mi
    acierta = rng.random(filas) >= 0.10                      # 9 de cada 10 veces sigue 
    # la regla
    se_movio = np.where(acierta, n - mi < mi, n - mi >= mi)  # regla: pasarse si la otra 
    # tiene menos
    X = np.column_stack([mi, n - mi, rng.integers(1, 11, filas)])   # entradas: mi, otra, 
    # energía
    return X, se_movio.astype(int)


from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def entrenar(visitantes, semilla=7):
    # 70 % para aprender, 30 % para probar; la línea base responde siempre lo más frecuente.
    X, y = ejemplos(visitantes, semilla=semilla)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=semilla)
    arbol = DecisionTreeClassifier(max_depth=6, random_state=semilla).fit(Xtr, ytr)
    base = DummyClassifier(strategy='most_frequent').fit(Xtr, ytr)
    return arbol, round(arbol.score(Xte, yte), 3), round(base.score(Xte, yte), 3)


from functools import lru_cache

ARBOL, ACC_PRUEBA, ACC_BASE = entrenar(range(6, 61, 2))   # los mismos tamaños que 
# permite la app


@lru_cache(maxsize=None)        # recuerda cada respuesta: la app no le pregunta dos 
# veces lo mismo
def regla_aprendida(mi, otra, energia):
    # El árbol decide si el visitante se pasa de sala (mismas entradas que su regla).
    return bool(ARBOL.predict([[mi, otra, energia]])[0])
