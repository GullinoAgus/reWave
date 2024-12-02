# Instalación

Para descargar el instalador acceder al siguiente
[link](https://github.com/GullinoAgus/reWave/releases/tag/release) y
seleccionar la opción que dice `reWave.Installer.exe`. Una vez
descargado hacer doble clic y completar el proceso de instalación.

Acceso al código fuente: <https://github.com/GullinoAgus/reWave>

# Manual de uso

En la siguiente imagen se muestra la pantalla principal:

<figure id="fig:mainscreen">
<img src="/images/PantallaPrincipal.png" style="width:80.0%" />
<figcaption>Pantalla principal de la aplicación.</figcaption>
</figure>

## Características de las capas:

<figure id="fig:capas_panel">
<img src="/images/panel_add_capas.png" style="width:50.0%" />
<figcaption>Panel de agregado de capas.</figcaption>
</figure>

Desde esta pantalla se pueden colocar los parámetros de las capas en el
apartado "Añadir capa" y luego presionando añadir esta aparecerá en al
zona de visualización. De esta forma se pueden añadir la cantidad de
capas deseadas. A continuación un ejemplo de la visualización:

<figure id="fig:visualizacion">
<img src="/images/ejemplo_visualizacion.png" style="width:75.0%" />
<figcaption>Ejemplo de visualización de múltiples capas.</figcaption>
</figure>

-   ****μ**<sub>**r**</sub>**: Permeabilidad magnética relativa del
    medio.

-   ****ϵ**<sub>**r**</sub>**: Permitividad eléctrica relativa del
    medio.

-   ****σ****: Conductividad del medio.

-   **Espesor**: Espesor de la capa. La unidad puede seleccionarse como
    múltiplos de longitudes de onda (calculadas con la propagación en la
    capa) o mm.

-   **Nombre**: Nombre identificativo para la capa.

En la etapa de visualización se pueden modificar los parámetros de las
capas o intercambiarlas con las vecinas. La primera y ultima capa son
consideradas el medio de incidencia y el medio al cual se transmite la
onda, respectivamente. Esto se ve reflejado en el texto presente que
indica "Incidencia", "Intermedio" o "Transmisión".

## Configuración de la simulación:

<figure id="fig:sim_conf_panel_sweep">
<figure id="fig:sim_conf_panel_no_sweep">
<img src="/images/sim_config_freq.png" />
<figcaption>Panel de configuración de simulación en barrido de
frecuencia.</figcaption>
</figure>
<figure id="fig:sim_conf_panel_sweep">
<img src="/images/sim_config_angle.png" />
<figcaption>Panel de configuración de simulación en barrido de
angulo.</figcaption>
</figure>
<figcaption>Panel de configuración de simulación en barrido de
angulo.</figcaption>
</figure>

-   **Barrido**: Por default se realiza un barrido de frecuencia, pero
    puede seleccionarse el barrido de angulo y se realizara desde 0º a
    90º.

-   **Frecuencia**: En caso de barrido en frecuencia se puede
    seleccionar el rango con una resolucion minima de 1MHz. Para el caso
    de barrido en angulo se selecciona la frecuencia a la cual se
    realizara este.

-   **Incidencia**: Define el angulo de incidencia para el barrido en
    frecuencia.

-   **Polarización**: TM o TE.

-   **Periodos de capas**: Se puede seleccionar la cantidad de
    repeticiones periódicas de capas intermedias. Por ejemplo, si se
    forma un sistema de 5 capas intermedios y este valor es de 3, el
    sistema final estará compuesto de 15 capas intermedias donde se
    encuentran repetidas 2 veces las primeras 5.

## Resultados

Al completar la configuración del sistema se puede presionar el botón de
calcular. Esto llevara a la ventana de resultados y el formato de esta
dependerá de la clase de barrido.

<figure>
<figure>
<img src="/images/res_barr_freq.png" style="width:100.0%" />
<figcaption>Vista de resultados para barrido de frecuencia.</figcaption>
</figure>
<figure>
<img src="/images/res_barr_angle.png" style="width:96.0%" />
<figcaption>Vista de Resultados para barrido de angulo.</figcaption>
</figure>
<figcaption>Vista de Resultados para barrido de angulo.</figcaption>
</figure>

-   **Frec. de evaluación**: Frecuencia a la cual se evaluaron los
    parámetros de seleccionar y transaccionan. Es la menor frecuencia
    representada en el gráfico

-   **Coef. de reflexión y transmisión**: Coeficientes de reflexión y
    transmisión para el vector de Poynting en la frecuencia de
    evaluación.

-   **Graficos**: Resultado del barrido en frecuencia o en angulo según
    corresponda. Se puede cliquear en la curva para obtener el valor del
    punto como se ve en la primera figura.

-   **Barra de herramientas del gráfico**: Herramienta de home, paneo,
    zoom, configuración de estilo, configuración de ejes, guardado de la
    figura.

# Marco teórico

Para desarrollar esta herramienta se consulto . En este trabajo se
propone un método de modelado de la física de incidencia oblicua como un
circuito serie de lineas de transmisión. En primer lugar se demuestra la
equivalencia entre incidencia normal y lineas de transmisión, lo cual es
un hecho simple de ver si se observan las ecuaciones básicas de ambos
casos. El problema surge con incidencia oblicua. El procedimiento de
modelado para la incidencia oblicua comienza por la interpretación la
onda plana como un frente de onda no uniforme. Esto permite descomponer
la onda en la propagación perpendicular y paralela a la superficie. Para
el siguiente desarrollo se tomaran las figuras de .

## Onda TE

<figure>
<img src="/images/incidencia_TE.png" style="width:50.0%" />
</figure>

En base a este gráfico se puede describir la onda incidente (primada) y
reflejada (doble primada) como:

E’\_z=E’\_0\*e^\_01\*(x\*()-y\*())  
E”\_z=E”\_0\*e^-\_01\*(x\*()+y\*())

De esta forma el campo resultante en la interfaz es:

E_z=\*e^-\_01\*y\*()

Con esta expresión se puede obtener el campo magnético en la interfaz
dividiendo por la impedancia característica del medio y ajustando el
signo de la componente reflejada(corrección por convención):

H=1/\_01\*e^-\_01\*y\*()

En este caso, la componente *y* del campo H es la que aporta a la
incidencia de la onda TEM perpendicular a la superficie, por lo que
nuestro interés se centra en el cociente
*E*<sub>*z*</sub>/*H*<sub>*y*</sub> que representara la impedancia
equivalente del medio para este angulo de incidencia. Con esto se pueden
obtener las expresiones para las nuevas constantes del medio 1(las de
subíndice 11):

H_y = ()\*H = ()/\_01 \* E_z  
\_11 = \_01 \* ()  
\_11 = \_01 \* ()  
\_term = E(0)/H_y(0)

Esa ultima ecuación representa la impedancia de terminación de la linea
de transmisión equivalente siendo el cociente entre el campo eléctrico y
magnético en la interfaz, denotado por el (0). Con esto ultimo se pueden
reescribir los campos utilizando las expresiones obtenidas evaluando en
la interfaz:

E’\_0=\*(1+) E”\_0=\*(1-)  

Con esto se puede escribir los campos, que luego de reemplazar las
exponenciales por equivalencias hiperbólicas se obtiene:

E_z = E(0) \* \*e^-\_01\*y\*()  
H_y = E(0)/\_term \* \*e^-\_01\*y\*()

En estas ecuaciones se ve la clara similitud con las ecuaciones de la
tensión y corriente a lo largo de una linea de transmisión, salvando la
exponencial en *y* representando el cambio de fase a lo largo de ese
eje. Nótese ademas la dependencia con el angulo de incidencia.

Hasta aquí se obtuvieron las características para el medio de
incidencia. Para el medio de transmisión se realiza un análisis de
condiciones de contorno teniendo en cuenta que ambos campos
*E*<sub>*z*</sub> y *H*<sub>*y*</sub> son tangenciales a la superficie,
así obteniendo los campos transmitidos(triple primada):

E”’\_z=E(0)\*e^-\_02\*(-x\*(\_t)+y\*(\_t))  
H”’\_y=E(0)/\_02\*(\_t)\*e^-\_02\*(-x\*(\_t)+y\*(\_t))  

De aquí se pueden reemplazar las igualdades:

\_22 = \_02 \* (\_t)  
\_22 = \_02 \* (\_t)  

Obteniendo:

E”’\_z=E(0)\*e^\_22\*xe^-\_02y\*(\_t)  
H”’\_y=E(0)/\_02\*e^\_22\*xe^-\_22y\*(\_t)  

Evaluando en la interfaz y utilizando las condiciones de contorno se
puede hacer el cociente y obtener
*η*<sub>*t**e**r**m*</sub> = *Z*<sub>22</sub>, terminando así el modelo.

Con esto se puede obtener el coeficiente de reflexion:

\_12 =

## Onda TM

Analogo a lo anterior se puede obtener las componentes que componen al
frente de onda con incidencia normal:

H_z=\*e^-\_01\*y\*()  
E_y=\_01\*()\*e^-\_01\*y\*()

Si se toman las siguientes ecuaciones:

\_11 = \_01()  
\_11 = \_01()  
\_term = E_y(0)/H(0)

Con esto se obtienen las ecuaciones de los campos:

E_y = E_y(0) \* \*e^-\_01\*y\*()  
H_z = E_y(0)/\_term \* \*e^-\_01\*y\*()

De forma equivalente se obtienen las ecuaciones en el medio 2:

E”’\_y=E_y(0)\*e^\_22\*xe^-\_02y\*(\_t)  
H”’\_z=E_y(0)/\_02\*e^\_22\*xe^-\_22y\*(\_t)  
\_22 = \_02 \* (\_t)  
\_22 = \_02 \* (\_t)  

Con esto se puede obtener *η*<sub>*t**e**r**m*</sub> = *Z*<sub>22</sub>,
terminando así el modelo. Y nuevamente el coeficiente de reflexión es el
mismo que en el caso anterior.

Se puede demostrar que con estas expresiones se alcanzan las ecuaciones
de Fresnell de forma trivial desde la expresión del coeficiente de
reflexión.
