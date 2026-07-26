import simpy
import random

# ===============================
# Parámetros del problema
# ===============================

TIEMPO_SIMULACION = 30          # días
TIEMPO_PRODUCCION_LOTE = 0.5    # días
TIEMPO_REPARACION = 0.2         # días

PROB_FALLA = 0.15
PROB_RECHAZO_CALIDAD = 0.10

PRODUCCION_MINIMA = 500

# Cada lote produce 20 unidades
UNIDADES_POR_LOTE = 20

# Variables
lotes_aprobados = 0
lotes_rechazados = 0
fallas = 0
unidades_producidas = 0


def planta(env):

    global lotes_aprobados
    global lotes_rechazados
    global fallas
    global unidades_producidas

    numero_lote = 1

    while True:

        # Producción del lote
        yield env.timeout(TIEMPO_PRODUCCION_LOTE)

        print(f"\nDía {env.now:.1f}")
        print(f"Lote {numero_lote} producido")

        # ¿Hay falla?
        if random.random() < PROB_FALLA:

            fallas += 1

            print(">>> FALLA DE MÁQUINA")
            print(f"Reparando durante {TIEMPO_REPARACION} días...")

            yield env.timeout(TIEMPO_REPARACION)

            print("Máquina reparada.")

        # Control de calidad
        if random.random() < PROB_RECHAZO_CALIDAD:

            lotes_rechazados += 1

            print("Resultado: Lote RECHAZADO")

        else:

            lotes_aprobados += 1
            unidades_producidas += UNIDADES_POR_LOTE

            print("Resultado: Lote APROBADO")

        numero_lote += 1


# ===============================
# Simulación
# ===============================

random.seed(15)

env = simpy.Environment()

env.process(planta(env))

env.run(until=TIEMPO_SIMULACION)

print("\n===========================")
print("RESULTADOS")
print("===========================")

print(f"Lotes aprobados : {lotes_aprobados}")
print(f"Lotes rechazados: {lotes_rechazados}")
print(f"Fallas          : {fallas}")
print(f"Unidades producidas: {unidades_producidas}")

if unidades_producidas >= PRODUCCION_MINIMA:
    print("Se alcanzó la producción mínima.")
else:
    print("NO se alcanzó la producción mínima.")