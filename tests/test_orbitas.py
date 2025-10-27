"""
Test: Órbitas LEO y GEO

Verifica que un satélite con la velocidad orbital correcta
pueda mantener una órbita circular estable.

LEO (200 km): v_orbital ≈ 7,784 m/s
GEO (35,786 km): v_orbital ≈ 3,075 m/s
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cohete import Cohete
from constantes import *
import matplotlib.pyplot as plt
import numpy as np

print("="*70)
print("TEST: ÓRBITAS LEO Y GEO")
print("="*70)

# Función para calcular velocidad orbital
def velocidad_orbital(altura_km):
    """Calcula la velocidad orbital circular a una altura dada"""
    r = R_E + altura_km * 1000
    return np.sqrt(MU / r)

# TEST LEO: 200 km
print(f"\n{'='*70}")
print("TEST LEO: Órbita a 200 km")
print("="*70)

h_leo = 200  # km
r_leo = R_E + h_leo * 1000
v_leo = velocidad_orbital(h_leo)

print(f"Altura: {h_leo} km")
print(f"Radio orbital: {r_leo/1000:.2f} km")
print(f"Velocidad orbital teórica: {v_leo:.2f} m/s ({v_leo/1000:.3f} km/s)")

# Crear satélite en LEO
# Para órbita circular: velocidad puramente tangencial (q=0, gamma=v/r)
cohete_leo = Cohete(
    r_0=r_leo,
    q_0=0.0,              # Velocidad radial = 0 (órbita circular)
    q_dot_0=0.0,
    theta_0=0.0,
    gamma_0=v_leo / r_leo,  # Velocidad angular = v/r
    gamma_dot_0=0.0,
    masa_cohete=1000.0,
    masa_fuel=0.0,        # Sin combustible
    beta=0.0,
    diametro=2.0,
    m_dot=0.0,
    isp=ISP,
    h_0=H_0, h_1=H_1, h_2=H_2
)

# Simular 1 órbita completa (período ≈ 90 minutos para LEO)
T_leo = 2 * np.pi * r_leo / v_leo  # Período orbital
print(f"Período orbital: {T_leo/60:.2f} minutos")

cohete_leo.simular(dt=1.0, t_max=T_leo*1.5, usar_backward=True, log_cada=0)

# TEST GEO: 35,786 km
print(f"\n{'='*70}")
print("TEST GEO: Órbita geoestacionaria a 35,786 km")
print("="*70)

h_geo = 35786  # km
r_geo = R_E + h_geo * 1000
v_geo = velocidad_orbital(h_geo)

print(f"Altura: {h_geo} km")
print(f"Radio orbital: {r_geo/1000:.2f} km")
print(f"Velocidad orbital teórica: {v_geo:.2f} m/s ({v_geo/1000:.3f} km/s)")

# Crear satélite en GEO
cohete_geo = Cohete(
    r_0=r_geo,
    q_0=0.0,
    q_dot_0=0.0,
    theta_0=0.0,
    gamma_0=v_geo / r_geo,
    gamma_dot_0=0.0,
    masa_cohete=1000.0,
    masa_fuel=0.0,
    beta=0.0,
    diametro=2.0,
    m_dot=0.0,
    isp=ISP,
    h_0=H_0, h_1=H_1, h_2=H_2
)

T_geo = 2 * np.pi * r_geo / v_geo
print(f"Período orbital: {T_geo/3600:.2f} horas")

cohete_geo.simular(dt=10.0, t_max=min(T_geo*1.2, 100000), usar_backward=True, log_cada=0)

# Análisis de resultados
print(f"\n{'='*70}")
print("RESULTADOS:")
print("="*70)

# LEO
alturas_leo = [(r - R_E)/1000 for r in cohete_leo.r_hist]
altura_promedio_leo = np.mean(alturas_leo)
altura_std_leo = np.std(alturas_leo)
theta_leo = cohete_leo.theta_hist

print(f"\nLEO (200 km):")
print(f"  Altura promedio: {altura_promedio_leo:.2f} km")
print(f"  Desviación estándar: {altura_std_leo:.2f} km")
print(f"  Altura min: {min(alturas_leo):.2f} km")
print(f"  Altura max: {max(alturas_leo):.2f} km")
print(f"  Ángulo recorrido: {theta_leo[-1]*180/np.pi:.2f}°")

# GEO
alturas_geo = [(r - R_E)/1000 for r in cohete_geo.r_hist]
altura_promedio_geo = np.mean(alturas_geo)
altura_std_geo = np.std(alturas_geo)

print(f"\nGEO (35,786 km):")
print(f"  Altura promedio: {altura_promedio_geo:.2f} km")
print(f"  Desviación estándar: {altura_std_geo:.2f} km")
print(f"  Altura min: {min(alturas_geo):.2f} km")
print(f"  Altura max: {max(alturas_geo):.2f} km")

# Graficar
fig = plt.figure(figsize=(14, 10))

# Subplot 1: Trayectoria polar LEO
ax1 = plt.subplot(2, 2, 1, projection='polar')
ax1.plot(cohete_leo.theta_hist, [r/1000 for r in cohete_leo.r_hist], 'b-', linewidth=2, label='Órbita LEO')
circle_leo = plt.Circle((0, 0), R_E/1000, color='brown', alpha=0.3, transform=ax1.transData._b, label='Tierra')
ax1.set_title('Órbita LEO (200 km)', pad=20)
ax1.legend(loc='upper right')

# Subplot 2: Trayectoria polar GEO
ax2 = plt.subplot(2, 2, 2, projection='polar')
ax2.plot(cohete_geo.theta_hist, [r/1000 for r in cohete_geo.r_hist], 'g-', linewidth=2, label='Órbita GEO')
ax2.set_title('Órbita GEO (35,786 km)', pad=20)
ax2.legend(loc='upper right')

# Subplot 3: Altura vs tiempo LEO
ax3 = plt.subplot(2, 2, 3)
tiempo_leo = np.arange(len(alturas_leo))
ax3.plot(tiempo_leo, alturas_leo, 'b-', linewidth=2)
ax3.axhline(y=h_leo, color='r', linestyle='--', alpha=0.5, label=f'Altura objetivo ({h_leo} km)')
ax3.set_xlabel('Tiempo (s)')
ax3.set_ylabel('Altura (km)')
ax3.set_title('LEO: Altura vs Tiempo')
ax3.grid(True, alpha=0.3)
ax3.legend()

# Subplot 4: Altura vs tiempo GEO
ax4 = plt.subplot(2, 2, 4)
tiempo_geo = np.arange(len(alturas_geo)) * 10
ax4.plot(tiempo_geo, alturas_geo, 'g-', linewidth=2)
ax4.axhline(y=h_geo, color='r', linestyle='--', alpha=0.5, label=f'Altura objetivo ({h_geo} km)')
ax4.set_xlabel('Tiempo (s)')
ax4.set_ylabel('Altura (km)')
ax4.set_title('GEO: Altura vs Tiempo')
ax4.grid(True, alpha=0.3)
ax4.legend()

plt.tight_layout()
plt.savefig('test_orbitas_leo_geo.png', dpi=150)
print(f"\n✓ Gráfico guardado: test_orbitas_leo_geo.png")

# Verificaciones
print(f"\n{'='*70}")
print("VERIFICACIONES:")

# LEO
variacion_leo = (max(alturas_leo) - min(alturas_leo)) / h_leo * 100
if variacion_leo < 5:  # Menos del 5% de variación
    print(f"  ✓ LEO: Órbita estable (variación: {variacion_leo:.2f}%)")
else:
    print(f"  ✗ LEO: Órbita inestable (variación: {variacion_leo:.2f}%)")

if abs(altura_promedio_leo - h_leo) < 10:  # Dentro de 10 km
    print(f"  ✓ LEO: Altura promedio correcta ({altura_promedio_leo:.2f} km)")
else:
    print(f"  ⚠ LEO: Altura promedio desviada ({altura_promedio_leo:.2f} km vs {h_leo} km)")

# GEO
variacion_geo = (max(alturas_geo) - min(alturas_geo)) / h_geo * 100
if variacion_geo < 5:
    print(f"  ✓ GEO: Órbita estable (variación: {variacion_geo:.2f}%)")
else:
    print(f"  ✗ GEO: Órbita inestable (variación: {variacion_geo:.2f}%)")

if abs(altura_promedio_geo - h_geo) < 100:  # Dentro de 100 km
    print(f"  ✓ GEO: Altura promedio correcta ({altura_promedio_geo:.2f} km)")
else:
    print(f"  ⚠ GEO: Altura promedio desviada ({altura_promedio_geo:.2f} km vs {h_geo} km)")

print("="*70)

# Guardar gráfico en la carpeta tests
plt.savefig(os.path.join(os.path.dirname(__file__), 'test_orbitas_leo_geo.png'), dpi=150, bbox_inches='tight')
print("\n✓ Gráfico guardado: tests/test_orbitas_leo_geo.png")
