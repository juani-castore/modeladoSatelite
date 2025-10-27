"""
Test: Velocidad de escape

Verifica que un cohete con velocidad = velocidad de escape
pueda alejarse indefinidamente de la Tierra.

Velocidad de escape: v_esc = √(2GM/R) ≈ 11,186 m/s
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cohete import Cohete
from constantes import *
import matplotlib.pyplot as plt
import numpy as np

print("="*70)
print("TEST: VELOCIDAD DE ESCAPE")
print("="*70)

# Calcular velocidad de escape teórica
v_escape_teorica = np.sqrt(2 * MU / R_E)
print(f"\nVelocidad de escape teórica: {v_escape_teorica:.2f} m/s ({v_escape_teorica/1000:.2f} km/s)")

# Test 1: Con velocidad MENOR que velocidad de escape (debe volver)
print(f"\n{'='*70}")
print("TEST 1: Velocidad SUB-ESCAPE (90% de v_esc)")
print("="*70)

v_inicial_1 = 0.9 * v_escape_teorica

cohete1 = Cohete(
    r_0=R_E + 100,
    q_0=v_inicial_1,      # 90% de v_escape
    q_dot_0=0.0,
    theta_0=0.0,
    gamma_0=0.0,
    gamma_dot_0=0.0,
    masa_cohete=1000.0,
    masa_fuel=0.0,        # Sin combustible
    beta=0.0,
    diametro=1.0,
    m_dot=0.0,
    isp=ISP,
    h_0=H_0, h_1=H_1, h_2=H_2
)

print(f"Velocidad inicial: {v_inicial_1:.2f} m/s ({v_inicial_1/v_escape_teorica*100:.1f}% de v_esc)")

cohete1.simular(dt=1.0, t_max=3000, usar_backward=True, log_cada=0)

alturas1 = [(r - R_E)/1000 for r in cohete1.r_hist]
velocidades1 = cohete1.q_hist
tiempo1 = np.arange(len(alturas1))

altura_max_1 = max(alturas1)
print(f"Altura máxima alcanzada: {altura_max_1:.2f} km")
print(f"Velocidad final: {velocidades1[-1]:.2f} m/s")

# Test 2: Con velocidad IGUAL a velocidad de escape
print(f"\n{'='*70}")
print("TEST 2: Velocidad DE ESCAPE (100% de v_esc)")
print("="*70)

cohete2 = Cohete(
    r_0=R_E + 100,
    q_0=v_escape_teorica,  # Exactamente v_escape
    q_dot_0=0.0,
    theta_0=0.0,
    gamma_0=0.0,
    gamma_dot_0=0.0,
    masa_cohete=1000.0,
    masa_fuel=0.0,
    beta=0.0,
    diametro=1.0,
    m_dot=0.0,
    isp=ISP,
    h_0=H_0, h_1=H_1, h_2=H_2
)

print(f"Velocidad inicial: {v_escape_teorica:.2f} m/s (100% de v_esc)")

cohete2.simular(dt=1.0, t_max=3000, usar_backward=True, log_cada=0)

alturas2 = [(r - R_E)/1000 for r in cohete2.r_hist]
velocidades2 = cohete2.q_hist
tiempo2 = np.arange(len(alturas2))

altura_max_2 = max(alturas2)
print(f"Altura alcanzada: {alturas2[-1]:.2f} km")
print(f"Velocidad final: {velocidades2[-1]:.2f} m/s")

# Graficar comparación
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Altura vs tiempo
ax1.plot(tiempo1, alturas1, 'r-', linewidth=2, label=f'90% v_esc (v={v_inicial_1:.0f} m/s)')
ax1.plot(tiempo2, alturas2, 'b-', linewidth=2, label=f'100% v_esc (v={v_escape_teorica:.0f} m/s)')
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Altura (km)')
ax1.set_title('Velocidad de Escape: Altura vs Tiempo')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Velocidad vs tiempo
ax2.plot(tiempo1, velocidades1, 'r-', linewidth=2, label='90% v_esc')
ax2.plot(tiempo2, velocidades2, 'b-', linewidth=2, label='100% v_esc')
ax2.axhline(y=0, color='k', linestyle='--', alpha=0.3)
ax2.set_xlabel('Tiempo (s)')
ax2.set_ylabel('Velocidad radial (m/s)')
ax2.set_title('Velocidad Radial vs Tiempo')
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.savefig('test_velocidad_escape.png', dpi=150)
print(f"\n✓ Gráfico guardado: test_velocidad_escape.png")

# Verificaciones
print(f"\n{'='*70}")
print("VERIFICACIONES:")

# Test 1: Sub-escape debe volver (velocidad final negativa)
if velocidades1[-1] < 0:
    print("  ✓ TEST 1: Velocidad sub-escape regresa a la Tierra")
else:
    print(f"  ⚠ TEST 1: Velocidad final = {velocidades1[-1]:.2f} m/s (debería ser < 0)")

# Test 2: Velocidad de escape debe seguir alejándose (velocidad final > 0)
if velocidades2[-1] > 0:
    print("  ✓ TEST 2: Velocidad de escape permite escapar")
    if velocidades2[-1] < 100:  # Debería tender a 0
        print(f"      Velocidad final ≈ 0 ({velocidades2[-1]:.2f} m/s) ✓")
else:
    print(f"  ✗ TEST 2: ERROR - No escapa (v_final = {velocidades2[-1]:.2f} m/s)")

# Verificar altura continua creciendo en test 2
if alturas2[-1] > alturas2[-100]:
    print("  ✓ TEST 2: Altura sigue aumentando")
else:
    print("  ✗ TEST 2: ERROR - Altura dejó de crecer")

print("="*70)

# Guardar gráfico en la carpeta tests
plt.savefig(os.path.join(os.path.dirname(__file__), 'test_velocidad_escape.png'), dpi=150, bbox_inches='tight')
print("\n✓ Gráfico guardado: tests/test_velocidad_escape.png")
