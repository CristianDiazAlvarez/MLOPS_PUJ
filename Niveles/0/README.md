### Punto de partida

- Existe un contexto de negocio en donde el uso de inteligencia artificial, puntualmente Machine Learning (ML) tiene un valor agregado. 
- El estado del arte en el tipo de problema objetivo, presenta opciones que tienen potencial para ser usados.
- Se decidió invertir en la construcción de un modelo de Machine Learning

# Nivel 0
El nivel cero por lo general es el primer paso de un equipo nuevo, quizás programadores que buscan incursionar en IA o ingenieros/científicos de datos. En este punto hay un mapa que, incluye recolección y procesamiento de datos, selección y entrenamiento de modelos, finalizando con una puesta en producción.

El primer paso es la recolección y etiquetado de datos, para este punto se asume la información ya está disponible.
Un equipo buscará probar los modelos disponibles en el estado del arte para la problemática de su contexto, para esto lo más común es usar las máquinas de trabajo en donde se instalaran las dependencias necesarias y se realizarán pruebas, hasta encontrar cual es el mejor modelo. Este proceso se repetirá hasta que el desempeño del modelo sea suficientemente bueno. En este punto se buscará integrar este modelo en el entorno donde aporta valor.

Este último elemento es lo que se considera llevar a producción un modelo. Esto puede ser desde, entregar un notebook a un gerente apasionado por TI para que de soporte a la toma de decisiones. Crear un sitio web el cual presenta los resultados del modelo o integrarlo como parte de un sistema más completo.

El escenario más real es que un modelo de machine learning no es el centro del mundo, solo es una funcionalidad más de un sistema, por lo tanto, se requiere que esté disponible para ser usado bajo petición. Más adelante en este curso se entenderá con más detalle, algunos ejemplos y argumentos para la toma de decisiones de como desplegar un modelo según requerimientos o condiciones específicas.

## Entrenamiento de modelo

Con el objetivo claro de entrenar un modelo de machine learning y teniendo un conjunto de datos iniciales es posible plantear un flujo de entrenamiento, si bien el proceso de desarrollo posiblemente se realice en un notebook que llevará al mejor modelo, al final se desea llegar a un flujo concreto de entrenamiento, posiblemente dividido en dos etapas, preparación de datos y creación de modelo.

![basic train flow](img/lvl0_train.svg)

Es claro que cada uno de de estos elementos contiene multiples procesos internos, este etapa no se enfoca en entregar el como realizar el mejor entrenamiento de datos ni creación de modelo, sin embargo se muestra de manera general lás etapas más comunes que se incluyen en este proceso. Si bien en clases posteriores se presentarán elemento clave, en el nivel cero no se ven aplicadas estás practicas al nivel que se entregarán.

Realizando un enfoque sobre las etapas de preparación de datos y creación de modelo se obtiene la siguiente imagen, la preparación de datos se muestra en 6 pasos:
- Carga
- Limpieza
- Transformación
- Validación
- Ingeniería de Características
- División

Por otro lado, la creación de modelo en 3 pasos:
- Construcción
- Entrenamiento
- Validación

Es importante aclarar que estos pasos son solo una generalización típica en estos procesos,  no una receta o norma a cumplir.

![detalle de entrenamiento](img/lvl0_train_detail.svg)

Si bien en este punto se cumple el objetivo de tener un modelo ajustado a las necesidades de unos datos iniciales, aún existe solo en la máquina del desarrollador.

## Despliegue a producción


A este punto es importante replicar el ambiente de trabajo del desarrollador para poder utilizar el modelo. Esto trae uno de los problemas más comunes en el desarrollo de software tradicional **"En mi máquina si funciona"**.

#### Contenedores

Como solución a esta problemática existen los contenedores. Un contenedor es una unidad estándar de software que empaqueta el código y todas sus dependencias para que la aplicación se ejecute de manera rápida y confiable de un entorno informático a otro.

Una imagen de contenedor de Docker es un paquete de software ligero, independiente y ejecutable que incluye todo lo necesario para ejecutar una aplicación: código, tiempo de ejecución, herramientas del sistema, bibliotecas del sistema y configuración.

Los contenedores y las máquinas virtuales tienen beneficios similares de asignación y aislamiento de recursos, pero funcionan de manera diferente porque los contenedores virtualizan el sistema operativo en lugar del hardware. Los contenedores son más portátiles y eficientes.

[Cómo instalar y usar Docker en Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)

El uso de los contenedores permite empaquetar y distribuir el código desarrollado, sin embargo, a este punto este código no sabe comunicarse con los sistemas que requieren la respuesta que el modelo entrega, para esto una de las soluciones más común es construir una API, interfaz de programación de aplicaciones.

[Docker](Docker/README.md)

#### API

En el contexto de las API, la palabra aplicación se refiere a cualquier software con una función distinta. La arquitectura de las API suele explicarse en términos de cliente y servidor. La aplicación que envía la solicitud se llama cliente, y la que envía la respuesta se llama servidor.

- API REST
Estas son las API más populares y flexibles que se encuentran en la web actualmente. El cliente envía las solicitudes al servidor como datos. El servidor utiliza esta entrada del cliente para iniciar funciones internas y devuelve los datos de salida al cliente. 

Uno de los framework más utilizados recientemente para la creación de API es [Documentación Oficial FastAPI](https://fastapi.tiangolo.com)


Al usar FastAPI es posible crear rápidamente una API que permita usar el modelo entrenado, está API recibirá los datos de entrada como petición, está deberá realizar inferencia con modelo entrenado y responder el resultado de inferencia.

El proceso completo de entrenamiento y puesta en producción utilizando una máquina virtual como soporte para el contenedor se vería de la siguiente manera.

![nivel 0](img/lvl0.svg)

Es importante agregar una aclaración, este curso busca generar explicaciones agnósticas a los proveedores Cloud, independientes a sus servicios o plataformas. Teniendo claro los conceptos el proveedor de infraestructura o servicios es solo una capa de abstracción que puede empaquetar algunos de los pasos o recursos. En ocasiones ofreciendo simplificar procesos o tareas por un costo adicional o la contraprestación de tener contratar infraestructura con ellos.

[FastAPI](FastAPI/README.md)