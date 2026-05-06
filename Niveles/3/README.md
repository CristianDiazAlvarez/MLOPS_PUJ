# Nivel 3 - Automatizado

En este nivel de MLOps, el objetivo principal es lograr una automatización avanzada en la gestión de modelos de machine learning. Se introducen herramientas de orquestación y monitoreo que permiten una operación continua de los modelos en producción, minimizando la intervención manual y mejorando la escalabilidad.

## 1. Orquestación y Escalabilidad con Kubernetes ☸️

El despliegue de modelos de machine learning en producción requiere gestionar múltiples componentes y garantizar su disponibilidad. **Kubernetes** permite automatizar el despliegue, la administración y la escalabilidad de los contenedores.

- **Gestión de clústeres**: Configuración de entornos escalables para la ejecución de modelos.
- **Despliegue de modelos en Kubernetes**: Uso de manifestos de Kubernetes para definir servicios y recursos.
- **Escalabilidad automática**: Configuración de **Horizontal Pod Autoscaler (HPA)** para ajustar dinámicamente la cantidad de réplicas en función de la carga de trabajo.

[**Kubernetes**](Kubernetes/README.md) será la tecnología utilizada para garantizar la estabilidad y escalabilidad de los modelos en producción.

## 2. Airflow en Kubernetes con Helm 🌀

Como continuidad de Airflow en Docker Compose (Nivel 2), en este nivel se migra a una ejecución sobre Kubernetes local usando el Helm Chart oficial.

- **Despliegue base en clúster local** con `kind + helm`.
- **Validación operativa** de pods, release y UI.
- **Extensión por imagen custom** para incluir DAGs y dependencias del proyecto.

[**Airflow en Kubernetes**](Airflow/README.md) será la base para orquestación de pipelines en entorno local de laboratorio.

## 3. Pruebas de Carga y Performance con Locust 📈

Una vez desplegados los modelos, es crucial evaluar su rendimiento bajo diferentes cargas de trabajo. **Locust** es una herramienta de código abierto que permite realizar pruebas de carga para evaluar el desempeño de los modelos de machine learning en un entorno de producción.

- **Simulación de tráfico real**: Generación de múltiples solicitudes concurrentes para evaluar la capacidad del modelo.
- **Identificación de cuellos de botella**: Análisis de tiempos de respuesta y optimización del rendimiento.

[**Locust**](Locust/README.md) se utilizará para validar la escalabilidad de los modelos y garantizar que el sistema pueda manejar grandes volúmenes de solicitudes.

## 4. Monitoreo con Prometheus y Grafana 📊

Para mantener la estabilidad y el rendimiento del sistema, es fundamental contar con herramientas de monitoreo. **Prometheus** y **Grafana** permiten recopilar, analizar y visualizar métricas en tiempo real.

- **Prometheus**: Sistema de monitoreo que recolecta métricas de diferentes componentes del sistema, incluyendo consumo de CPU, memoria y tiempo de respuesta de los modelos.
- **Grafana**: Plataforma de visualización que permite construir dashboards personalizados para monitorear el estado del sistema en producción.

[**Observabilidad**](Observabilidad/README.md) integra Prometheus y Grafana para asegurar visibilidad de extremo a extremo.

## 5. CI/CD: Pruebas y Automatización 🔁

Para sostener automatización confiable en producción, se requiere validar código antes de integrar y publicar artefactos.

- **Unit Testing con Pytest**: Pruebas unitarias básicas para validar funciones y evitar regresiones.
- **GitHub Actions**: Workflow para ejecutar pruebas al detectar cambios en rutas específicas y publicar imagen solo en `main` si todos los tests pasan.

[**CI/CD**](CICD/README.md) será el punto de partida para prácticas de calidad y automatización de despliegues.

---

Al finalizar este nivel, los estudiantes habrán aprendido a automatizar el despliegue de modelos en Kubernetes, orquestar pipelines con Airflow en clúster local, aplicar pruebas unitarias y flujos básicos de CI/CD, evaluar rendimiento con pruebas de carga y monitorear el sistema con herramientas especializadas.
