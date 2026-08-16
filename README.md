# ⚡ Visualizador de funciones con trayectorias

Una aplicación de escritorio interactiva y de alto rendimiento desarrollada en Python para el análisis y visualización de cinemática paramétrica en 2D. 

A diferencia de las graficadoras tradicionales, esta herramienta no utiliza aproximaciones numéricas básicas; integra un motor analítico simbólico para calcular derivadas exactas en tiempo real, permitiendo observar el comportamiento preciso de los vectores de velocidad y aceleración a lo largo de cualquier curva paramétrica.
---------------------------------------------------------------------------------------------------------------------------------------
# Características principales

*Motor analítico simbólico: Utiliza SymPy para procesar ecuaciones ingresadas por el usuario y calcular las derivadas analíticas exactas ($v$ y $a$) sobre la marcha.
*Animación fluida a 60 FPS: Reproducción cinemática controlable mediante *sliders* de tiempo, renderizada con un motor optimizado en Matplotlib.
*Telemetría HUD flotante: Visualización en pantalla de datos críticos en tiempo real, incluyendo posición $(x, y)$, tiempo $(t)$, y magnitudes de los vectores de velocidad $(|v|)$ y aceleración $(|a|)$.
*Estética neón futurista: Interfaz oscura de alto contraste (*Dark Mode*) con efectos de resplandor (*glow*) dinámicos para diferenciar claramente las capas de información.
*Colección de presets matemáticos: Incluye curvas paramétricas clásicas listas para analizar (Espiral de Arquímedes, Figura de Lissajous, Curva Mariposa, entre otras).
---------------------------------------------------------------------------------------------------------------------------------------
# Stack 

El proyecto está construido íntegramente en Python, combinando librerías científicas y de interfaces gráficas:

* Tkinter & ttk:** Arquitectura de la Interfaz Gráfica de Usuario (GUI) y controles de estado.
* Matplotlib:** Motor de renderizado vectorial, capas espaciales (Quivers) y sistema de animación *backend*.
* SymPy:** Ecosistema de matemáticas simbólicas y cálculo diferencial.
* NumPy:** Generación de mallas de tiempo y evaluación rápida de matrices numéricas (Lambdify).
---------------------------------------------------------------------------------------------------------------------------------------
# Requisitos e instalación

*Asegúrate de tener instalado Python 3.x. Para ejecutar el visualizador, necesitas instalar las dependencias científicas requeridas. 

*Instala los paquetes necesarios a través de pip:

Bash
pip install numpy sympy matplotlib
---------------------------------------------------------------------------------------------------------------------------------------

*Controles de la interfaz:
Ecuaciones paramétricas: Ingresa tus funciones x(t) y y(t) utilizando notación estándar de Python (ej. t * cos(t) o sin(3*t)).

Rango de tiempo: Define el intervalo evaluable estableciendo t min y t max.

Capas (layers):

Alterna entre una relación de aspecto 1:1 real o un auto-escalado.

Activa/desactiva la visibilidad de los vectores de velocidad y aceleración.

Activa el HUD para ver la telemetría métrica en la esquina superior.

Reproducción: usa el botón de reproducir animación o desplaza el slider manualmente para analizar instantes específicos de la trayectoria.
