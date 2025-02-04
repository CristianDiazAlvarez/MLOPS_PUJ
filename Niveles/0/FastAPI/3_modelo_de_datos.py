from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Definiendo un modelo de datos
class Item(BaseModel):
    name: str
    price: float
    description: str

@app.post("/items/")
def create_item(item: Item):
    return {"message": "Item creado", "item": item}
