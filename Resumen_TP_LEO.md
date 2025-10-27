# 🛰️ Resumen Completo del Trabajo Práctico: Perfil de Vuelo de un Cohete a LEO

## 🎯 Objetivo General

Diseñar y simular el **perfil de vuelo de un cohete de una etapa** hasta alcanzar una **órbita baja (LEO)** a 200 km de altura.  
Aplicar los principios de **dinámica orbital y de vuelo**, implementando un **solver numérico (Forward y Backward Euler)** que resuelva las ecuaciones diferenciales del movimiento considerando **gravedad, empuje, y arrastre aerodinámico**.

---

## 1️⃣ Fundamentos Teóricos

### 1.1 Movimiento en Coordenadas Cilíndricas

Para describir el movimiento orbital o de un cohete, se usa un sistema polar (r, θ):

\[
\vec{p} = r \hat{e_r}
\]
\[
\vec{v} = \dot{r}\hat{e_r} + r\dot{\theta}\hat{e_\theta}
\]
\[
\vec{a} = (\ddot{r} - r\dot{\theta}^2)\hat{e_r} + (r\ddot{\theta} + 2\dot{r}\dot{\theta})\hat{e_\theta}
\]

- \( \hat{e_r} \): dirección radial  
- \( \hat{e_\theta} \): dirección tangencial  
- \( r \): distancia al centro de la Tierra  
- \( \theta \): ángulo respecto al eje de referencia  

---

### 1.2 Ley de Gravitación Universal

\[
F_g = -\frac{GMm}{r^2}
\]
\[
g = \frac{GM}{r^2}
\]

Constantes:
- \( G = 6.674\times10^{-11} \, \text{N·m²/kg²} \)
- \( M_T = 5.972\times10^{24} \, \text{kg} \)
- \( R_T = 6.371\times10^6 \, \text{m} \)

---

### 1.3 Tipos de Órbita

| Tipo | Altura (km) | Características |
|------|-------------|-----------------|
| **LEO** | 200–2 000 | Observación terrestre, baja latencia |
| **MEO** | 2 000–35 786 | GPS, Galileo, navegación |
| **GEO** | ≈ 35 786 | Estacionaria sobre el ecuador |
| **HEO** | Variable | Elípticas, misiones científicas |

---

### 1.4 Velocidades Características

- **Velocidad orbital (LEO):**
  \[
  v = \sqrt{\frac{GM}{R_T + h}}
  \]
  Para \(h=200 \text{km}\), \(v≈7.8 \text{km/s}\).

- **Velocidad de escape:**
  \[
  v_e = \sqrt{\frac{2GM}{R_T}} ≈ 11.2 \text{km/s}
  \]

---

### 1.5 Fuerzas Sobre el Cohete

**1. Gravedad:**
\[
\vec{F_g} = -\frac{GMm}{r^2}\hat{e_r}
\]

**2. Empuje (Thrust):**
\[
\vec{T} = T(\cos\beta \, \hat{e_r} + \sin\beta \, \hat{e_\theta})
\]

**3. Arrastre (Drag):**
\[
D = \frac{1}{2} C_D \rho v^2 A
\]
\[
\vec{D} = -D \frac{\vec{v}}{|\vec{v}|}
\]

---

### 1.6 Ecuación del Cohete (Tsiolkovsky)

\[
m \frac{dv}{dt} = -v_e \frac{dm}{dt}
\]
\[
\Delta v = v_e \ln\frac{m_0}{m_f}
\]

donde:
- \(v_e = I_{sp} g_0\)
- \(I_{sp}\): impulso específico (s)
- \(m_0\), \(m_f\): masa inicial y final

---

## 2️⃣ Ecuaciones de Gobierno del Sistema

Variables de estado:
\[
[r, \dot{r}, \theta, \dot{\theta}, m]
\]

### Sistema Completo con Empuje y Drag:

\[
\begin{cases}
\dot{r} = q \\
\dot{q} = r\gamma^2 - \frac{GM}{r^2} - \frac{C_D\rho v^2 A}{2m} + \frac{I_{sp}\dot{m} g_0 \cos\beta}{m} \\
r\dot{\gamma} + 2q\gamma = -\frac{C_D\rho v^2 A r}{2m} + \frac{I_{sp}\dot{m} g_0 \sin\beta}{m} \\
\dot{\theta} = \gamma \\
\dot{m} = -\dot{m}_p(t)
\end{cases}
\]

Sin empuje ni arrastre:
\[
\begin{cases}
\dot{r} = q \\
\dot{q} = r\gamma^2 - \frac{GM}{r^2} \\
r\dot{\gamma} + 2q\gamma = 0
\end{cases}
\]

---

## 3️⃣ Métodos Numéricos de Integración

### 3.1 Forward Euler

\[
x_{n+1} = x_n + \Delta t \, f(x_n, t_n)
\]

Método explícito, simple pero sensible a \(\Delta t\).

---

### 3.2 Backward Euler

\[
x_{n+1} = x_n + \Delta t \, f(x_{n+1}, t_{n+1})
\]

Método implícito, estable y adecuado para órbitas largas. Requiere resolver un sistema no lineal (p. ej. Newton-Raphson).

---

### 3.3 Newton-Raphson (Sistemas No Lineales)

\[
\mathbf{x}_{k+1} = \mathbf{x}_k - J^{-1}(\mathbf{x}_k)\mathbf{f}(\mathbf{x}_k)
\]

---

## 4️⃣ Casos de Prueba

| Caso | Descripción | Propósito |
|------|--------------|-----------|
| **Tiro con mortero** | Parabólico sin drag ni empuje | Validar solver |
| **Órbita LEO (200 km)** | Movimiento circular estable | Verificar equilibrio |
| **Órbita GEO (35 786 km)** | Estacionaria | Validar relación radio-período |
| **Velocidad de escape** | \(v_e = \sqrt{2GM/R_T}\) | Verificar energía total |

---

## 5️⃣ Parámetros del Cohete

- Masa en seco: 20,000 kg  
- Impulso específico: 300 s  
- Diámetro: 4 m → Área = 12.57 m²  
- Altura: 40 m  
- Órbita objetivo: h = 200 km  
- \( R_T = 6.371\times10^6 \text{ m} \)  
- \( G = 6.674\times10^{-11} \)  

---

## 6️⃣ Variables a Graficar

1. r(t): radio terrestre  
2. θ(t): ángulo orbital  
3. v_r(t): velocidad radial  
4. v_θ(t): velocidad angular  
5. a_r(t): aceleración radial  
6. a_θ(t): aceleración angular  
7. m(t): masa instantánea  
8. β(t): dirección del empuje  
9. Trayectoria esperada en (r, θ)

---

## 7️⃣ Estrategia de Simulación

1. **Inicialización:**  
   r₀ = R_T, θ₀ = 0, q₀ = 0, γ₀ = 0, m₀ = m_dry + m_fuel

2. **Leyes de Control:**  
   - Consumo de masa: \(\dot{m} = \text{constante}\)  
   - Dirección de empuje: β(t) definida según perfil de vuelo

3. **Integración (Euler Forward o Backward):**  
   Calcular r, q, γ, θ, m en cada paso Δt.  
   Evaluar estabilidad y conservar energía.

---

## 8️⃣ Resultados Esperados

- LEO: r = R_T + 200 km, v ≈ 7.8 km/s  
- GEO: r = 42,240 km, T ≈ 24 h  
- Escape: v ≈ 11.2 km/s  

---

## ✅ Conclusión

Este trabajo combina:
- **Dinámica orbital realista** (gravedad, empuje, drag)
- **Métodos numéricos estables** (Forward y Backward Euler)
- **Validación con escenarios límite**  
Permite desarrollar una simulación física precisa de un cohete en ascenso a LEO.
