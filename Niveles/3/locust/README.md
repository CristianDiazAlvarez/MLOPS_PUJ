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

Primero vamos a asumir que tenemos una API que tiene un endpoint `/predict` que recibe un JSON con los datos de entrada del modelo.

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
        # catch_response permite marcar explícitamente el resultado en Locust.
        with self.client.post(
            "/predict", json=payload, name="/predict", catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"HTTP {response.status_code}: {response.text[:200]}"
                )
                return

            try:
                body = response.json()
            except ValueError:
                response.failure("La respuesta no contiene JSON válido")
                return

            if "resultado" not in body:
                response.failure("La respuesta no contiene el campo 'resultado'")
                return

            response.success()

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

Sin embargo, por simplicidad se ha creado un Docker Compose para iniciar la API y Locust:

```bash
docker compose -f docker-compose.locust.yaml up --build
```

En `http://localhost:8089` se configura y ejecuta la prueba. Usar solamente
`print()` ante una respuesta incorrecta no comunica el fallo a Locust. En este
ejemplo, `response.failure(...)` aumenta el contador de fallos y conserva el
motivo en la interfaz y en los reportes. En una ejecución *headless*, Locust
también termina con un código distinto de cero si se registran errores.

## Taller Locust

El objetivo es relacionar las restricciones de CPU y memoria estudiadas en
[`../Recursos`](../Recursos/) con la capacidad observada mediante una prueba de
carga. Las pruebas de CPU y memoria de ese ejemplo son independientes y no es
necesario modificarlas.

1. Cree una imagen Docker que contenga una API FastAPI capaz de realizar
   inferencia con un modelo previamente entrenado y cargado desde MLflow.
2. Publique la imagen de inferencia en Docker Hub.
3. Cree un `docker-compose.yaml` que permita ejecutar la imagen publicada.
4. Despliegue en una VM la API de inferencia, Nginx como balanceador y los demás
   servicios que la aplicación necesite, pero **no ejecute Locust en esa misma
   VM**. Inicie una sola réplica de la API y limítela a 1 CPU y 1 GB de memoria.
5. Ejecute Locust desde una segunda VM o desde su máquina personal. Ambas
   máquinas deben poder comunicarse por red. De esta forma, la CPU y la memoria
   usadas para simular usuarios no compiten con los recursos de la API.
6. Aumente gradualmente los usuarios concurrentes y determine la cantidad
   máxima que puede atender una réplica de 1 CPU y 1 GB sin incumplir el criterio
   de capacidad.
7. Aumente la API a tres réplicas, cada una con 1 CPU y 1 GB, y repita la misma
   prueba desde la otra máquina. Mantenga iguales el `locustfile.py`, la tasa de
   aparición de usuarios, la duración y el criterio de aceptación.
8. Compare la capacidad máxima, los RPS y los tiempos de respuesta obtenidos con
   una y con tres réplicas.

Antes de medir, defina un criterio verificable. Por ejemplo: una configuración
"soporta" la carga si mantiene menos de 1 % de fallos y un percentil 95 (p95)
menor a 500 ms durante dos minutos. Antes de registrar cada nivel, deje que todos
los usuarios terminen de aparecer. Registre usuarios concurrentes, RPS,
peticiones totales, porcentaje de fallos, p95, CPU, memoria y réplicas. No
confunda usuarios concurrentes con peticiones por segundo: la espera configurada
en `wait_time` afecta directamente el RPS generado.

Comience con incrementos amplios y, al observar fallos o un aumento fuerte del
p95, repita con incrementos menores alrededor de ese punto. Vigile también la
CPU de la máquina que ejecuta Locust. Si esta se satura antes que la VM de la
API, el resultado describe el límite del generador y no el del servicio.

Use [`locust_limitado`](./locust_limitado/) como preparación en clase. Su README
explica Nginx, los comandos y la actividad para experimentar con límites de CPU,
memoria y réplicas. Para el taller evaluado, siga la separación entre máquinas
descrita en los puntos 4 y 5.

Responda finalmente:

- ¿Cuál es la concurrencia máxima sostenible y cuántos RPS procesa una réplica
  limitada a 1 CPU y 1 GB?
- ¿Cuál es la concurrencia máxima sostenible y cuántos RPS procesan tres
  réplicas con esos mismos límites por réplica?
- ¿En qué porcentaje cambió la capacidad? ¿El aumento fue cercano a tres veces
  o aparecieron otros cuellos de botella?
- ¿Qué recurso se saturó primero y qué evidencia muestran `docker stats`,
  Locust y la máquina generadora de carga?
- ¿Qué servicios adicionales —por ejemplo MLflow, base de datos o balanceador—
  pudieron limitar el resultado?
