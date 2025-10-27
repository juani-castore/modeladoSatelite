"""
Módulo para generar gráficos de la simulación del cohete.

Este módulo contiene funciones para visualizar:
- Evolución temporal de posición, velocidad y aceleración (radial y angular)
- Masa del cohete y tasa de consumo
- Dirección del empuje (beta)
- Trayectoria en coordenadas polares

Todos los gráficos se guardan en la carpeta 'graficos/'
"""

import math
import os
import numpy as np
import matplotlib.pyplot as plt
from constantes import R_E


# Crear carpeta de gráficos si no existe
CARPETA_GRAFICOS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    'graficos'
)
if not os.path.exists(CARPETA_GRAFICOS):
    os.makedirs(CARPETA_GRAFICOS)
    print(f"Carpeta creada: {CARPETA_GRAFICOS}")


def graficar_evolucion_cohete(cohete, dt: float):
    """
    Genera múltiples gráficos mostrando la evolución temporal del cohete.
    
    Gráficos generados y guardados en la carpeta 'graficos/':
    1. 01_aceleracion_radial.png - Aceleración radial vs tiempo
    2. 02_velocidad_radial.png - Velocidad radial vs tiempo
    3. 03_posicion_radial.png - Posición radial (radio y altura) vs tiempo
    4. 04_masa_cohete.png - Masa del cohete vs tiempo
    5. 05_aceleracion_angular.png - Aceleración angular vs tiempo
    6. 06_velocidad_angular.png - Velocidad angular vs tiempo
    7. 07_posicion_angular.png - Posición angular vs tiempo
    8. 08_direccion_empuje_beta.png - Dirección del empuje (beta) vs tiempo
    
    Args:
        cohete: Objeto Cohete con historiales de simulación
        dt (float): Paso de tiempo usado en la simulación (s)
    """
    # Crear eje de tiempo
    N = len(cohete.r_hist)
    tiempo = np.arange(N) * dt
    
    # LIMITAR A LOS PRIMEROS 500 SEGUNDOS (zona de interés: despegue)
    idx_500s = int(500 / dt) if len(tiempo) > int(500 / dt) else len(tiempo)
    tiempo = tiempo[:idx_500s]
    
    # Convertir historiales a arrays numpy (limitados a 500s)
    r = np.array(cohete.r_hist[:idx_500s])
    q = np.array(cohete.q_hist[:idx_500s])
    q_dot = np.array(cohete.q_dot_hist[:idx_500s])
    theta = np.array(cohete.theta_hist[:idx_500s])
    gamma = np.array(cohete.gamma_hist[:idx_500s])
    gamma_dot = np.array(cohete.gamma_dot_hist[:idx_500s])
    masa = np.array(cohete.masa_hist[:idx_500s])
    beta = np.array(cohete.beta_hist[:idx_500s])
    
    altura = r - R_E
    
    # ====================
    # GRÁFICO 1: Aceleración radial
    # ====================
    plt.figure(figsize=(12, 5))
    plt.plot(tiempo, q_dot, 'b-', linewidth=1.5)
    plt.xlabel('Tiempo (s)', fontsize=12)
    plt.ylabel('Aceleración radial (m/s²)', fontsize=12)
    plt.title('Evolución de la aceleración radial', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '01_aceleracion_radial.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    # ====================
    # GRÁFICO 2: Velocidad radial
    # ====================
    plt.figure(figsize=(12, 5))
    plt.plot(tiempo, q, 'g-', linewidth=1.5)
    plt.xlabel('Tiempo (s)', fontsize=12)
    plt.ylabel('Velocidad radial (m/s)', fontsize=12)
    plt.title('Evolución de la velocidad radial', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '02_velocidad_radial.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    # ====================
    # GRÁFICO 3: Posición radial (radio y altura)
    # ====================
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Radio
    ax1.plot(tiempo, r, 'r-', linewidth=1.5)
    ax1.set_ylabel('Radio desde centro de la Tierra (m)', fontsize=11)
    ax1.set_title('Evolución de la posición radial', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Altura sobre el nivel del mar
    ax2.plot(tiempo, altura / 1000.0, 'orange', linewidth=1.5)
    ax2.set_xlabel('Tiempo (s)', fontsize=12)
    ax2.set_ylabel('Altura sobre el nivel del mar (km)', fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '03_posicion_radial.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    # ====================
    # GRÁFICO 4: Masa del cohete
    # ====================
    plt.figure(figsize=(12, 5))
    plt.plot(tiempo, masa, 'purple', linewidth=1.5)
    plt.xlabel('Tiempo (s)', fontsize=12)
    plt.ylabel('Masa (kg)', fontsize=12)
    plt.title('Evolución de la masa del cohete', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Línea horizontal para masa estructural
    plt.axhline(y=cohete.masa_cohete, color='red', linestyle='--',
                linewidth=1, label='Masa estructural (sin combustible)')
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '04_masa_cohete.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    # ====================
    # GRÁFICO 5: Aceleración angular
    # ====================
    plt.figure(figsize=(12, 5))
    plt.plot(tiempo, gamma_dot, 'b-', linewidth=1.5)
    plt.xlabel('Tiempo (s)', fontsize=12)
    plt.ylabel('Aceleración angular (rad/s²)', fontsize=12)
    plt.title('Evolución de la aceleración angular', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '05_aceleracion_angular.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    # ====================
    # GRÁFICO 6: Velocidad angular
    # ====================
    plt.figure(figsize=(12, 5))
    plt.plot(tiempo, gamma, 'g-', linewidth=1.5)
    plt.xlabel('Tiempo (s)', fontsize=12)
    plt.ylabel('Velocidad angular (rad/s)', fontsize=12)
    plt.title('Evolución de la velocidad angular', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '06_velocidad_angular.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    # ====================
    # GRÁFICO 7: Posición angular
    # ====================
    plt.figure(figsize=(12, 5))
    plt.plot(tiempo, theta, 'r-', linewidth=1.5)
    plt.xlabel('Tiempo (s)', fontsize=12)
    plt.ylabel('Posición angular (rad)', fontsize=12)
    plt.title('Evolución de la posición angular', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '07_posicion_angular.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    # ====================
    # GRÁFICO 8: Dirección del empuje (beta)
    # ====================
    plt.figure(figsize=(12, 5))
    # Convertir a grados para mejor comprensión
    beta_grados = np.rad2deg(beta)
    plt.plot(tiempo, beta_grados, 'orange', linewidth=1.5)
    plt.xlabel('Tiempo (s)', fontsize=12)
    plt.ylabel('Ángulo de empuje β (grados)', fontsize=12)
    plt.title('Evolución de la dirección del empuje', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Líneas de referencia
    plt.axhline(y=0, color='gray', linestyle=':', linewidth=1,
                label='0° (empuje radial)')
    plt.axhline(y=45, color='gray', linestyle=':', linewidth=1,
                label='45°')
    plt.axhline(y=90, color='gray', linestyle=':', linewidth=1,
                label='90° (empuje tangencial)')
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '08_direccion_empuje_beta.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    # ====================
    # GRÁFICO 9: Tasa de consumo de combustible (mdot)
    # ====================
    from utilidades import calcular_mdot
    
    plt.figure(figsize=(12, 5))
    # Calcular mdot para cada tiempo
    mdot_valores = np.array([calcular_mdot(t) for t in tiempo])
    
    plt.plot(tiempo, mdot_valores, 'purple', linewidth=2)
    plt.xlabel('Tiempo (s)', fontsize=12)
    plt.ylabel('Tasa de consumo mdot (kg/s)', fontsize=12)
    plt.title('Evolución de la tasa de consumo de combustible', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Línea vertical en t=70s (cambio de fase)
    plt.axvline(x=70, color='red', linestyle='--', linewidth=1.5,
                label='Cambio de fase (t=70s)')
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '09_mdot.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    # ====================
    # GRÁFICO 10: Beta y mdot combinados
    # ====================
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Subplot 1: Beta
    ax1.plot(tiempo, beta_grados, 'orange', linewidth=2, label='Beta (ángulo empuje)')
    ax1.set_ylabel('Ángulo β (grados)', fontsize=11)
    ax1.set_title('Perfil de vuelo: Beta y mdot vs Tiempo', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='gray', linestyle=':', linewidth=1, alpha=0.5)
    ax1.axhline(y=90, color='gray', linestyle=':', linewidth=1, alpha=0.5)
    ax1.axvline(x=70, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax1.legend(fontsize=10)
    
    # Subplot 2: mdot
    ax2.plot(tiempo, mdot_valores, 'purple', linewidth=2, label='mdot (consumo)')
    ax2.set_xlabel('Tiempo (s)', fontsize=12)
    ax2.set_ylabel('mdot (kg/s)', fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.axvline(x=70, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Cambio fase')
    ax2.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '10_perfil_vuelo.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    # ====================
    # GRÁFICOS ZOOM: Primeros 500 segundos
    # ====================
    # Encontrar índice correspondiente a t=500s
    idx_500 = min(np.searchsorted(tiempo, 500), len(tiempo)-1)
    
    # ====================
    # GRÁFICO 11: Perfil vuelo ZOOM (primeros 500s)
    # ====================
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Subplot 1: Beta
    ax1.plot(tiempo[:idx_500], beta_grados[:idx_500], 'orange', linewidth=2, label='Beta (ángulo empuje)')
    ax1.set_ylabel('Ángulo β (grados)', fontsize=11)
    ax1.set_title('ZOOM: Perfil de vuelo primeros 500s - Beta y mdot', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='gray', linestyle=':', linewidth=1, alpha=0.5)
    ax1.axhline(y=90, color='gray', linestyle=':', linewidth=1, alpha=0.5)
    ax1.axvline(x=30, color='blue', linestyle='--', linewidth=1.5, alpha=0.7, label='Inicio gravity turn (30s)')
    ax1.axvline(x=70, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Cambio fase (70s)')
    ax1.legend(fontsize=9)
    ax1.set_xlim(0, 500)
    
    # Subplot 2: mdot
    ax2.plot(tiempo[:idx_500], mdot_valores[:idx_500], 'purple', linewidth=2, label='mdot (consumo)')
    ax2.set_xlabel('Tiempo (s)', fontsize=12)
    ax2.set_ylabel('mdot (kg/s)', fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.axvline(x=30, color='blue', linestyle='--', linewidth=1.5, alpha=0.7)
    ax2.axvline(x=70, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax2.legend(fontsize=9)
    ax2.set_xlim(0, 500)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '11_perfil_vuelo_zoom_500s.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    # ====================
    # GRÁFICO 12: Altura y velocidades ZOOM (primeros 500s)
    # ====================
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Subplot 1: Altura
    ax1.plot(tiempo[:idx_500], altura[:idx_500] / 1000.0, 'orange', linewidth=2, label='Altura')
    ax1.set_ylabel('Altura (km)', fontsize=11)
    ax1.set_title('ZOOM: Primeros 500s - Altura y Velocidades', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.axvline(x=30, color='blue', linestyle='--', linewidth=1, alpha=0.5)
    ax1.axvline(x=70, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax1.legend(fontsize=9)
    ax1.set_xlim(0, 500)
    
    # Subplot 2: Velocidades
    v_tangencial = r[:idx_500] * gamma[:idx_500]  # v_tangencial = r * gamma
    ax2.plot(tiempo[:idx_500], q[:idx_500], 'b-', linewidth=2, label='Velocidad radial', alpha=0.7)
    ax2.plot(tiempo[:idx_500], v_tangencial, 'g-', linewidth=2, label='Velocidad tangencial', alpha=0.7)
    ax2.set_xlabel('Tiempo (s)', fontsize=12)
    ax2.set_ylabel('Velocidad (m/s)', fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.axvline(x=30, color='blue', linestyle='--', linewidth=1, alpha=0.5, label='t=30s')
    ax2.axvline(x=70, color='red', linestyle='--', linewidth=1, alpha=0.5, label='t=70s')
    ax2.legend(fontsize=9)
    ax2.set_xlim(0, 500)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '12_altura_velocidad_zoom_500s.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    # ====================
    # GRÁFICO 13: Masa ZOOM (primeros 500s)
    # ====================
    plt.figure(figsize=(12, 5))
    plt.plot(tiempo[:idx_500], masa[:idx_500], 'purple', linewidth=2)
    plt.xlabel('Tiempo (s)', fontsize=12)
    plt.ylabel('Masa (kg)', fontsize=12)
    plt.title('ZOOM: Evolución de la masa - Primeros 500s', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Líneas de referencia
    plt.axhline(y=cohete.masa_cohete, color='red', linestyle='--',
                linewidth=1, label='Masa estructural')
    plt.axvline(x=30, color='blue', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(x=70, color='red', linestyle='--', linewidth=1, alpha=0.5)
    
    # Buscar cuando se agota el combustible
    idx_agotado = np.where(masa <= cohete.masa_cohete * 1.01)[0]
    if len(idx_agotado) > 0 and idx_agotado[0] < idx_500:
        t_agotado = tiempo[idx_agotado[0]]
        plt.axvline(x=t_agotado, color='orange', linestyle='--', linewidth=2,
                   label=f'Combustible agotado (t={t_agotado:.1f}s)')
    
    plt.legend(fontsize=10)
    plt.xlim(0, 500)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '13_masa_zoom_500s.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n✓ 13 gráficos de evolución guardados en: {CARPETA_GRAFICOS}")
    print(f"  - Gráficos 1-10: Evolución completa")
    print(f"  - Gráficos 11-13: ZOOM primeros 500 segundos")


def graficar_trayectoria_polar(cohete):
    """
    Genera un gráfico de la trayectoria del cohete en coordenadas polares.
    
    Muestra:
    - Trayectoria del cohete
    - Circunferencia de la Tierra
    
    Guarda: 09_trayectoria_polar.png
    
    Args:
        cohete: Objeto Cohete con historiales de simulación
    """
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, projection='polar')
    
    # Trayectoria del cohete
    theta = np.array(cohete.theta_hist)
    r = np.array(cohete.r_hist)
    ax.plot(theta, r, 'b-', linewidth=2, label='Trayectoria del cohete')
    
    # Circunferencia de la Tierra
    theta_circle = np.linspace(0, 2*np.pi, 720)
    r_earth = np.full_like(theta_circle, R_E)
    ax.plot(theta_circle, r_earth, 'brown', linestyle='--',
            linewidth=2, alpha=0.8, label='Superficie terrestre')
    
    ax.set_title('Trayectoria del cohete en coordenadas polares',
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '09_trayectoria_polar.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Gráfico de trayectoria polar guardado en: {CARPETA_GRAFICOS}")


def graficar_metricas_adicionales(cohete, dt: float):
    """
    Genera gráficos de métricas adicionales útiles.
    
    Gráficos generados y guardados:
    - 10_comparacion_velocidades.png - Comparación de velocidades 
      (radial, tangencial, total)
    
    Args:
        cohete: Objeto Cohete con historiales de simulación
        dt (float): Paso de tiempo usado en la simulación (s)
    """
    N = len(cohete.r_hist)
    tiempo = np.arange(N) * dt
    
    r = np.array(cohete.r_hist)
    q = np.array(cohete.q_hist)
    gamma = np.array(cohete.gamma_hist)
    
    # Calcular velocidad tangencial y total
    v_tangencial = r * gamma
    v_total = np.sqrt(q**2 + v_tangencial**2)
    
    # ====================
    # GRÁFICO 1: Comparación de velocidades
    # ====================
    plt.figure(figsize=(12, 6))
    plt.plot(tiempo, q, 'b-', linewidth=1.5, label='Velocidad radial')
    plt.plot(tiempo, v_tangencial, 'g-', linewidth=1.5,
             label='Velocidad tangencial')
    plt.plot(tiempo, v_total, 'r-', linewidth=2, label='Velocidad total')
    plt.xlabel('Tiempo (s)', fontsize=12)
    plt.ylabel('Velocidad (m/s)', fontsize=12)
    plt.title('Comparación de velocidades', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, '10_comparacion_velocidades.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Gráfico de comparación de velocidades guardado en: {CARPETA_GRAFICOS}")


def calcular_desplazamiento_angular_total(theta_hist):
    """
    Calcula el desplazamiento angular total sin saltos de 2π.
    
    Unwrap de ángulos para obtener el desplazamiento angular acumulado real.
    
    Args:
        theta_hist (list): Historial de posiciones angulares (rad)
        
    Returns:
        float: Desplazamiento angular total (rad)
    """
    acc = 0.0
    prev = theta_hist[0]
    for th in theta_hist[1:]:
        d = th - prev
        # Traer d al rango (-π, π] para evitar saltos artificiales de 2π
        while d <= -math.pi:
            d += 2 * math.pi
        while d > math.pi:
            d -= 2 * math.pi
        acc += d
        prev = th
    return acc


def imprimir_metricas_finales(cohete, dt: float):
    """
    Imprime un resumen de las métricas finales de la simulación.
    
    Métricas:
    - Altura máxima alcanzada
    - Velocidades máximas (radial, tangencial, total)
    - Tiempo total de vuelo
    - Desplazamiento angular total
    - Distancia de arco sobre la superficie terrestre
    
    Args:
        cohete: Objeto Cohete con historiales de simulación
        dt (float): Paso de tiempo usado en la simulación (s)
    """
    print("\n" + "="*60)
    print("MÉTRICAS FINALES DE LA SIMULACIÓN")
    print("="*60)
    
    # Altura máxima
    r = np.array(cohete.r_hist)
    altura_max_m = max(r - R_E)
    print(f"Altura máxima: {altura_max_m/1000:.3f} km ({altura_max_m:.0f} m)")
    
    # Velocidades máximas
    q = np.array(cohete.q_hist)
    gamma = np.array(cohete.gamma_hist)
    v_rad_max = max(q)
    v_tan = r * gamma
    v_tan_max = max(v_tan)
    v_total = np.sqrt(q**2 + v_tan**2)
    v_tot_max = max(v_total)
    
    print(f"Velocidad radial máxima: {v_rad_max:.3f} m/s")
    print(f"Velocidad tangencial máxima: {v_tan_max:.3f} m/s")
    print(f"Velocidad total máxima: {v_tot_max:.3f} m/s")
    
    # Tiempo total
    tiempo_total_s = (len(cohete.r_hist) - 1) * dt
    print(f"Tiempo total de vuelo: {tiempo_total_s:.1f} s ({tiempo_total_s/60:.2f} min)")
    
    # Desplazamiento angular
    theta = cohete.theta_hist
    despl_angular_total = calcular_desplazamiento_angular_total(theta)
    print(f"Desplazamiento angular total: {despl_angular_total:.6f} rad")
    print(f"  = {np.rad2deg(despl_angular_total):.3f} grados")
    
    # Distancia sobre la superficie
    distancia_superficie_m = R_E * abs(despl_angular_total)
    print(f"Distancia de arco sobre la Tierra: {distancia_superficie_m/1000:.3f} km")
    
    print("="*60 + "\n")
