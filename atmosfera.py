"""
Módulo para cálculos relacionados con la atmósfera terrestre.

Este módulo contiene funciones para calcular la densidad del aire
en función de la altura sobre el nivel del mar.
"""

import math


def calcular_densidad_aire(altura):
    """
    Calcula la densidad del aire en función de la altura.
    
    Usa un modelo atmosférico estándar por capas:
    - Troposfera: 0 - 11,000 m
    - Estratosfera baja: 11,000 - 25,000 m
    - Estratosfera alta: > 25,000 m
    
    Args:
        altura (float): Altura sobre el nivel del mar (m)
        
    Returns:
        float: Densidad del aire (kg/m³)
    """
    if altura < 11000:
        # Troposfera
        T = 15.04 - 0.00649 * altura  # Temperatura en °C
        P = 101.29 * ((T + 273.1) / 288.08) ** 5.256  # Presión en kPa
    elif 11000 <= altura < 25000:
        # Estratosfera baja
        T = -56.46  # Temperatura en °C
        P = 22.65 * math.exp(1.73 - 0.000157 * altura)  # Presión en kPa
    else:
        # Estratosfera alta
        T = -131.21 + 0.00299 * altura  # Temperatura en °C
        P = 2.488 * ((T + 273.1) / 216.6) ** -11.388  # Presión en kPa
    
    # Densidad usando ecuación de gas ideal
    rho = P / (0.2869 * (T + 273.1))  # Densidad en kg/m³
    return rho
