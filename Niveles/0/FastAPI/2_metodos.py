from fastapi import FastAPI

app = FastAPI()

# Ruta GET
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "message": "Este es el item solicitado"}

# Ruta POST
@app.post("/items/")
def create_item(name: str):
    return {"name": name, "message": "El item ha sido creado"}

# Ruta PUT
@app.put("/items/{item_id}")
def update_item(item_id: int, name: str):
    return {"item_id": item_id, "name": name, "message": "Item actualizado"}

# Ruta DELETE
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} eliminado"}
