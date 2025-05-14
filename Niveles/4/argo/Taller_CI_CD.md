
# Taller: CI/CD y GitOps para Despliegue de API de IA

## Objetivo del Taller

Diseñar e implementar una arquitectura CI/CD con GitOps para desplegar una API FastAPI con un modelo de IA, incluyendo observabilidad con Prometheus y Grafana, utilizando GitHub Actions, Docker, Kubernetes y Argo CD.

---

## Estructura del Proyecto

```
MLOPS_PUJ/
├── .github/workflows/ci-cd.yml
├── Niveles/
│   └── 4/
│       ├── api/
│       │   ├── app/main.py
│       │   ├── app/model.pkl
│       │   ├── train_model.py
│       │   ├── Dockerfile
│       │   └── requirements.txt
│       ├── loadtester/
│       │   ├── main.py
│       │   ├── Dockerfile
│       │   └── requirements.txt
│       ├── manifests/
│       │   ├── api-deployment.yaml
│       │   ├── script-deployment.yaml
│       │   ├── prometheus-deployment.yaml
│       │   ├── grafana-deployment.yaml
│       │   ├── grafana-config/datasources.yaml
│       │   ├── prometheus.yml
│       │   └── kustomization.yaml
│       └── argo-cd/app.yaml
```

---

## Servicios a Implementar

### FastAPI API
- Endpoint `/predict` que usa un modelo entrenado (`model.pkl`)
- Endpoint `/metrics` con `prometheus_client`

### LoadTester
- Envía peticiones aleatorias a la API cada segundo

### Prometheus
- Scrapea métricas de la API

### Grafana
- Visualiza métricas a partir de Prometheus

### GitHub Actions
- Entrena el modelo
- Construye y sube imágenes Docker

### Argo CD
- Sincroniza manifiestos desde Git automáticamente

---

## Instrucciones Paso a Paso

1. Crear `train_model.py` para entrenar y guardar un modelo
2. Implementar la API en `app/main.py` con predicción y métricas
3. Crear Dockerfile de la API y de LoadTester
4. Crear script de carga `loadtester/main.py`
5. Escribir manifiestos YAML para:
   - API (deployment + service)
   - LoadTester (deployment)
   - Prometheus (deployment + service + configmap)
   - Grafana (deployment + service + configmap)
6. Configurar `.github/workflows/ci-cd.yml`:
   - Entrenar modelo
   - Construir imágenes
   - Publicar imágenes
   - Actualizar versiones de manifiestos 

7. Escribir `kustomization.yaml`
8. Crear archivo `argo-cd/app.yaml` para Argo CD

---

## Evaluación

| Criterio                                   | Peso |
|-------------------------------------------|------|
| Correcta estructura y componentes YAML     | 20%  |
| Dockerfiles funcionales y eficientes       | 15%  |
| Entrenamiento automatizado en el pipeline  | 15%  |
| Instrumentación y métricas Prometheus      | 20%  |
| Funcionalidad de Grafana + visualización   | 10%  |
| Integración completa GitHub Actions + Argo | 20%  |

---

## Recomendaciones

- Usa `kubectl port-forward` para acceder a Grafana localmente
- Valida que las métricas de `/predict` se visualicen correctamente
- Documenta en tu README cómo probar y desplegar el sistema
