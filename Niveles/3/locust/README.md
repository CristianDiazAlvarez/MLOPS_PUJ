# Locust

Locust es una herramienta de código abierto para realizar pruebas de carga distribuidas y escalables. Está escrita en Python y permite simular miles (o incluso millones) de usuarios concurrentes que interactúan con un sistema, con el objetivo de medir su rendimiento y detectar cuellos de botella.

### Características principales

- `Fácil de usar`: Las pruebas de carga se escriben en Python, lo que las hace legibles, flexibles y fáciles de mantener.

- `Altamente escalable`: Puede ejecutarse de forma distribuida para simular un alto volumen de usuarios desde múltiples máquinas.

- `Interfaz web`: Ofrece una UI web intuitiva donde se puede iniciar, detener y monitorear las pruebas en tiempo real.

### ¿Para qué sirve?

Permite medir tiempos de respuesta y rendimiento de APIs o sitios web, lo que es indispensable para identificar cuellos de botella o puntos débiles bajo alta carga y validar que una aplicación puede escalar correctamente y soportar un número esperado de usuarios concurrentes. Para esto vamos a realizar pruebas de resistencia (stress testing) y durabilidad (soak testing).

---
#### Ejemplo simple

Primeo vamos a asumir que tenemos una API que tiene un endpoint `/predict` que recibe un JSON con los datos de entrada del modelo.

```python
from locust import HttpUser, task, between

class UsuarioDeCarga(HttpUser):
    # Tiempo de espera entre tareas por usuario simulado (en segundos)
    wait_time = between(1, 2.5)

    @task
    def hacer_inferencia(self):
        payload = {
            "feature1": 5.3,
            "feature2": 2.1,
            "feature3": 0.8
        }
        # Enviar una petición POST al endpoint /predict
        response = self.client.post("/predict", json=payload)
        # Opcional: validación de respuesta
        if response.status_code != 200:
            print("❌ Error en la inferencia:", response.text)

```

Ahora necesitamos nuestra API
Debemos asegurar de que la API esté corriendo (por ejemplo en http://localhost:8000)

El siguiente ejemplo muestra una API dummy

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

app = FastAPI()

# Definimos la estructura esperada del JSON de entrada
class InputData(BaseModel):
    feature1: float
    feature2: float
    feature3: float

@app.post("/predict")
def predict(data: InputData) -> Any:
    # Simulación de inferencia: aca se debe reemplazar esta lógica por una real
    dummy_result = data.feature1 + data.feature2 + data.feature3  # solo suma

    return {
        "message": "Predicción generada exitosamente",
        "input": data.dict(),
        "resultado": dummy_result  # valor simulado
    }
```

Ahora para ejecutar locust usariamos el siguiente comando:

```bash
locust -f locustfile.py --host http://localhost:8000
```

Sin embargo, por simplicidad se ha creado un docker compose para iniciar la API y Locust

```bash
docker-compose -f docker-compose.locust.yaml up --build
```

## Taller Locust

- Cree una imagen de docker que contenga una API usando FastAPI que permita realizar inferencia a un modelo previamente entrenado.
    - Este modelo debe ser consumido de MLflow
- Publique el la imagen de inferencia en DockerHub
- Cree un docker-compose.yaml que le permita usar la imagen publicada.
- Cree un docker-compose.yaml (diferente) que le permita realizar pruebas de carga a su imagen de inferencia (use Locust)
- Límite los recursos de su contenedor de inferencia al mínimo posible para que soporte 10.000 usuarios agregando 500 cada vez.

- Cuando se encuentre los recursos mínimos para soportar esta carga, incremente la cantidad de replicas de la API en el docker compose y describa el comportamiento, ¿Es posible reducir más los recursos? ¿Cuál es la mayor cantidad de peticiones soportadas? ¿Qué diferencia hay entre una o multiples instancias?
- Si no logra llegar a 10.000 usuarios, ¿Cual es la cantidad máxima alcanzada?
