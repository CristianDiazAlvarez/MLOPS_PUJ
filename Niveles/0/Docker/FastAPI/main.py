from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"MLOPS PUJ": "Hello World"}

