from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"1": "Laptop", "2": "Teléfono"}

@app.get("/items/{item_id}")
def get_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return {"item_id": item_id, "name": items[item_id]}
