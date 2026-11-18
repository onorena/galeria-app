# galeria_modelo.py — la galería de dos salas como modelo de Mesa
from mesa import Agent, Model


class Visitante(Agent):
    # Un visitante: está en una sala (0 = Entrada, 1 = Fondo) y tiene energía.
    def __init__(self, model, sala):
        super().__init__(model)
        self.sala = sala
        self.energia = 10

    def step(self):
        mi = self.model.gente_en(self.sala)      # gente en mi sala (me incluye)
        otra = self.model.n - mi                 # gente en la otra sala
        if self.energia > 0 and self.model.regla(mi, otra, self.energia):
            self.sala = 1 - self.sala            # me paso de sala
            self.energia -= 1                    # moverse cuesta 1


class Galeria(Model):
    # El mundo: n visitantes, una regla de decisión y una semilla.
    def __init__(self, regla, n=24, semilla=1):
        super().__init__(rng=semilla)            # la semilla fija todo el azar
        self.n = n
        self.regla = regla
        en_entrada = int(self.rng.integers(n // 4, 3 * n // 4 + 1))
        for i in range(n):
            Visitante(self, 0 if i < en_entrada else 1)
        self.historia = [self.desbalance()]      # desbalance en cada paso

    def gente_en(self, sala):
        return sum(1 for a in self.agents if a.sala == sala)

    def desbalance(self):
        return abs(self.gente_en(0) - self.gente_en(1))   # 0 = reparto perfecto

    def step(self):
        self.agents.shuffle_do("step")           # orden al azar, fijado por la semilla
        self.historia.append(self.desbalance())


def quedarse(mi, otra, energia):
    return False                                 # línea base: nadie se mueve


def seguir_multitud(mi, otra, energia):
    return otra > mi                             # la regla de la galería (semana 8)


def correr(regla, semilla, n=24, pasos=30):
    # Corre una simulación completa y devuelve la historia del desbalance.
    modelo = Galeria(regla, n=n, semilla=semilla)
    for _ in range(pasos):
        modelo.step()
    return modelo.historia


def promedio_final(regla, semillas, n=24):
    # Desbalance final promedio sobre varias semillas: la métrica honesta.
    finales = [correr(regla, s, n)[-1] for s in semillas]
    return round(sum(finales) / len(finales), 2)
