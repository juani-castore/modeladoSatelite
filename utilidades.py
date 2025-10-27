"""
Funciones auxiliares para la simulación del cohete.

Este módulo contiene funciones de utilidad para cálculos físicos
como gravedad, velocidad, área, ángulo de empuje beta, y tasa
de consumo de combustible.
"""

import math
import numpy as np
from constantes import G, M_EARTH, R_E


def calcular_gravedad(radio):
    """
    Calcula la gravedad en función del radio desde el centro de la Tierra.
    
    Args:
        radio (float): Distancia desde el centro de la Tierra (m)
        
    Returns:
        float: Aceleración gravitacional (m/s²)
    """
    return G * M_EARTH / (radio ** 2)


def calcular_velocidad(v_rad, v_ang, distancia_radial):
    """
    Calcula la velocidad total a partir de las componentes radial y angular.
    
    Args:
        v_rad (float): Velocidad radial (m/s)
        v_ang (float): Velocidad angular (rad/s)
        distancia_radial (float): Distancia desde el centro de la Tierra (m)
        
    Returns:
        float: Velocidad total (m/s)
    """
    v_tangencial = v_ang * distancia_radial
    return math.sqrt(v_rad**2 + v_tangencial**2)


def calcular_area_frontal_esfera(radio):
    """
    Calcula el área frontal de una esfera dado su radio.
    
    Args:
        radio (float): Radio de la esfera (m)
        
    Returns:
        float: Área frontal (m²)
    """
    return math.pi * radio**2


def calcular_beta_tiempo(tiempo_de_vuelo: float) -> float:
    """
    Calcula el ángulo de inclinación del empuje en función del tiempo.
    
    Estrategia FINAL para LEO 200 km:
    - Fase 1 (0-30s): Beta = 0° (vertical - altura inicial)
    - Fase 2 (30-60s): Beta 0° → 45° (gravity turn más agresivo)
    - Fase 3 (60-100s): Beta 45° → 80° (transición rápida a horizontal)
    - Fase 4 (100-150s): Beta 80° → 90° (completar horizontal)
    - Fase 5 (150s+): Beta = 90° (horizontal - circularización)
    
    Llegar a 90° a los 150s (antes era 250s) para construir
    v_tangencial antes y reducir apogeo de 503km a ~200km.
    
    Args:
        tiempo_de_vuelo (float): Tiempo desde el despegue (s)
        
    Returns:
        float: Ángulo beta (rad)
    """
    # Horizontal más temprano para reducir apogeo
    tiempos = np.array([0, 30, 50, 69, 100, 150, 250, 400], float)
    betas = np.deg2rad([0, 0, 30, 50, 80, 90, 90, 90], dtype=float)
    
    return float(np.interp(tiempo_de_vuelo, tiempos, betas))


def calcular_beta_altura(altura: float, h_0: float, h_1: float, 
                         h_2: float) -> float:
    """
    Calcula el ángulo de inclinación del empuje en función de la altura.
    
    Usa interpolación lineal por tramos entre puntos de control.
    Esta es la función actualmente utilizada en la simulación.
    
    Estrategia de guiado MEJORADA (Gravity Turn optimizado):
    - Despegue vertical corto (solo para escapar la plataforma)
    - Transición temprana y agresiva hacia empuje horizontal
    - Mayor énfasis en construir velocidad tangencial
    - Define 9 puntos de control de altura
    - Interpola linealmente el ángulo beta entre ellos
    - Limita beta al rango [0, π/2]
    
    Args:
        altura (float): Altura sobre el nivel del mar (m)
        h_0 (float): Primera altura de transición (m)
        h_1 (float): Segunda altura de transición (m)
        h_2 (float): Tercera altura de transición (m)
        
    Returns:
        float: Ángulo beta (rad)
    """
    h0 = float(h_0)
    h1 = float(h_1)
    h2 = float(h_2)

    # Puntos de control de altura - HORIZONTAL MÁS TEMPRANO
    # Objetivo: empuje horizontal completo desde 150 km para velocidad orbital
    a0 = 0.0                      # Despegue
    a1 = h0                       # Mantener vertical más tiempo
    a2 = h0 + 0.20 * (h1 - h0)   # Transición
    a3 = h0 + 0.40 * (h1 - h0)   # Ángulo medio bajo
    a4 = h0 + 0.65 * (h1 - h0)   # Ángulo medio
    a5 = h1                       # Ángulo medio-alto
    a6 = h1 + 0.30 * (h2 - h1)   # Inclinado (antes: 0.35)
    a7 = h1 + 0.60 * (h2 - h1)   # Casi horizontal (antes: 0.70)
    a8 = h2                       # Horizontal completo

    alturas = np.array([a0, a1, a2, a3, a4, a5, a6, a7, a8], float)
    # Ángulos PARA VELOCIDAD ORBITAL: horizontal desde ~55km (150km altura)
    # Objetivo: MÁXIMA aceleración tangencial en zona orbital
    # 89° en a7 (~64km altura = ~150km altitud) = casi todo horizontal
    betas = np.deg2rad([0, 3, 12, 28, 45, 62, 77, 88, 90], dtype=float)
    
    # Interpolación lineal
    beta = float(np.interp(altura, alturas, betas))
    
    # Limitar beta al rango válido
    return max(0.0, min(math.pi/2, beta))


def calcular_mdot(tiempo: float) -> float:
    """
    Calcula la tasa de consumo de combustible en función del TIEMPO.
    
    Estrategia basada en ejemplo de referencia (ajustado):
    - Fase 1 (0-69s): mdot = 4492 kg/s - Ascenso rápido
    - Fase 2 (69-280s): mdot = 1118 kg/s - Circularización
    - Fase 3 (280s+): mdot = 0 - Órbita libre
    
    Consumo estimado:
    - Fase 1: 4492 kg/s × 69s ≈ 310,000 kg
    - Fase 2: 1118 kg/s × 211s ≈ 236,000 kg
    - Total: ~546,000 kg (dentro del límite de 548,000 kg)
    
    Args:
        tiempo (float): Tiempo desde el despegue (s)
        
    Returns:
        float: Tasa de consumo de combustible (kg/s)
    """
    if tiempo < 69.0:
        return 4492.0  # Fase 1: ascenso según referencia
    elif tiempo < 280.0:
        return 1118.0  # Fase 2: circularización según referencia
    else:
        return 0.0  # Fase 3: órbita libre