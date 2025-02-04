from fastapi import FastAPI # Importamos la clase FastAPI

app = FastAPI() # Instanciamos la clase FastAPI

@app.get("/") # Definimos una ruta GET
def home(): # Definimos una función llamada home
    return {"message": "¡Hola, FastAPI está funcionando!"} # Retornamos un diccionario con un mensaje
