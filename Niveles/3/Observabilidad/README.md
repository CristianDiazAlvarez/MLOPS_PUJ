# Observabilidad en MLOps con Prometheus + Grafana

Este laboratorio muestra cómo monitorear una API de inferencia con:

- Instrumentación de aplicación en FastAPI (`/metrics`)
- Recolección con Prometheus (scrape cada 5s)
- Visualización en Grafana (dashboard base provisionado)

## Arquitectura

- `api` (FastAPI): expone `/predict` y `/metrics`
- `prometheus`: recolecta métricas desde `api:8000/metrics`
- `grafana`: consulta Prometheus y muestra dashboards

## Métricas de la API

### Instrumentadas manualmente en la API

- `predict_requests_total` (Counter): total de peticiones de predicción
- `predict_latency_seconds` (Histogram): latencia por petición

Notas:

- Del `Histogram`, Prometheus también expone:
  - `predict_latency_seconds_bucket`
  - `predict_latency_seconds_sum`
  - `predict_latency_seconds_count`

### Métricas automáticas expuestas por `prometheus_client`

- `process_cpu_seconds_total`
- `process_resident_memory_bytes`
- `python_gc_objects_collected_total`
- otras métricas de proceso/runtime

Estas métricas son útiles para explicar diferencia entre observabilidad de negocio (predicciones/latencia del modelo) y observabilidad técnica (CPU/memoria/runtime).

## Ejecución

Desde `Niveles/3/Observabilidad`:

```bash
docker compose up --build
```

Servicios:

- API: http://localhost:8000
- API metrics: http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (`admin` / `admin`)

## Generar tráfico de prueba

```bash
for i in {1..100}; do curl -s http://localhost:8000/predict > /dev/null; done
```

## Consultas PromQL

- Total predicciones:

```promql
predict_requests_total
```

- Throughput (req/s):

```promql
rate(predict_requests_total[1m])
```

- Latencia promedio:

```promql
rate(predict_latency_seconds_sum[1m]) / rate(predict_latency_seconds_count[1m])
```

- Latencia percentil 95:

```promql
histogram_quantile(0.95, sum(rate(predict_latency_seconds_bucket[5m])) by (le))
```

- CPU proceso API:

```promql
rate(process_cpu_seconds_total[1m])
```

- Memoria proceso API:

```promql
process_resident_memory_bytes
```

## Dashboard base

Se crea automáticamente al iniciar Grafana:

- Carpeta: `MLOps`
- Dashboard: `MLOps - Observabilidad API`

Incluye paneles:

- Total Predicciones
- Requests por segundo (1m)
- Latencia promedio (ms)
- Latencia P95
- Serie de tráfico
- Serie de latencia (promedio y P95)
- Memoria del proceso
- CPU del proceso