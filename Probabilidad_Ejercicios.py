"""
Simulación Monte Carlo de la demanda diaria de un componente (100 días).
1. Número de días: de 10 a 100.
2. Números pseudoaleatorios entre 0 y 99.
3. Demanda asignada según el intervalo de la tabla.
Fórmula del promedio: x̄ = Σxᵢ / n
"""
import random
import pandas as pd

demanda = [10, 20, 30, 40, 50]
prob = [0.10, 0.20, 0.40, 0.20, 0.10]
assert abs(sum(prob) - 1.0) < 1e-9, "Las probabilidades deben sumar 1.00"

acum_prob, intervalos = [], []
total, inferior = 0.0, 0
for p in prob:
    total += p
    acum_prob.append(round(total, 2))
    superior = round(total * 100) - 1
    intervalos.append((inferior, superior))
    inferior = superior + 1

tabla = pd.DataFrame({
    "Demanda diaria": demanda,
    "Probabilidad": prob,
    "Prob. acumulada": acum_prob,
    "Intervalo aleatorio": [f"{a:02d}-{b:02d}" for a, b in intervalos],
})
print("DISTRIBUCIÓN DE PROBABILIDADES")
print(tabla.to_string(index=False), "\n")

def asignar_demanda(na: int) -> int:
    """Asigna la demanda según el intervalo en que cae el N.A."""
    for d, (a, b) in zip(demanda, intervalos):
        if a <= na <= b:
            return d
    raise ValueError(f"Número aleatorio fuera de rango: {na}")

DIAS = 100
random.seed(2026)  # quítala para obtener resultados distintos en cada corrida

numeros_aleatorios = [random.randint(0, 99) for _ in range(DIAS)]  # 0 a 99

sim = pd.DataFrame({"Día": range(1, DIAS + 1), "N.A.": numeros_aleatorios})
sim["Demanda asignada"] = sim["N.A."].apply(asignar_demanda)
sim["Demanda acumulada"] = sim["Demanda asignada"].cumsum()

pd.set_option("display.max_rows", None)
print(f"SIMULACIÓN DE {DIAS} DÍAS")
print(sim.to_string(index=False), "\n")

suma = sim["Demanda asignada"].sum()
promedio = suma / DIAS
esperada = sum(d * p for d, p in zip(demanda, prob))

frecuencia = sim["Demanda asignada"].value_counts().reindex(demanda, fill_value=0)
comparacion = pd.DataFrame({
    "Demanda": demanda,
    "Frecuencia simulada": frecuencia.values,
    "Frec. relativa simulada": (frecuencia.values / DIAS).round(2),
    "Probabilidad teórica": prob,
})
print("COMPARACIÓN SIMULADO VS TEÓRICO")
print(comparacion.to_string(index=False), "\n")

print(f"Demanda promedio simulada: x̄ = {suma}/{DIAS} = {promedio:.2f} unidades/día")
print(f"Demanda esperada teórica:  E(x) = {esperada:.2f} unidades/día")