"""
Clase Cohete para la simulación de trayectoria orbital.

Este módulo contiene la clase Cohete que modela el comportamiento
dinámico del cohete usando ecuaciones de movimiento en coordenadas
polares y métodos de integración numérica (Forward y Backward Euler).
"""

import math
from constantes import (
    G0, R_E, CD, MU, BETA_ALTURA
)
from atmosfera import calcular_densidad_aire
from utilidades import (
    calcular_gravedad, calcular_velocidad, calcular_area_frontal_esfera,
    calcular_beta_altura, calcular_beta_tiempo, calcular_mdot
)


class Cohete:
    """
    Clase que representa un cohete y simula su trayectoria.
    
    Variables de estado (coordenadas polares):
    - r: Posición radial (m) - distancia desde el centro de la Tierra
    - q: Velocidad radial (m/s)
    - q_dot: Aceleración radial (m/s²)
    - theta: Posición angular (rad)
    - gamma: Velocidad angular (rad/s)
    - gamma_dot: Aceleración angular (rad/s²)
    
    Parámetros físicos:
    - masa: Masa total actual del cohete (kg)
    - masa_cohete: Masa estructural del cohete sin combustible (kg)
    - beta: Ángulo de inclinación del empuje (rad)
    - diametro: Diámetro del cohete (m)
    - m_dot: Tasa de consumo de combustible (kg/s)
    - isp: Impulso específico (s)
    
    Parámetros de guiado:
    - h_0, h_1, h_2: Alturas de transición para el perfil de beta
    """
    
    def __init__(self, r_0, q_0, q_dot_0, theta_0, gamma_0, gamma_dot_0,
                 masa_cohete, masa_fuel, beta, diametro, m_dot, isp,
                 h_0, h_1, h_2):
        """
        Inicializa el cohete con condiciones iniciales y parámetros.
        
        Args:
            r_0 (float): Posición radial inicial (m)
            q_0 (float): Velocidad radial inicial (m/s)
            q_dot_0 (float): Aceleración radial inicial (m/s²)
            theta_0 (float): Posición angular inicial (rad)
            gamma_0 (float): Velocidad angular inicial (rad/s)
            gamma_dot_0 (float): Aceleración angular inicial (rad/s²)
            masa_cohete (float): Masa estructural sin combustible (kg)
            masa_fuel (float): Masa de combustible inicial (kg)
            beta (float): Ángulo de empuje inicial (rad)
            diametro (float): Diámetro del cohete (m)
            m_dot (float): Tasa de consumo de combustible inicial (kg/s)
            isp (float): Impulso específico (s)
            h_0 (float): Primera altura de transición (m)
            h_1 (float): Segunda altura de transición (m)
            h_2 (float): Tercera altura de transición (m)
        """
        # Estado actual
        self.r = r_0
        self.q = q_0
        self.q_dot = q_dot_0
        self.theta = theta_0
        self.gamma = gamma_0
        self.gamma_dot = gamma_dot_0
        self.masa = masa_cohete + masa_fuel
        
        # Parámetros físicos
        self.masa_cohete = masa_cohete
        self.beta = beta
        self.diametro = diametro
        self.m_dot = m_dot
        self.isp = isp
        
        # Parámetros de guiado
        self.h_0 = h_0
        self.h_1 = h_1
        self.h_2 = h_2

        # Historiales para análisis posterior
        self.r_hist = [r_0]
        self.q_hist = [q_0]
        self.q_dot_hist = [q_dot_0]
        self.theta_hist = [theta_0]
        self.gamma_hist = [gamma_0]
        self.gamma_dot_hist = [gamma_dot_0]
        self.masa_hist = [masa_cohete + masa_fuel]
        self.beta_hist = [beta]

    def empuje(self):
        """
        Calcula la fuerza de empuje del cohete.
        
        Usa self.m_dot (tasa de consumo actual) para calcular empuje.
        Si no hay combustible, m_dot=0 y empuje=0.
        
        Returns:
            float: Fuerza de empuje (N)
        """
        return self.isp * self.m_dot * G0

    def arrastre(self):
        """
        Calcula la fuerza de arrastre aerodinámico.
        
        La fuerza de arrastre depende de:
        - Coeficiente de arrastre (CD)
        - Densidad del aire (función de la altura)
        - Velocidad al cuadrado
        - Área frontal
        
        Returns:
            float: Fuerza de arrastre (N)
        """
        altura = self.r - R_E
        rho = calcular_densidad_aire(altura)
        v = calcular_velocidad(self.q, self.gamma, self.r)
        area = calcular_area_frontal_esfera(self.diametro / 2)
        return CD * 0.5 * rho * (v ** 2) * area

    def forward_euler(self, dt):
        """
        Realiza un paso de integración usando el método Forward Euler.
        
        NOTA: Actualiza automáticamente todos los historiales.
        
        Args:
            dt (float): Paso de tiempo (s)
            
        Returns:
            tuple: (r, q, theta, gamma) - Estado actualizado
        """
        tiempo_de_vuelo = dt * len(self.r_hist)
        
        # Actualizar tasa de consumo de combustible según el tiempo
        altura = self.r - R_E
        fuel_restante = self.masa - self.masa_cohete
        m_dot_cmd = calcular_mdot(tiempo_de_vuelo)
        
        # Limitar m_dot por combustible disponible
        if fuel_restante > 0:
            self.m_dot = min(m_dot_cmd, fuel_restante / dt)
        else:
            self.m_dot = 0.0
        
        # Consumir combustible
        self.masa = max(self.masa_cohete, self.masa - self.m_dot * dt)
        
        # Actualizar beta según configuración
        if BETA_ALTURA:
            self.beta = calcular_beta_altura(
                self.r - R_E, self.h_0, self.h_1, self.h_2
            )
        else:
            self.beta = calcular_beta_tiempo(tiempo_de_vuelo)

        # Calcular aceleraciones
        # Velocidades radial y tangencial
        v_radial = self.q
        v_tangencial = self.r * self.gamma
        v_total = calcular_velocidad(self.q, self.gamma, self.r)
        
        # Componentes del arrastre (proyección sobre ejes radial y tangencial)
        # El arrastre SIEMPRE se opone al movimiento
        D_total = self.arrastre()
        # IMPORTANTE: El signo del arrastre debe ser opuesto a la velocidad
        # Si v_radial > 0 (subiendo): drag frena → drag < 0
        # Si v_radial < 0 (cayendo): drag frena → drag > 0
        drag_radial_magnitude = D_total * (abs(v_radial) / max(1e-9, v_total))
        drag_radial = -math.copysign(drag_radial_magnitude, v_radial) if abs(v_radial) > 1e-9 else 0.0
        
        drag_tangencial_magnitude = D_total * (abs(v_tangencial) / max(1e-9, v_total))
        drag_tangencial = -math.copysign(drag_tangencial_magnitude, v_tangencial) if abs(v_tangencial) > 1e-9 else 0.0
        
        # Aceleración radial: incluye gravedad, empuje, arrastre y centrífuga
        self.q_dot = (
            - calcular_gravedad(self.r)
            + (self.empuje() * math.cos(self.beta)) / self.masa
            + drag_radial / self.masa  # Ahora drag_radial ya tiene el signo correcto
            + self.r * (self.gamma ** 2)
        )
        
        # Aceleración angular (ecuación: r·γ̇ + 2·q·γ = fuerzas_tangenciales)
        # De la ecuación: r·γ̇ + 2·q·γ = (T·sin(β) + D_t) / m
        # Ahora drag_tangencial ya tiene el signo correcto (opuesto al movimiento)
        # Despejando: γ̇ = [(T·sin(β) + D_t) / m - 2·q·γ] / r
        self.gamma_dot = (
            (self.empuje() * math.sin(self.beta)) / self.masa
            + drag_tangencial / self.masa
            - 2 * self.q * self.gamma
        ) / self.r

        # Integración Forward Euler
        self.gamma = self.gamma_dot * dt + self.gamma
        self.q = self.q_dot * dt + self.q
        self.theta = self.gamma * dt + self.theta
        self.r = self.q * dt + self.r

        # Actualizar historiales
        self.r_hist.append(self.r)
        self.q_hist.append(self.q)
        self.q_dot_hist.append(self.q_dot)
        self.theta_hist.append(self.theta)
        self.gamma_hist.append(self.gamma)
        self.gamma_dot_hist.append(self.gamma_dot)
        self.masa_hist.append(self.masa)
        self.beta_hist.append(self.beta)

        return (self.r, self.q, self.theta, self.gamma)

    def backward_euler(self, dt):
        """
        Realiza un paso de integración usando el método Backward Euler.
        
        Este método es más estable numéricamente que Forward Euler,
        especialmente para sistemas con fuerzas grandes o cambios rápidos.
        
        Implementación: Usa una iteración de punto fijo para aproximar
        la solución implícita, evaluando las fuerzas en el estado predicho.
        
        NOTA: Actualiza automáticamente todos los historiales.
        
        Args:
            dt (float): Paso de tiempo (s)
        """
        # 1) Actualizar tasa de consumo de combustible
        # IMPORTANTE: Ahora calcular_mdot usa TIEMPO en lugar de altura
        altura = self.r - R_E  # Mantener para beta y densidad
        tiempo_actual = len(self.r_hist) * dt  # Usar el dt correcto de la simulación
        fuel_restante = self.masa - self.masa_cohete
        m_dot_cmd = calcular_mdot(tiempo_actual)
        
        # Limitar m_dot por combustible disponible
        if fuel_restante > 0:
            self.m_dot = min(m_dot_cmd, fuel_restante / dt)
        else:
            self.m_dot = 0.0
    
        # Consumir combustible
        self.masa = max(self.masa_cohete, self.masa - self.m_dot * dt)
    
        # 2) Actualizar beta
        if BETA_ALTURA:
            self.beta = calcular_beta_altura(
                altura, self.h_0, self.h_1, self.h_2
            )
        else:
            tiempo_de_vuelo = dt * len(self.r_hist)
            self.beta = calcular_beta_tiempo(tiempo_de_vuelo)
        
        # 3) Calcular empuje
        T = self.empuje()
        
        # Log periódico del empuje (cada 100,000 iteraciones)
        if len(self.r_hist) % 100_000 == 1:
            print(f"Empuje: {T:.2f} N")
        
        # 4) Calcular componentes de velocidad y arrastre
        v_r = self.q
        v_t = self.r * self.gamma
        v = max(1e-9, math.hypot(v_r, v_t))
    
        rho = max(0.0, calcular_densidad_aire(altura))
        A = calcular_area_frontal_esfera(self.diametro / 2)
        D = 0.5 * CD * rho * (v ** 2) * A
        # El arrastre se opone al movimiento
        D_r_magnitude = D * (abs(v_r) / v)
        D_r = -math.copysign(D_r_magnitude, v_r) if abs(v_r) > 1e-9 else 0.0
        D_t_magnitude = D * (abs(v_t) / v)
        D_t = -math.copysign(D_t_magnitude, v_t) if abs(v_t) > 1e-9 else 0.0
    
        # 5) Integración Backward Euler (iterativo para convergencia)
        # Estimación inicial con Forward Euler
        q_new = self.q
        gamma_new = self.gamma
        r_new = self.r
        
        # Iterar 3 veces para convergencia del método implícito
        for _ in range(3):
            # Predecir nueva posición radial
            r_new = self.r + dt * q_new
            
            # Recalcular arrastre con nuevas velocidades
            v_r_new = q_new
            v_t_new = r_new * gamma_new
            v_new = max(1e-9, math.hypot(v_r_new, v_t_new))
            
            rho_new = max(0.0, calcular_densidad_aire(r_new - R_E))
            D_new = 0.5 * CD * rho_new * (v_new ** 2) * A
            D_r_new_magnitude = D_new * (abs(v_r_new) / v_new)
            D_r_new = -math.copysign(D_r_new_magnitude, v_r_new) if abs(v_r_new) > 1e-9 else 0.0
            D_t_new_magnitude = D_new * (abs(v_t_new) / v_new)
            D_t_new = -math.copysign(D_t_new_magnitude, v_t_new) if abs(v_t_new) > 1e-9 else 0.0
            
            # Aceleración radial (usando valores nuevos para implícito)
            q_dot_new = (
                (T * math.cos(self.beta) + D_r_new) / self.masa
                - MU / (r_new ** 2)
                + r_new * (gamma_new ** 2)  # Término centrífugo con gamma_new
            )
            q_new = self.q + dt * q_dot_new
            
            # Aceleración angular (usando valores nuevos)
            # De la ecuación: r·γ̇ + 2·q·γ = (T·sin(β) + D_t) / m
            # Ahora D_t ya tiene el signo correcto (opuesto a v_t)
            gamma_dot_new = (
                (T * math.sin(self.beta) + D_t_new) / self.masa
                - 2 * q_new * gamma_new  # Término de Coriolis con q_new y gamma_new
            ) / r_new
            gamma_new = self.gamma + dt * gamma_dot_new
        
        # Actualizar theta con gamma final
        theta_new = self.theta + dt * gamma_new

        # 6) Actualizar historiales
        self.r_hist.append(r_new)
        self.q_hist.append(q_new)
        self.q_dot_hist.append(q_dot_new)
        self.gamma_hist.append(gamma_new)
        self.gamma_dot_hist.append(gamma_dot_new)
        self.theta_hist.append(theta_new)
        self.masa_hist.append(self.masa)
        self.beta_hist.append(self.beta)
        
        # 7) Actualizar estado
        self.r = r_new
        self.q = q_new
        self.gamma = gamma_new
        self.theta = theta_new
        self.q_dot = q_dot_new
        self.gamma_dot = gamma_dot_new

    def simular(self, dt: float, t_max: float, usar_backward: bool = True,
                log_cada: int = 0):
        """
        Ejecuta la simulación completa hasta t_max.
        
        Criterios de parada:
        - Tiempo máximo alcanzado
        - Cohete colisiona con la Tierra (r <= R_E)
        - Valores numéricos inválidos (NaN/inf)
        
        Args:
            dt (float): Paso de tiempo (s)
            t_max (float): Tiempo máximo de simulación (s)
            usar_backward (bool): True para Backward Euler, False para Forward
            log_cada (int): Frecuencia de logging (0 para silenciar)
            
        Returns:
            dict: Resumen de la simulación con:
                - end_reason: Razón de finalización
                - iter: Número de iteraciones
                - t_final: Tiempo final (s)
                - h_final_m: Altura final (m)
                - theta_final: Ángulo final (rad)
        """
        # Seleccionar método de integración
        paso = self.backward_euler if usar_backward else self.forward_euler
        nombre_metodo = "Backward Euler" if usar_backward else "Forward Euler"
    
        t = 0.0
        iter_max = max(1, int(t_max / dt))
    
        # Log inicial
        if log_cada != 0:
            print(f"Simulando con dt = {dt} s usando {nombre_metodo}")
            print(
                f"Iter 0: altura = {max(0.0, self.r - R_E)/1000:.3f} km, "
                f"v_r = {self.q:.3f} m/s, omega = {self.gamma:.3e} rad/s, "
                f"masa = {self.masa:.0f} kg, beta = {self.beta:.3f} rad, "
                f"t = {t:.1f} s"
            )
    
        end_reason = "t_max"
        i_fin = 0
        flag_combustible_agotado = True

        for i in range(1, iter_max + 1):
            # 1) Manejar agotamiento de combustible
            if self.masa <= self.masa_cohete:
                self.masa = self.masa_cohete
                if flag_combustible_agotado:
                    altura_km = max(0.0, self.r - R_E) / 1000
                    print(f"*** COMBUSTIBLE AGOTADO en t={t:.1f}s, altura={altura_km:.1f}km ***")
                    flag_combustible_agotado = False
                self.m_dot = 0.0
    
            # 2) Ejecutar un paso del método de integración
            if usar_backward:
                paso(dt)  # backward_euler actualiza automáticamente
            else:
                # NOTA: forward_euler no actualiza historiales automáticamente
                # Habría que agregarlo si se usa forward_euler
                paso(dt)
    
            t += dt
            i_fin = i
    
            # 3) Criterios de parada
            # a) Colisión con la Tierra
            if self.r <= R_E:
                end_reason = "hit_ground"
                break
            
            # b) Valores numéricos inválidos
            if not (math.isfinite(self.r) and math.isfinite(self.q) and
                    math.isfinite(self.theta) and math.isfinite(self.gamma)):
                end_reason = "numerical_error"
                break
            
            # 4) Logging periódico
            if log_cada > 0 and (i % log_cada == 0):
                altura_km = max(0.0, self.r - R_E) / 1000.0
                print(
                    f"Iter {i}: altura = {altura_km:.3f} km, "
                    f"v_r = {self.q:.3f} m/s, omega = {self.gamma:.3e} rad/s, "
                    f"masa = {self.masa:.0f} kg, beta = {self.beta:.3f} rad, "
                    f"t = {t:.1f} s"
                )
    
            # 5) Corte por tiempo máximo
            if t >= t_max:
                end_reason = "t_max"
                break
            
        # Resumen final
        if log_cada != 0:
            altura_km = max(0.0, self.r - R_E) / 1000.0
            print(
                f"FIN: {end_reason} | iter: {i_fin} | t: {t:.1f} s | "
                f"h: {altura_km:.2f} km | theta: {self.theta:.4f} rad"
            )
    
        return {
            "end_reason": end_reason,
            "iter": i_fin,
            "t_final": t,
            "h_final_m": max(0.0, self.r - R_E),
            "theta_final": self.theta,
        }
