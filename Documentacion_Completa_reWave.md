# Manual de Usuario y Documentación Técnica - reWave
**Autores:** Gonzalo Linares, Agustin Gullino  
**Profesor:** Patricio Marco


## 1. Manual de Usuario

### 1.1. Pantalla de Inicio

La pantalla principal de reWave permite acceder a todas las funcionalidades de simulación y configuración de capas.

![Pantalla de inicio](images/inicio.png)

---

### 1.2. Panel de Capas

Este panel permite agregar, editar, duplicar, deshabilitar y eliminar capas. Cada capa representa un material en el sistema multicapa.

![Panel de capas](images/panel_capas.png)

- **μr, εr, σ/εi**: Parámetros electromagnéticos de cada capa.
- **Espesor (d)**: Puede elegirse en milímetros o en longitudes de onda del propio medio.
- **Nombre**: Identificador de la capa.
- **Controles**: Mover, duplicar, eliminar, habilitar/deshabilitar.

#### Ejemplo de selección de espesor:

![Elegir espesor](images/panel_capas_choosing_d.png)

#### Ejemplo de selección de modelo de pérdidas:

![Elegir pérdidas](images/capa_overview_choosing_loss.png)

#### Capa deshabilitada:

![Capa deshabilitada](images/capa_overview_disabled.png)

---

### 1.3. Visualización de Capas

Vista general de las capas agregadas y su orden en el sistema.

![Visualización de capas](images/capa_overview.png)

#### Ejemplo de sistema con capa de incidencia y transmisión:

![Incidencia y transmisión](images/capa_inc_trans_overview.png)

---

### 1.4. Configuración de Simulación

Panel para definir el tipo de barrido, frecuencia, ángulo de incidencia y polarización.

![Panel de configuración](images/sim_config.png)

#### Desplegables de configuración:

![Desplegable de configuración](images/sim_config_desplegable.png)
![Desplegable de polarización](images/sim_config_desplegable_pol.png)

---

### 1.5. Opciones de Gráficos

Herramientas para cambiar escala de ejes, estilo y guardar gráficos.

![Opciones de gráfico](images/plot_options.png)
![Cambiar escala de eje](images/plot_change_axis_scale.png)

---

### 1.6. Ejemplo de Tutorial Paso a Paso

A continuación se muestran imágenes de un tutorial guiado para configurar y simular un sistema multicapa:

| Paso | Imagen |
|------|--------|
| 1 | ![](images/tutorial_1.png) |
| 2 | ![](images/tutorial_2.png) |
| 3 | ![](images/tutorial_3.png) |
| 4 | ![](images/tutorial_4.png) |
| 5 | ![](images/tutorial_5.png) |
| 6 | ![](images/tutorial_6.png) |
| 7 | ![](images/tutorial_7.png) |
| 8 | ![](images/tutorial_8.png) |
| 9 | ![](images/tutorial_9.png) |
| 10 | ![](images/tutorial_10.png) |

Cada paso muestra la evolución de la configuración y el análisis.

---

### 1.7. Resultados de Simulación

#### Barrido en Frecuencia

- **Coeficientes de transmisión y reflexión:**

![Coeficientes barrido frecuencia](images/barrido_en_freq_coef_tx_refl.png)

- **Potencias de Poynting:**

![Poynting barrido frecuencia](images/barrido_en_freq_poyting.png)

- **Efectividad de blindaje (SE):**

![SE barrido frecuencia](images/barrido_en_freq_se.png)

#### Barrido en Ángulo

- **Coeficientes de transmisión y reflexión:**

![Coeficientes barrido ángulo](images/barrido_en_angulo_coef_tx_refl.png)

- **Potencias de Poynting:**

![Poynting barrido ángulo](images/barrido_en_angulo_poyting.png)

- **SE en escala lineal y semilog:**

![SE lineal ángulo](images/barrido_en_angulo_se_linear.png)
![SE semilog ángulo](images/barrido_en_angulo_se_semilog.png)

---

## 2. Documentación Técnica

### 2.1. Estructura del Proyecto

- **main.py**: Punto de entrada de la aplicación.
- **Windows/app.py**: Lógica principal de la interfaz y simulación.
- **UI/Main_UI.py, Main.ui**: Definición visual y lógica de la interfaz gráfica.
- **Utils/**: Módulos de cálculo físico y visualización.
    - **Medium.py**: Modelo de material/capa.
    - **TLNetwork.py**: Algoritmo de red de líneas de transmisión.
    - **plotWidget.py**: Gráficos y visualización.
- **images/**: Recursos gráficos y tutoriales.
- **Documentacion/**: Material teórico de referencia.

### 2.2. Algoritmo de Simulación

La simulación se basa en el método de líneas de transmisión equivalentes para calcular la propagación de ondas electromagnéticas en sistemas multicapa. Se consideran los parámetros físicos de cada capa y se resuelven las ecuaciones de contorno para obtener los coeficientes de reflexión, transmisión y la efectividad de blindaje (SE).

#### Parámetros de cada capa:
- **μr**: Permeabilidad relativa
- **εr**: Permitividad relativa
- **σ**: Conductividad
- **εi**: Permitividad imaginaria (modelo alternativo de pérdidas)
- **Espesor**: En mm o longitudes de onda

#### Tipos de simulación:
- **Barrido de frecuencia**: SE y coeficientes en función de la frecuencia
- **Barrido de ángulo**: SE y coeficientes en función del ángulo de incidencia
- **Polarización**: TE y TM

#### Resultados:
- **Coeficientes de reflexión y transmisión**
- **Potencias reflejada, transmitida y absorbida**
- **Efectividad de blindaje (SE)**

### 2.3. Referencia Teórica

El fundamento teórico está basado en el libro:

- Salvatore Celozzi, Rodolfo Araneo, "Electromagnetic Shielding", Wiley-IEEE Press (2008). [Ver PDF en Documentacion/]

El método implementado modela la incidencia oblicua y normal de ondas electromagnéticas como un circuito de líneas de transmisión, permitiendo el análisis detallado de sistemas multicapa y la descomposición de la SE en componentes de reflexión, absorción y múltiples reflexiones.

### 2.4. Ejemplo de Código (Python)

```python
# Ejemplo de creación de una capa
from Utils.Medium import Medium
capa = Medium(er=2.2, ur=1, sigma=0, width=0.005)

# Ejemplo de simulación de red multicapa
from Utils.TLNetwork import TLineNetwork
red = TLineNetwork([capa1, capa2, capa3], theta_i=0)
se_total = red.get_se(freq=1e9, pol='TE')
```

---

## 3. Contacto y Soporte

- **Repositorio:** https://github.com/GullinoAgus/reWave
- **Documentación teórica:** Ver PDF en `Documentacion/`
- **Reportar errores:** Usar Issues en GitHub

---

**Fecha:** Octubre 2025  
**Versión:** 1.0
