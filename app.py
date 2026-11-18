# app.py — galería de dos salas: la app del proyecto final (Solara)
import solara
from matplotlib.figure import Figure
from galeria_modelo import correr, promedio_final, quedarse, seguir_multitud
from mi_regla import regla_mia
from decision_aprendida import regla_aprendida, ACC_PRUEBA, ACC_BASE

semilla = solara.reactive(1)            # valores que el usuario cambia con los controles;
visitantes = solara.reactive(24)        # cuando uno cambia, Solara vuelve a dibujar la página
nombre_regla = solara.reactive('Mi regla')


def grafico(historia, base, n):
    # Desbalance paso a paso: la regla elegida contra la línea base.
    fig = Figure(figsize=(6, 3))
    ax = fig.subplots()
    ax.plot(base, '--', label='línea base: nadie se mueve')
    ax.plot(historia, label=nombre_regla.value)
    ax.set_ylim(0, n)                   # eje desde 0: no exagera diferencias
    ax.set_xlabel('paso')
    ax.set_ylabel('desbalance (personas)')
    ax.legend()
    return fig


@solara.component
def Corrida():
    # Controles + gráfico de UNA corrida (la semilla elegida).
    solara.SliderInt('Semilla', value=semilla, min=1, max=3000)
    solara.SliderInt('Visitantes', value=visitantes, min=6, max=60, step=2)
    solara.Select('Regla', value=nombre_regla, values=list(REGLAS))
    historia = correr(REGLAS[nombre_regla.value], semilla.value, visitantes.value)
    base = correr(quedarse, semilla.value, visitantes.value)
    solara.FigureMatplotlib(grafico(historia, base, visitantes.value))
    solara.Markdown(f'**Esta corrida:** desbalance final {historia[-1]} · línea base {base[-1]}')


def metrica(regla, semilla, n):
    # Desbalance final promedio en las 10 semillas que empiezan en `semilla` (Taller 15).
    return promedio_final(regla, range(semilla, semilla + 10), n)


@solara.component
def Page():
    solara.Markdown(f'## Galería de dos salas\n{PREGUNTA}')       # 1. la pregunta, arriba
    Corrida()                                                      # 2. controles, gráfico, una corrida
    regla = REGLAS[nombre_regla.value]
    promedio = metrica(regla, semilla.value, visitantes.value)
    base = metrica(quedarse, semilla.value, visitantes.value)
    solara.Markdown(f'**Promedio en 10 semillas:** {promedio} · línea base {base}  \n{COMO_LEER}')
    solara.Markdown(f'*Decisión aprendida:* exactitud en prueba {ACC_PRUEBA} · línea base {ACC_BASE}')


# --- Su parte (Taller 16): el menú de reglas y los textos que guían al usuario ---
REGLAS = {'Mi regla': regla_mia, 'Seguir a la multitud': seguir_multitud,
          'Decisión aprendida': regla_aprendida}
PREGUNTA = '¿Cómo se desempeña el modelo con respecto a la regla base y que distribución so obtiene con cada regla?'    # la pregunta que responde la app y para quién (1 o 2 frases)
COMO_LEER = 'Es el resultado de emplear la misma regla varias veces e identificar que distribución resulta más probable; el mejor valor es 0,0'   # qué significa el promedio y cuál es su mejor valor posible
