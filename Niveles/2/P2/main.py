from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel, Field
import random
import json
import time
import csv
import os

MIN_UPDATE_TIME = 300 ## Aca pueden cambiar el tiempo minimo para cambiar bloque de información

# ---------------------------
# Metadatos y documentación
# ---------------------------

# Descripción corta y accionable para Swagger UI.
APP_DESCRIPTION = (
    """
    API para suministrar datos del Proyecto 2 (Extracción de datos y entrenamiento de modelos).

    - Origen de datos externo: http://10.43.100.103:80
    - Los datos cambian cada 5 minutos (configurable con MIN_UPDATE_TIME).
    - El dataset completo se divide en 10 lotes (batches). Cada request al endpoint /data
      devuelve una porción aleatoria del batch vigente para el grupo solicitado.
    - Para obtener una muestra mínima útil, recolecta al menos una porción de cada uno de los 10 batches.
    - Uso sugerido: orquestar la recolección con Airflow y entrenar/registrar modelos con MLflow.

    Código y guía para desplegar/pruebas (incluyendo cómo reducir el tiempo entre cambios de batch):
    https://github.com/CristianDiazAlvarez/MLOPS_PUJ/tree/main/Niveles/2/P2

    Diagrama ilustrativo del flujo de batches (GitHub):
    https://raw.githubusercontent.com/CristianDiazAlvarez/MLOPS_PUJ/refs/heads/main/Niveles/2/P2/images/p2_data.png
    
    Orden de las columnas en el CSV:
    # Elevation,
    # Aspect,
    # Slope,
    # Horizontal_Distance_To_Hydrology,
    # Vertical_Distance_To_Hydrology,
    # Horizontal_Distance_To_Roadways,
    # Hillshade_9am,
    # Hillshade_Noon,
    # Hillshade_3pm,
    # Horizontal_Distance_To_Fire_Points,
    # Wilderness_Area,
    # Soil_Type,
    # Cover_Type
    """
)

tags_metadata = [
    {"name": "info", "description": "Información general del servicio."},
    {"name": "data", "description": "Obtención de porciones de datos por grupo y batch."},
    {"name": "admin", "description": "Operaciones de control para reiniciar conteos por grupo."},
]

app = FastAPI(
    title="Proyecto 2 - Data API",
    version="1.0.0",
    description=APP_DESCRIPTION,
    contact={
        "name": "Curso MLOps PUJ",
        "url": "https://github.com/CristianDiazAlvarez/MLOPS_PUJ",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=tags_metadata,
)

# ---------------------------
# Modelos para documentación
# ---------------------------

class BatchResponse(BaseModel):
    """Estructura de respuesta del endpoint /data."""

    group_number: int = Field(..., ge=1, le=10, description="Número de grupo solicitado (1-10)")
    batch_number: int = Field(..., description="Índice del batch servido para el grupo")
    data: List[List[str]] = Field(
        ..., description="Filas del dataset (valores en formato string) para la porción solicitada"
    )

# Elevation,
# Aspect,
# Slope,
# Horizontal_Distance_To_Hydrology,
# Vertical_Distance_To_Hydrology,
# Horizontal_Distance_To_Roadways,
# Hillshade_9am,
# Hillshade_Noon,
# Hillshade_3pm,
# Horizontal_Distance_To_Fire_Points,
# Wilderness_Area,
# Soil_Type,
# Cover_Type

@app.get(
    "/",
    tags=["info"],
    summary="Estado del servicio",
    description=(
        "Endpoint base para verificar disponibilidad. Devuelve información corta del proyecto."
    ),
)
async def root():
    return {"Proyecto 2": "Extracción de datos, entrenamiento de modelos."}


# Cargar los datos del archivo CSV
data = []
with open('/data/covertype.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        data.append(row)

batch_size = len(data) // 10

# Definir la función para generar la fracción de datos aleatoria
def get_batch_data(batch_number:int, batch_size:int=batch_size):
    start_index = batch_number * batch_size
    end_index = start_index + batch_size
    # Obtener datos aleatorios dentro del rango del grupo
    random_data = random.sample(data[start_index:end_index], batch_size // 10)
    return random_data

# Cargar información previa si existe
if os.path.isfile('/data/timestamps.json'):
    with open('/data/timestamps.json', "r") as f:
        timestamps = json.load(f)
        
else:
    # Definir el diccionario para almacenar los timestamps de cada grupo e incializar el conteo, inicia en -1 para no agregar logica adicional de conteo
    timestamps = {str(group_number): [0, -1] for group_number in range(1, 11)} # el valor está definido como [timestamp, batch]

# Definir la ruta de la API
@app.get(
    "/data",
    tags=["data"],
    summary="Obtener porción aleatoria del batch vigente",
    description=(
        "Devuelve filas aleatorias del batch actual para el grupo indicado. "
        "El batch cambia cada 5 minutos (MIN_UPDATE_TIME). Para una muestra mínima, "
        "extrae al menos una porción de cada uno de los 10 batches."
    ),
    response_model=BatchResponse,
    responses={
        200: {
            "description": "Porción de datos del batch vigente para el grupo indicado.",
            "content": {
                "application/json": {
                    "example": {
                        "group_number": 1,
                        "batch_number": 2,
                        "data": [
                            [
                                "2596","51","3","258","0","510","221","232","148","6279",
                                "Rawah","C7744","1"
                            ],
                            [
                                "2763","56","2","212","-6","390","220","235","151","6225",
                                "Rawah","C7745","1"
                            ]
                        ]
                    }
                }
            }
        },
        400: {
            "description": "Número de grupo inválido o se alcanzó la recolección mínima por grupo.",
        }
    },
)
async def read_data(
    group_number: int = Query(
        ..., ge=1, le=10, description="Número de grupo asignado (1-10).", example=1
    )
):
    global timestamps

    # Verificar si el número de grupo es válido
    if group_number < 1 or group_number > 10:
        raise HTTPException(status_code=400, detail="Número de grupo inválido")
    # Verificar si el número de conteo es adecuado
    if timestamps[str(group_number)][1] >= 10:
        raise HTTPException(status_code=400, detail="Ya se recolectó toda la información minima necesaria")
    
    current_time = time.time()
    last_update_time = timestamps[str(group_number)][0]
    
    # Verificar si han pasado más de 5 minutos desde la última actualización
    if current_time - last_update_time > MIN_UPDATE_TIME: 
        # Actualizar el timestamp y obtener nuevos datos
        timestamps[str(group_number)][0] = current_time
        timestamps[str(group_number)][1] += 2 if timestamps[str(group_number)][1] == -1 else 1
    
    # Utilizar los mismos datos que la última vez (una parte del mismo grupo de información)
    random_data = get_batch_data(group_number)
    with open('/data/timestamps.json', 'w') as file:
        file.write(json.dumps(timestamps))
    
    return {"group_number": group_number, "batch_number": timestamps[str(group_number)][1], "data": random_data}

@app.get(
    "/restart_data_generation",
    tags=["admin"],
    summary="Reiniciar la generación para un grupo",
    description=(
        "Reinicia el temporizador y el conteo de batch para el grupo indicado. "
        "Útil para pruebas locales o para volver a comenzar la recolección de datos de un grupo."
    ),
)
async def restart_data(
    group_number: int = Query(
        ..., ge=1, le=10, description="Número de grupo a reiniciar (1-10).", example=1
    )
):
    # Verificar si el número de grupo es válido
    if group_number < 1 or group_number > 10:
        raise HTTPException(status_code=400, detail="Número de grupo inválido")

    timestamps[str(group_number)][0] = 0
    timestamps[str(group_number)][1] = -1
    with open('/data/timestamps.json', 'w') as file:
        file.write(json.dumps(timestamps))
    return {'ok'}