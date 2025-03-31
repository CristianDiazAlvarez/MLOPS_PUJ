# Nivel 2 - Estructurado

En este nivel de MLOps, se introduce una mayor estandarización en el desarrollo, experimentación y despliegue de modelos de machine learning. Se comienza a implementar el uso de pipelines de ML para mejorar la reproducibilidad y trazabilidad, además de integrar herramientas para la gestión de experimentos y el monitoreo del rendimiento de los modelos.

## 1. Pipelines de ML Estandarizadas 🔄

Los pipelines de machine learning permiten organizar de manera estructurada los diferentes pasos de un flujo de trabajo de ML, desde la ingesta de datos hasta el despliegue del modelo. En este nivel se introduce **Apache Airflow** como herramienta para la orquestación de flujos de trabajo, lo que permite definir tareas de forma modular y escalonada, facilitando la escalabilidad y mantenimiento del código.

- **[Airflow](Airflow/README.md)**: Se usará para programar, monitorizar y gestionar flujos de trabajo de ML de manera automatizada y reproducible.

## 2. Gestión de Experimentos y Registro de Modelos 📊

El versionamiento y seguimiento de los experimentos es un aspecto clave en MLOps. En este nivel, se introduce el uso de **MLflow**, una plataforma de código abierto diseñada para gestionar el ciclo de vida de los modelos de machine learning. Esto incluye:

- **Rastreo de experimentos**: Registrar diferentes ejecuciones con sus respectivos hiperparámetros y métricas de evaluación.
- **Versionamiento de modelos**: Guardar y comparar diferentes versiones de un modelo entrenado.
- **Despliegue de modelos**: Facilitar la transición de un modelo desde el entorno de experimentación hasta producción.

[**MLflow**](MLflow/README.md) será la herramienta utilizada en este nivel para la gestión de experimentos y modelos.

## 3. Redes de Docker y Comunicación entre Servicios 🌐

A medida que el sistema crece en complejidad, es importante establecer una comunicación eficiente entre los diferentes componentes del sistema de machine learning. En este nivel, se trabajará con **redes de Docker**, que permiten que los contenedores se comuniquen entre sí de manera segura y eficiente.

- **Redes de Docker**: Se explorará cómo conectar distintos servicios de manera estructurada dentro de un ecosistema basado en contenedores.
- **Interoperabilidad entre servicios**: Comunicación entre pipelines de Airflow, tracking de MLflow y otros servicios.

[**Redes de Docker**](Redes_Docker/README.md) se estudiarán en detalle para garantizar que las soluciones de ML puedan escalar de manera estructurada.

---

Al finalizar este nivel, los estudiantes habrán adquirido conocimientos fundamentales sobre la estructuración y automatización de procesos en MLOps. La implementación de pipelines, la gestión de experimentos y el uso de redes de Docker permitirá una mayor eficiencia y control sobre los modelos en desarrollo, sentando las bases para la automatización avanzada en los siguientes niveles.
