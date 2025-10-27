"""
Constantes físicas y de configuración para la simulación del cohete.

Este módulo contiene todas las constantes necesarias para la simulación,
incluyendo constantes físicas universales, parámetros de la Tierra,
y configuración de la simulación.
"""

# =========================
# CONSTANTES FÍSICAS
# =========================
G = 6.67430e-11          # Constante de gravitación universal (m^3/kg/s^2)
M_EARTH = 5.972e24       # Masa de la Tierra (kg)
MU = G * M_EARTH         # Parámetro gravitacional estándar de la Tierra (m^3/s^2)
R_E = 6.371e6            # Radio de la Tierra (m)
G0 = 9.81                # Gravedad en la superficie terrestre (m/s^2)

# =========================
# PARÁMETROS DEL COHETE
# =========================
MASA_COHETE = 20_000     # Masa del cohete sin combustible (kg) - fijada por consigna
# AJUSTE: 548,000 kg según ejemplo de referencia (profesor)
MASA_FUEL = 548_000      # Masa del combustible (kg) - según ejemplo de referencia
DIAMETRO_COHETE = 4.0    # Diámetro del cohete (m)
ISP = 300.0              # Impulso específico (s) - constante según consigna
CD = 0.47                # Coeficiente de arrastre de una esfera (adimensional) - consigna

# =========================
# CONDICIONES INICIALES
# =========================
R_0 = R_E + 100          # Posición radial inicial (m) - 100m sobre la superficie
Q_0 = 0.0                # Velocidad radial inicial (m/s)
Q_DOT_0 = 0.0            # Aceleración radial inicial (m/s^2)
THETA_0 = 0.0            # Posición angular inicial (rad)
GAMMA_0 = 0.0            # Velocidad angular inicial (rad/s)
GAMMA_DOT_0 = 0.0        # Aceleración angular inicial (rad/s^2)
BETA_0 = 0.0             # Ángulo de inclinación del empuje inicial (rad)
M_DOT_0 = 7500.0         # Tasa de consumo de masa inicial (kg/s)

# =========================
# PARÁMETROS DE GUIADO (Beta en función de altura)
# =========================
# Alturas de transición para el ángulo de empuje
# VALORES MEJORADOS para gravity turn más eficiente:
# - H_0 más bajo: iniciar gravity turn antes (menos atmósfera densa)
# - H_1 más bajo: alcanzar ángulos medios antes (construir velocidad horiz.)
# - H_2 más bajo: empuje horizontal completo antes (fase de circularización)
H_0 = 7_000              # Primera transición (antes: 7,000 m)
H_1 = 25_000             # Segunda transición (antes: 55,000 m)
H_2 = 80_000             # Tercera transición (antes: 140,000 m)

# =========================
# CONFIGURACIÓN DE SIMULACIÓN
# =========================
DT = 0.1               # Paso de tiempo (s)
T_MAX = 20000         # Tiempo máximo de simulación (s)
USAR_BACKWARD = True    # True: Backward Euler, False: Forward Euler
LOG_CADA = 100_000      # Frecuencia de logging (0 para silenciar)

# =========================
# OPCIONES DE CONTROL
# =========================
# Si es True, beta depende de la altura; si es False, beta depende del tiempo
BETA_ALTURA = False

# =========================
# CONSTANTES AUXILIARES
# =========================
ALTURA_LEO = 2e5         # Altura típica de órbita baja (m) - referencia
