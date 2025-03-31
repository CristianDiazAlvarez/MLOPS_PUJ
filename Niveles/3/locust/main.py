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
    # Simulación de inferencia: podrías reemplazar esta lógica por una real
    dummy_result = data.feature1 + data.feature2 + data.feature3  # solo suma

    return {
        "message": "Predicción generada exitosamente",
        "input": data.dict(),
        "resultado": dummy_result  # valor simulado
    }
