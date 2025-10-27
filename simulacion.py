"""
Script principal para ejecutar la simulación del cohete.

Este script:
1. Configura los parámetros del cohete
2. Ejecuta la simulación
3. Muestra métricas finales
4. Genera gráficos de análisis
"""

from cohete import Cohete
from constantes import (
    R_E, DT, T_MAX, USAR_BACKWARD, LOG_CADA,
    MASA_COHETE, MASA_FUEL, DIAMETRO_COHETE, ISP, M_DOT_0,
    R_0, Q_0, Q_DOT_0, THETA_0, GAMMA_0, GAMMA_DOT_0, BETA_0,
    H_0, H_1, H_2
)
from graficos import (
    graficar_evolucion_cohete, graficar_trayectoria_polar,
    graficar_metricas_adicionales, imprimir_metricas_finales
)


def main():
    """
    Función principal que ejecuta la simulación completa.
    """
    print("="*60)
    print("SIMULACIÓN DE COHETE - PUESTA EN ÓRBITA")
    print("="*60)
    print(f"Método de integración: {'Backward Euler' if USAR_BACKWARD else 'Forward Euler'}")
    print(f"Paso de tiempo: {DT} s")
    print(f"Tiempo máximo: {T_MAX} s ({T_MAX/60:.1f} min)")
    print("="*60 + "\n")
    
    # =========================
    # CREAR INSTANCIA DEL COHETE
    # =========================
    cohete1 = Cohete(
        r_0=R_0,
        q_0=Q_0,
        q_dot_0=Q_DOT_0,
        theta_0=THETA_0,
        gamma_0=GAMMA_0,
        gamma_dot_0=GAMMA_DOT_0,
        masa_cohete=MASA_COHETE,
        masa_fuel=MASA_FUEL,
        beta=BETA_0,
        diametro=DIAMETRO_COHETE,
        m_dot=M_DOT_0,
        isp=ISP,
        h_0=H_0,
        h_1=H_1,
        h_2=H_2
    )
    
    # Asegurar que los historiales estén inicializados
    # (ya deberían estarlo en __init__, pero por seguridad)
    if not hasattr(cohete1, "r_hist"):
        cohete1.r_hist = [cohete1.r]
    if not hasattr(cohete1, "q_hist"):
        cohete1.q_hist = [cohete1.q]
    if not hasattr(cohete1, "theta_hist"):
        cohete1.theta_hist = [cohete1.theta]
    if not hasattr(cohete1, "gamma_hist"):
        cohete1.gamma_hist = [cohete1.gamma]
    if not hasattr(cohete1, "masa_hist"):
        cohete1.masa_hist = [cohete1.masa]
    
    # =========================
    # EJECUTAR SIMULACIÓN
    # =========================
    resultado = cohete1.simular(
        dt=DT,
        t_max=T_MAX,
        usar_backward=USAR_BACKWARD,
        log_cada=LOG_CADA
    )
    
    # =========================
    # MOSTRAR MÉTRICAS FINALES
    # =========================
    imprimir_metricas_finales(cohete1, DT)
    
    # =========================
    # GENERAR GRÁFICOS
    # =========================
    print("Generando gráficos de evolución temporal...")
    graficar_evolucion_cohete(cohete1, DT)
    
    print("Generando gráfico de trayectoria polar...")
    graficar_trayectoria_polar(cohete1)
    
    print("Generando gráficos de métricas adicionales...")
    graficar_metricas_adicionales(cohete1, DT)
    
    print("\n" + "="*60)
    print("SIMULACIÓN COMPLETADA")
    print("="*60)
    
    return cohete1, resultado


if __name__ == "__main__":
    cohete_simulado, resultado_simulacion = main()
