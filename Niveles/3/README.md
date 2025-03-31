# Nivel 3 - Automatizado

En este nivel de MLOps, el objetivo principal es lograr una automatización avanzada en la gestión de modelos de machine learning. Se introducen herramientas de orquestación y monitoreo que permiten una operación continua de los modelos en producción, minimizando la intervención manual y mejorando la escalabilidad.

## 1. Orquestación y Escalabilidad con Kubernetes ☸️

El despliegue de modelos de machine learning en producción requiere gestionar múltiples componentes y garantizar su disponibilidad. **Kubernetes** permite automatizar el despliegue, la administración y la escalabilidad de los contenedores.

- **Gestión de clústeres**: Configuración de entornos escalables para la ejecución de modelos.
- **Despliegue de modelos en Kubernetes**: Uso de manifestos de Kubernetes para definir servicios y recursos.
- **Escalabilidad automática**: Configuración de **Horizontal Pod Autoscaler (HPA)** para ajustar dinámicamente la cantidad de réplicas en función de la carga de trabajo.

[**Kubernetes**](Kubernetes/README.md) será la tecnología utilizada para garantizar la estabilidad y escalabilidad de los modelos en producción.

## 2. Pruebas de Carga y Performance con Locust 📈

Una vez desplegados los modelos, es crucial evaluar su rendimiento bajo diferentes cargas de trabajo. **Locust** es una herramienta de código abierto que permite realizar pruebas de carga para evaluar el desempeño de los modelos de machine learning en un entorno de producción.

- **Simulación de tráfico real**: Generación de múltiples solicitudes concurrentes para evaluar la capacidad del modelo.
- **Identificación de cuellos de botella**: Análisis de tiempos de respuesta y optimización del rendimiento.

[**Locust**](Locust/README.md) se utilizará para validar la escalabilidad de los modelos y garantizar que el sistema pueda manejar grandes volúmenes de solicitudes.

## 3. Monitoreo con Prometheus y Grafana 📊

Para mantener la estabilidad y el rendimiento del sistema, es fundamental contar con herramientas de monitoreo. **Prometheus** y **Grafana** permiten recopilar, analizar y visualizar métricas en tiempo real.

- **Prometheus**: Sistema de monitoreo que recolecta métricas de diferentes componentes del sistema, incluyendo consumo de CPU, memoria y tiempo de respuesta de los modelos.
- **Grafana**: Plataforma de visualización que permite construir dashboards personalizados para monitorear el estado del sistema en producción.

[**Prometheus**](Prometheus/README.md) y [**Grafana**](Grafana/README.md) serán implementados para asegurar la observabilidad de los modelos y la infraestructura.

---

Al finalizar este nivel, los estudiantes habrán aprendido a automatizar el despliegue de modelos en Kubernetes, evaluar su rendimiento con pruebas de carga y monitorear su estado con herramientas especializadas. Con estas capacidades, los sistemas de machine learning pueden operar de manera confiable y escalable en entornos de producción.
