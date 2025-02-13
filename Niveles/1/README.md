# Nivel 1

En este nivel en MLOps, el objetivo principal es integrar prácticas fundamentales que ya están consolidadas en el desarrollo de software tradicional, adaptándolas al ciclo de vida de los proyectos de machine learning. Estas prácticas sientan las bases para una mayor eficiencia, colaboración y control en el desarrollo y despliegue de modelos.

## 1. Versionamiento de Código 💾

El seguimiento de los cambios en el código es crucial para garantizar la trazabilidad y la colaboración efectiva entre los miembros del equipo. Para esto, se utiliza [**Git**](Git/README.md), un sistema de control de versiones distribuido que permite gestionar el historial de modificaciones en cualquier conjunto de archivos. Git es ampliamente utilizado para coordinar el trabajo de múltiples desarrolladores que contribuyen de manera simultánea al código fuente, facilitando la integración continua y la resolución de conflictos.

## 2. Manejo de Paquetes en Proyectos 💻

El manejo adecuado de dependencias es clave para la reproducibilidad de los experimentos de machine learning. Se abordan herramientas y buenas prácticas para la gestión de paquetes, lo que incluye la creación de entornos virtuales y la documentación precisa de las bibliotecas utilizadas mediante archivos como `requirements.txt` o `pyproject.toml`. De manera específica se usará [**UV**](uv/README.md) para este fin.

## 3. Desarrollo en Contenedores ⚙️

La portabilidad y la consistencia del entorno de desarrollo y producción son esenciales en MLOps. Aquí se introduce el uso de contenedores, que permiten empaquetar aplicaciones junto con sus dependencias para garantizar que se ejecuten de manera uniforme en diferentes entornos. Se hace especial énfasis en **Docker**, una de las herramientas más populares para la creación y gestión de contenedores. Al final de esta sección, se realizará un taller práctico en clase donde los estudiantes aprenderán a configurar un ambiente de desarrollo utilizando **[Docker Compose](DockerCompose/README.md)**.

Desarrollar en contenedores ofrece ventajas clave como el aislamiento de entornos, evitando conflictos de dependencias entre proyectos, y la portabilidad, permitiendo que las aplicaciones se ejecuten de forma consistente en diferentes sistemas. Además, facilita la escalabilidad y optimiza los flujos de trabajo de integración y despliegue continuo (CI/CD), mejorando la eficiencia en la gestión de recursos y el mantenimiento del software **[Desarrollo en Contenedores](Desarollo_en_contenedores/README.md)**.

## 4. Validación y Transformación de Datos 💉

Una estructura de proyecto bien definida facilita la organización del código, la colaboración entre equipos y la mantenibilidad a largo plazo. Este nivel incluye directrices para estructurar proyectos de machine learning de forma modular y escalable. Además, se abordan dos aspectos críticos del procesamiento de datos:

- **[Validación de Datos](Validacion_de_datos/README.md):** Técnicas para asegurar la calidad y la integridad de los datos, detectando inconsistencias, valores nulos o atípicos que puedan afectar el rendimiento del modelo.
- [**Transformación de Datos:**](Transformacion_de_datos/README.md) Métodos para preparar los datos antes del entrenamiento del modelo, incluyendo la normalización, estandarización y codificación de variables.

Al finalizar este nivel, los estudiantes habrán adquirido las habilidades necesarias para establecer un flujo de trabajo básico pero sólido en proyectos de machine learning, sentando las bases para niveles más avanzados de automatización y operación continua.
