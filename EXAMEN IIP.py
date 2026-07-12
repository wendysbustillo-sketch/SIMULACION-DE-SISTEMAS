import random
import simpy

# Configuración / Parámetros
SEMILLA = 42
NUM_AGENTES = 1          # Un agente para notar más fácil las colas
INTERVALO_LLEGADA = 5    # Cada cuántos minutos entra una llamada
TIEMPO_SIMULACION = 25   # Duración de la simulación, tiempo ficticio que transcurre dentro del universo del Call Center.

# Contadores globales (Esto va en un print al final)
clientes_llamaron = 0
clientes_atendidos = 0
tiempos_de_llamadas = []

def cliente_proceso(env, nombre, call_center):
    global clientes_llamaron, clientes_atendidos
    
    # 1. ESTADO: Llama
    clientes_llamaron += 1
    print(f"[{env.now:.2f} min] 📞 {nombre} llama al call center.")
    
    # El cliente solicita un agente
    peticion = call_center.request()
    yield peticion
    
    # 2. ESTADO: Se le atiende
    print(f"[{env.now:.2f} min] 🎧 {nombre}: Está siendo atendido...")
    
    # Duración de la llamada aleatoria (entre 2 y 6 minutos)
    duracion = random.uniform(2, 6)
    tiempos_de_llamadas.append(duracion)
    yield env.timeout(duracion)
    
    # Liberamos al agente de inmediato
    call_center.release(peticion)
    
    # 3. ESTADO: Cliente atendido
    clientes_atendidos += 1
    print(f"[{env.now:.2f} min] ✅ {nombre}: ¡Cliente atendido!")

def generar_llamadas(env, call_center):
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / INTERVALO_LLEGADA))
        i += 1
        env.process(cliente_proceso(env, f"Cliente {i}", call_center))

# --- Ejecución ---
random.seed(SEMILLA)
env = simpy.Environment()
call_center = simpy.Resource(env, capacity=NUM_AGENTES)

env.process(generar_llamadas(env, call_center))

print("--- INICIO DE LA SIMULACIÓN ---")
env.run(until=TIEMPO_SIMULACION)
print("--- FIN DE LA SIMULACIÓN ---\n")

# --- Impresión de Métricas Obligatorias ---
print("================ METRICAS FINALES ================")
if tiempos_de_llamadas:
    promedio = sum(tiempos_de_llamadas) / len(tiempos_de_llamadas)
    print(f"Tiempo de llamadas (Promedio): {promedio:.2f} minutos")
else:
    print("Tiempo en llamadas: 0")

print(f"Cantidad de clientes que llaman: {clientes_llamaron}")
print(f"Cantidad de clientes atendidos: {clientes_atendidos}")
print("==================================================")