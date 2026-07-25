import random
import simpy

# Parámetros del sistema
TIEMPO_SIMULACION = 30  # días
TIEMPO_ENTRE_CLIENTES = 1.5  # media de días entre clientes
TIEMPO_ENTRE_PEDIDOS = 3  # días de entrega del proveedor
PUNTO_REORDEN = 20  # libros
CANTIDAD_PEDIDO = 50  # libros
INVENTARIO_INICIAL = 40  # libros


class Libreria:

  def __init__(self, env):
    self.env = env
    self.inventario = INVENTARIO_INICIAL
    self.pedido_en_transito = False
    self.ventas_realizadas = 0
    self.ventas_perdidas = 0

  def proceso_llegada_clientes(self):
    while True:
      # Tiempo aleatorio hasta la llegada del próximo cliente (Distribución Exponencial)
      tiempo_espera = random.expovariate(1.0 / TIEMPO_ENTRE_CLIENTES)
      yield self.env.timeout(tiempo_espera)

      print(
          f"[{self.env.now:.2f} días] Llegó un cliente. Inventario actual:"
          f" {self.inventario}"
      )

      # Venta del libro
      if self.inventario > 0:
        self.inventario -= 1
        self.ventas_realizadas += 1
        print(f"  -> Venta realizada. Nuevo inventario: {self.inventario}")
      else:
        self.ventas_perdidas += 1
        print("  -> ¡Sin Stock! Venta perdida.")

      # Verificación del punto de reorden
      if self.inventario <= PUNTO_REORDEN and not self.pedido_en_transito:
        self.env.process(self.realizar_pedido())

  def realizar_pedido(self):
    self.pedido_en_transito = True
    print(
        f"[{self.env.now:.2f} días] 📦 PUNTO DE REORDEN ALCANZADO. Solicitando"
        f" {CANTIDAD_PEDIDO} libros al proveedor..."
    )

    # Tiempo que tarda el proveedor en entregar
    yield self.env.timeout(TIEMPO_ENTRE_PEDIDOS)

    # Recepción del pedido
    self.inventario += CANTIDAD_PEDIDO
    self.pedido_en_transito = False
    print(
        f"[{self.env.now:.2f} días] ✅ PEDIDO RECIBIDO. Nuevo inventario:"
        f" {self.inventario}"
    )


# Inicializar el entorno de simulación
random.seed(42)  # Semilla para reproducibilidad
env = simpy.Environment()
libreria = Libreria(env)

# Iniciar procesos
env.process(libreria.proceso_llegada_clientes())

# Ejecutar simulación
env.run(until=TIEMPO_SIMULACION)

# Resumen de resultados
print("\n" + "=" * 40)
print("RESUMEN DE LA SIMULACIÓN (30 DÍAS)")
print("=" * 40)
print(f"Inventario Final: {libreria.inventario} libros")
print(f"Ventas Realizadas: {libreria.ventas_realizadas}")
print(f"Ventas Perdidas por Falta de Stock: {libreria.ventas_perdidas}")
import random
import simpy

# --- PARÁMETROS DEL PROBLEMA ---
TIEMPO_SIMULACION = 30  # días de duración
TIEMPO_ENTRE_CLIENTES = 1.5  # media de días entre clientes (dist. exponencial)
TIEMPO_ENTRE_PEDIDOS = 3  # tiempo de entrega del proveedor (días)
PUNTO_REORDEN = 20  # umbral para solicitar pedido (libros)
CANTIDAD_PEDIDO = 50  # tamaño del pedido (libros)
INVENTARIO_INICIAL = 40  # stock inicial (libros)


class Libreria:

  def __init__(self, env):
    self.env = env
    self.inventario = INVENTARIO_INICIAL
    self.pedido_en_transito = False
    self.ventas_exitosas = 0
    self.ventas_perdidas = 0

  def proceso_llegada_clientes(self):
    """Maneja la llegada de clientes y las ventas."""
    while True:
      # Tiempo aleatorio entre clientes
      tiempo_espera = random.expovariate(1.0 / TIEMPO_ENTRE_CLIENTES)
      yield self.env.timeout(tiempo_espera)

      # 1. Observar cómo disminuye el inventario con cada venta
      print(
          f"[{self.env.now:6.2f} días] 🚶 Cliente llega. Inventario actual:"
          f" {self.inventario}"
      )

      if self.inventario > 0:
        self.inventario -= 1
        self.ventas_exitosas += 1
        print(
            f"             🛒 Venta realizada -> Nuevo Inventario:"
            f" {self.inventario}"
        )
      else:
        self.ventas_perdidas += 1
        print("             ❌ ¡SIN STOCK! Venta no realizada.")

      # 2. Si el inventario baja del punto de reorden, se genera automáticamente un pedido
      if self.inventario <= PUNTO_REORDEN and not self.pedido_en_transito:
        self.env.process(self.realizar_pedido())

  def realizar_pedido(self):
    """Proceso de reabastecimiento con el proveedor."""
    self.pedido_en_transito = True
    print(
        f"\n[{self.env.now:6.2f} días] 🚨 REORDEN AUTOMÁTICA: Inventario"
        f" ({self.inventario}) <= {PUNTO_REORDEN}."
    )
    print(
        f"             📦 Se genera un pedido de {CANTIDAD_PEDIDO} unidades al"
        " proveedor.\n"
    )

    # 3. El proveedor entrega el pedido después de un tiempo determinado
    yield self.env.timeout(TIEMPO_ENTRE_PEDIDOS)

    # Reponiendo el inventario
    self.inventario += CANTIDAD_PEDIDO
    self.pedido_en_transito = False
    print(
        f"\n[{self.env.now:6.2f} días] 🚛 PEDIDO RECIBIDO del proveedor."
        f" Reponiendo stock..."
    )
    print(
        f"             ✅ Nuevo Inventario tras reposición:"
        f" {self.inventario}\n"
    )


# --- EJECUCIÓN DE LA SIMULACIÓN ---
random.seed(42)  # Semilla para que los resultados sean reproducibles
env = simpy.Environment()
libreria = Libreria(env)

# Iniciar el proceso de llegada de clientes
env.process(libreria.proceso_llegada_clientes())

# Correr la simulación durante 30 días
#print("=== INICIO DE LA SIMULACIÓN DE LA LIBRERÍA UNIVERSITARIA ===")
#env.run(until=TIEMPO_SIMULACION)

# --- REPORTE DE RESULTADOS ---
print("-" * 55)
#print("              RESUMEN DE RESULTADOS (30 DÍAS)")
print("-" * 55)
#print(f"Inventario Final:                     {libreria.inventario} libros")
#print(f"Ventas Exitosas:                      {libreria.ventas_exitosas}")
print(f"Ventas Perdidas (Falta de Stock):     {libreria.ventas_perdidas}")
print("-" * 55)
