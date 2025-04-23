# Monitoreo con Prometheus y Grafana

 ¿Por qué es importante el monitoreo en MLOps?
Modelos pueden degradarse con el tiempo (data drift, concept drift)

- Infraestructura puede fallar (problemas de CPU, memoria, red, etc.)

- Necesidad de observabilidad continua para:
  - Prevenir caídas

  - Detectar degradaciones de rendimiento antes que afecten al usuario

  - Analizar el comportamiento post-despliegue de los modelos

## ¿Qué es Prometheus?

Sistema de monitoreo de series temporales basado en scraping de métricas

- Conceptos clave:

  - Targets: Componentes del sistema de donde Prometheus recoge métricas

  - Scrape: Acción de recolectar datos

  - Métricas: Datos estructurados (por ejemplo, cpu_usage, memory_usage, latency_seconds)

  - PromQL: Lenguaje de consultas de Prometheus

  - Alertmanager: Herramienta asociada para notificaciones automáticas.

- Funcionamiento general:

  - Los servicios exponen endpoints `/metrics`

  - Prometheus los consulta periódicamente (scrape)

  - Almacena métricas en su base de datos de series temporales

  - Permite consultas y alertas

## ¿Qué es Grafana?

Plataforma de visualización para métricas, logs y trazas

- Funciones principales:

  - Crear dashboards dinámicos

  - Conectar diferentes fuentes de datos (Prometheus, Loki, ElasticSearch, etc.)

Configurar alertas visuales

- Componentes importantes:

  - Panels: Gráficos individuales (líneas, barras, tablas, heatmaps)

  - Dashboards: Colecciones de panels organizados

  - Variables: Parámetros para hacer dashboards más dinámicos (ej., seleccionar el modelo a monitorear)

  - Alertas: Definición de condiciones que disparan notificaciones

## Flujo de trabajo entre Prometheus y Grafana

- Los modelos o servicios exponen métricas en /metrics (ej., API en FastAPI o Flask con prometheus_client)

- Prometheus recoge esas métricas y las almacena

- Grafana consulta Prometheus y construye dashboards

## ¿Qué métricas debemos monitorear en ML?

- De la infraestructura:

  - CPU utilizada

  - Memoria utilizada

  - Latencia de respuesta

  - Uso de disco

- Del modelo:

  - Latencia de inferencia

  - Tasa de error (error rate)

  - AUC, precisión, recall, F1 en producción (si es factible)

- De los datos:

  - Tamaño promedio de las solicitudes

  - Cambios de distribución (drift detection)

## Configuración de Prometheus y Grafana para monitorear una API de inferencia de ML

### API de inferencia

Usaremos una pequeña API en FastAPI que tiene un endpoint `/predict` simulado y otro endpoint `/metrics`usando `prometheus_client`

```python
from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

# Métricas Prometheus
REQUEST_COUNT = Counter('predict_requests_total', 'Total de peticiones de predicción')
REQUEST_LATENCY = Histogram('predict_latency_seconds', 'Tiempo de latencia de predicción')

@app.get("/predict")
def predict():
    import time
    import random
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        time.sleep(random.uniform(0.1, 0.3))
    return {"prediction": random.choice(["cat", "dog"])}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

```

`generate_latest()` devuelve todas las métricas registradas en formato que Prometheus entiende.

`CONTENT_TYPE_LATEST` asegura que el encabezado sea correcto (text/plain; version=0.0.4).

### Docker Compose

El archivo de docker compose contiene 3 servicios, prometheus, grafana y la API

```docker
version: '3'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  api:
    build: ./api
    ports:
      - "8000:8000"
```

### prometheus.yaml

Este archivo de configuración le especifica a prometheus a cuales servicios debe hacer peticiones buscando el endpoint `/metrics` y cual es el intervalo de búsqueda.

```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'api'
    static_configs:
      - targets: ['api:8000']
```

## Configurar dashboard en Grafana

- Conectar Prometheus como Data Source en Grafana

- Crear un Dashboard:

  - Número total de predicciones (predict_requests_total).

  - Latencia promedio (rate(predict_latency_seconds_sum[1m]) / rate(predict_latency_seconds_count[1m]))