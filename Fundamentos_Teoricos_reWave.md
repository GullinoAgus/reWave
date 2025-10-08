# Fundamentos Teóricos de reWave

---

## 1. Introducción

El programa reWave está basado en el análisis de la efectividad de apantallamiento electromagnético (Shielding Effectiveness, SE) en sistemas multicapa. Utiliza el método de líneas de transmisión equivalentes para modelar la propagación de ondas electromagnéticas en medios estratificados, permitiendo el cálculo de los coeficientes de reflexión, transmisión y la SE total.

---

## 2. Modelo Físico

### 2.1. Incidencia de Ondas Electromagnéticas

Cuando una onda electromagnética incide sobre un sistema de capas, parte de la energía se refleja, parte se transmite y parte se absorbe. El análisis se realiza para dos polarizaciones:
- **TE (Transverse Electric):** El campo eléctrico es perpendicular al plano de incidencia.
- **TM (Transverse Magnetic):** El campo magnético es perpendicular al plano de incidencia.

### 2.2. Método de Líneas de Transmisión

Cada capa se modela como una línea de transmisión con parámetros característicos:
- **Impedancia característica (Z₀)**
- **Constante de propagación (γ)**

Las condiciones de contorno en cada interfaz permiten calcular los coeficientes de reflexión y transmisión.

---

## 3. Fórmulas Principales

### 3.1. Parámetros de Material

- **Permitividad relativa:**  
  $\varepsilon_r$
- **Permeabilidad relativa:**  
  $\mu_r$
- **Conductividad:**  
  $\sigma$
- **Permitividad imaginaria (modelo alternativo de pérdidas):**  
  $\varepsilon_i$

### 3.2. Espesor de Capa

- En milímetros: $d$ (m)
- En longitudes de onda: $d = n_\lambda \cdot \lambda$

### 3.3. Impedancia Característica y Constante de Propagación

Para cada capa, se calcula:

- **Impedancia característica (TE):**
  $$
  \eta_{11} = \eta_{01} \cdot \sec(\theta)
  $$
- **Impedancia característica (TM):**
  $$
  \eta_{11} = \eta_{01} \cdot \cos(\theta)
  $$
- **Constante de propagación:**
  $$
  \gamma_{11} = \gamma_{01} \cdot \cos(\theta)
  $$

Donde $\eta_{01}$ y $\gamma_{01}$ son los valores en incidencia normal, y $\theta$ es el ángulo de incidencia.

### 3.4. Efectividad de Blindaje (SE)

La SE se define como:
$$
SE = 20 \cdot \log_{10}\left|\frac{E_i}{E_t}\right| \quad [dB]
$$
Donde $E_i$ es el campo incidente y $E_t$ el transmitido.

Para sistemas de una sola capa, se descompone en:
$$
SE = R + A + M
$$
- **R:** Pérdidas por reflexión
- **A:** Pérdidas por absorción
- **M:** Corrección por múltiples reflexiones

#### Cálculo de Componentes (según Celozzi & Araneo):
- **Reflexión:**
  $$
  R = \left|\frac{(Z_1 + Z_2)(Z_2 + Z_3)}{4 Z_2 Z_3}\right|
  $$
- **Absorción:**
  $$
  A = \left|e^{j k_{x2} d}\right| = e^{-\text{Im}(k_{x2}) d}
  $$
- **Múltiples reflexiones:**
  $$
  M = \left|1 - \frac{(Z_2 - Z_1)(Z_2 - Z_3)}{(Z_2 + Z_1)(Z_2 + Z_3)} e^{-2 j k_{x2} d}\right|
  $$

Donde:
- $Z_1$, $Z_2$, $Z_3$: Impedancias características de cada medio
- $k_{x2}$: Componente normal del número de onda en la capa intermedia
- $d$: Espesor de la capa

### 3.5. Coeficientes de Reflexión y Transmisión

- **Reflexión:**
  $$
  \Gamma = \frac{Z_l - Z_0}{Z_l + Z_0}
  $$
- **Transmisión:**
  $$
  \tau = \frac{2 Z_l}{Z_l + Z_0}
  $$

---

## 4. Algoritmo de Simulación

El programa construye una red de líneas de transmisión equivalente a partir de las capas definidas por el usuario. Para cada frecuencia y ángulo de incidencia:
1. Calcula los parámetros de cada capa
2. Resuelve las condiciones de contorno
3. Obtiene los coeficientes de reflexión y transmisión
4. Calcula la SE total y sus componentes

---

## 5. Referencias Bibliográficas

- Bronwell, A. "Transmission-Line Analogies of Plane Electromagnetic-Wave Reflections." IEEE, Vol. 32, no. 4, Apr. 1944, pp. 233–241.
- Salvatore Celozzi, Rodolfo Araneo, "Electromagnetic Shielding", Wiley-IEEE Press (2008). (Ver PDF en Documentacion/)

---

**Fecha:** Octubre 2025  
**Versión:** 1.0
