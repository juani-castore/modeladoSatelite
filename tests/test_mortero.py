"""
Test: Tiro con mortero (tiro parabólico)

Simula un proyectil lanzado verticalmente con velocidad inicial,
sin empuje, solo bajo la acción de la gravedad y el arrastre.
Debe subir hasta un apogeo y luego caer de vuelta.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cohete import Cohete
from constantes import *
import matplotlib.pyplot as plt
import numpy as np

print("="*70)
print("TEST: TIRO CON MORTERO (Tiro Parabólico)")
print("="*70)

# Crear un "cohete" que es realmente un proyectil
# Sin combustible, solo masa seca, con velocidad inicial
cohete = Cohete(
    r_0=R_E + 100,        # Altura inicial: 100m
    q_0=100.0,            # Velocidad radial inicial: 100 m/s (hacia arriba)
    q_dot_0=0.0,
    theta_0=0.0,
    gamma_0=0.0,          # Sin velocidad angular (tiro vertical)
    gamma_dot_0=0.0,
    masa_cohete=100.0,    # Masa pequeña (proyectil)
    masa_fuel=0.0,        # SIN COMBUSTIBLE
    beta=0.0,
    diametro=0.1,         # Diámetro pequeño (10 cm)
    m_dot=0.0,            # Sin consumo
    isp=ISP,
    h_0=H_0, h_1=H_1, h_2=H_2
)

print(f"\nCondiciones iniciales:")
print(f"  Altura: {(cohete.r - R_E):.1f} m")
print(f"  Velocidad radial: {cohete.q:.2f} m/s")
print(f"  Masa: {cohete.masa:.2f} kg")
print(f"  Diámetro: {cohete.diametro*100:.1f} cm\n")

# Simular hasta que caiga de vuelta
dt = 0.1
t_max = 30.0  # 30 segundos debería ser suficiente
cohete.simular(dt, t_max, usar_backward=True, log_cada=0)

# Encontrar el apogeo
alturas = [(r - R_E) for r in cohete.r_hist]
velocidades_radiales = cohete.q_hist
tiempo = np.arange(len(alturas)) * dt

idx_apogeo = np.argmax(alturas)
altura_maxima = alturas[idx_apogeo]
tiempo_apogeo = tiempo[idx_apogeo]

print(f"Resultados:")
print(f"  Altura máxima (apogeo): {altura_maxima:.2f} m")
print(f"  Tiempo al apogeo: {tiempo_apogeo:.2f} s")
print(f"  Velocidad en apogeo: {velocidades_radiales[idx_apogeo]:.4f} m/s")

# Verificar física básica
# Para tiro vertical: h_max ≈ v₀²/(2g) = 100²/(2*9.81) ≈ 510 m
h_teorica = (100**2) / (2 * 9.81)
print(f"\n  Altura teórica (sin arrastre): {h_teorica:.2f} m")
print(f"  Diferencia: {abs(altura_maxima - h_teorica):.2f} m")

# Graficar
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Altura vs tiempo
ax1.plot(tiempo, alturas, 'b-', linewidth=2)
ax1.axhline(y=0, color='brown', linestyle='--', label='Superficie')
ax1.axvline(x=tiempo_apogeo, color='r', linestyle='--', alpha=0.5, label=f'Apogeo ({tiempo_apogeo:.1f}s)')
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Altura (m)')
ax1.set_title('Tiro con Mortero: Altura vs Tiempo')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Velocidad radial vs tiempo
ax2.plot(tiempo, velocidades_radiales, 'g-', linewidth=2)
ax2.axhline(y=0, color='r', linestyle='--', alpha=0.5, label='Velocidad = 0')
ax2.set_xlabel('Tiempo (s)')
ax2.set_ylabel('Velocidad radial (m/s)')
ax2.set_title('Velocidad Radial vs Tiempo')
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.savefig('test_mortero.png', dpi=150)
print(f"\n✓ Gráfico guardado: test_mortero.png")

# Verificaciones
print(f"\n{'='*70}")
print("VERIFICACIONES:")
if abs(velocidades_radiales[idx_apogeo]) < 1.0:
    print("  ✓ Velocidad en apogeo ≈ 0")
else:
    print("  ✗ ERROR: Velocidad en apogeo debería ser ≈ 0")

if altura_maxima > 0 and altura_maxima < h_teorica * 1.2:
    print("  ✓ Altura máxima razonable (con arrastre < sin arrastre)")
else:
    print("  ✗ ERROR: Altura máxima fuera de rango esperado")

# Verificar que cae de vuelta
if len(alturas) > idx_apogeo + 10:
    if alturas[-1] < alturas[idx_apogeo]:
        print("  ✓ El proyectil cae después del apogeo")
    else:
        print("  ✗ ERROR: El proyectil no cae")
else:
    print("  ⚠ Advertencia: Simulación muy corta para ver la caída completa")

print("="*70)

# Guardar gráfico en la carpeta tests
plt.savefig(os.path.join(os.path.dirname(__file__), 'test_mortero.png'), dpi=150, bbox_inches='tight')
print("\n✓ Gráfico guardado: tests/test_mortero.png")
