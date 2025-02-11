# Desarrollo de Machine Learning en Contenedores

El desarrollo de modelos de Machine Learning (ML) enfrenta desafíos significativos al pasar del entorno de desarrollo a producción. La reproducibilidad, escalabilidad y portabilidad son aspectos críticos para garantizar el éxito del ciclo de vida del modelo. Los contenedores permiten abordar estos desafíos al proporcionar entornos aislados y consistentes.

## Componentes Claves del Desarrollo de ML en Contenedores

1. **Entorno de Desarrollo Aislado:** Garantiza que las dependencias y configuraciones del entorno sean consistentes entre diferentes máquinas.
2. **Docker y Docker Compose:** Herramientas fundamentales para crear, gestionar y orquestar contenedores.
3. **Gestión de Dependencias:** Uso de archivos `requirements.txt` para definir las bibliotecas necesarias.
4. **Versionamiento de Imágenes:** Mantener versiones de imágenes para garantizar la trazabilidad y reproducibilidad.
5. **Orquestación de Contenedores:** Herramientas como Kubernetes para entornos de producción a gran escala.
6. **Persistencia de Datos:** Montaje de volúmenes para mantener datos entre sesiones.
7. **Exposición de Modelos:** APIs para desplegar modelos y permitir su consumo desde aplicaciones externas.

## Ejemplo Básico de Desarrollo en Contenedores

### 1. **Dockerfile para un Proyecto de ML**

```dockerfile
# Imagen base con Python y bibliotecas de ML
FROM python:3.9-slim

# Copiar archivos del proyecto
WORKDIR /app
COPY . /app

# Instalar dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Comando por defecto
CMD ["python", "main.py"]
```

### 2. **Archivo de requerimientos del proyecto**

```
numpy
pandas
scikit-learn
fastapi
uvicorn
```

### 3. **Script de ML (main.py)**

```python
from fastapi import FastAPI
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

app = FastAPI()

# Modelo simple de ejemplo
data = load_iris()
model = RandomForestClassifier()
model.fit(data.data, data.target)

@app.get("/predict")
def predict(sepal_length: float, sepal_width: float, petal_length: float, petal_width: float):
    prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
    return {"prediction": int(prediction[0])}
```

### 4. **Archivo Docker-compose**``

```yaml
version: '3'  # Especifica la versión de Docker Compose que se está utilizando.

services:     # Define los servicios que se ejecutarán en contenedores Docker.
  ml_service: # Nombre del servicio, en este caso es un servicio para ML (Machine Learning).
    build: .  # Indica que Docker debe construir la imagen usando el Dockerfile ubicado en el directorio actual (".").
    
    ports:
      - "8000:80" 
      # Mapea el puerto 80 del contenedor al puerto 8000 del host.
      # Esto permite acceder a la aplicación en http://localhost:8000 mientras que internamente escucha en el puerto 80.

    volumes:
      - './app:/app' 
      # Monta el directorio local './app' en la ruta '/app' dentro del contenedor.
      # Esto permite que los cambios realizados en el código fuente local se reflejen inmediatamente en el contenedor (ideal para desarrollo).

    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
    # Define el comando que se ejecutará al iniciar el contenedor.
    # Aquí se usa `uvicorn` para iniciar una aplicación FastAPI (`main:app`).
    # --host 0.0.0.0: Permite que la aplicación sea accesible desde cualquier IP dentro de la red del contenedor.
    # --port 80: La aplicación se ejecutará en el puerto 80 dentro del contenedor.
    # --reload: Activa el modo de recarga automática, útil para entornos de desarrollo ya que reinicia el servidor si hay cambios en el código.

```

### 5. **Iniciar el Contenedor**

```bash
docker-compose up --build
```

Valores de referencia para probar el servicio:
  - sepal_length=5.1
  - sepal_width=3.5
  - petal_length=1.4
  - petal_width=0.2
## Actividad en Clase

1. Tome el Taller 1 desplieguelo usando Docker Compose
2. Cree un volumen persistente para guardar logs de predicciones