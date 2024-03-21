from fastapi import FastAPI, HTTPException
from typing import Optional
import random
import json
import time
import csv
import os

MIN_UPDATE_TIME = 300 ## Aca pueden cambiar el tiempo minimo para cambiar bloque de información

app = FastAPI()

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

@app.get("/")
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
@app.get("/data")
async def read_data(group_number: int):
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

@app.get("/restart_data_generation")
async def restart_data(group_number: int):
    # Verificar si el número de grupo es válido
    if group_number < 1 or group_number > 10:
        raise HTTPException(status_code=400, detail="Número de grupo inválido")

    timestamps[str(group_number)][0] = 0
    timestamps[str(group_number)][1] = -1
    with open('/data/timestamps.json', 'w') as file:
        file.write(json.dumps(timestamps))
    return {'ok'}