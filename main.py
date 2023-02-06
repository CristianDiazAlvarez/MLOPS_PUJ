from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

import requests
import os
import numpy as np
import pandas as pd
from joblib import dump, load

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import metrics


url_wine='https://docs.google.com/uc?export=download&id=1ZsJWYHxcEdJQdb62diQf8o3fvXFawt1a'
url_house_price='https://docs.google.com/uc?export=download&id=1WsTJN-u4YRrPKqJTp8h8iUSAdfJC8_qn'

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def get_data(data:str='wine'):
    if data=='wine' or data=='house_price':
        if not os.path.isfile(data+'.csv'):
            url = url_wine if data == 'wine' else url_house_price
            r = requests.get(url, allow_redirects=True)
            open(data+'.csv', 'wb').write(r.content)
    else:
        raise HTTPException(status_code=500, detail="Unkown dataset: "+ data)

@app.get("/train_model")
async def train_model(data:str='wine'):
    get_data()
    if not os.path.isfile(data+'.csv'):
        raise HTTPException(status_code=500, detail="Unkown dataset: "+ data)
    df = pd.read_csv('wine.csv')
    df.columns = df.columns.str.replace(' ', '_')
    X = df.drop('quality', axis=1)
    y = df['quality']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    model = SVC()
    model.fit(X_train, y_train)
    expected_y  = y_test
    predicted_y = model.predict(X_test)
    model_metrics = metrics.classification_report(expected_y, predicted_y, output_dict=True,zero_division=1)
    dump(model, data+'_model.joblib')
    return model_metrics
    
class Wine(BaseModel):
    fixed_acidity: float = 8.0
    volatile_acidity: float = 0.57
    citric_acid: float = 0.23
    residual_sugar: float = 3.2
    chlorides: float = 0.073
    free_sulfur_dioxide: float = 17.0
    total_sulfur_dioxide: float = 119.0
    density: float = 0.99675	
    pH: float = 3.26
    sulphates: float = 0.57
    alcohol: float = 9.3

@app.post("/do_inference")
async def train_model(wine: Wine, model:str='wine'):
    if not os.path.isfile(model+'_model.joblib'):
        raise HTTPException(status_code=500, detail="Unkown model: "+ model+" Try to train model first.")
    model_loaded = load(model+'_model.joblib')
    return int(model_loaded.predict(pd.DataFrame([wine.dict()]))[0])