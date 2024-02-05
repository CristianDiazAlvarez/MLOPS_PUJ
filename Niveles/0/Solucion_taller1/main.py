from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from os.path import exists
import pandas as pd
from joblib import dump, load
from typing import List

from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.preprocessing import LabelEncoder


class Penguin(BaseModel):
    studyName: str = "PAL0708"
    SampleNumber: int = 1
    Region: str = "Anvers"
    Island: str = "Torgersen"
    Stage: str = "Adult, 1 Egg Stage"
    IndividualID: str = "N1A1"
    ClutchCompletion: str = "Yes"
    DateEgg: str = "11/11/07"
    CulmenLength_mm: float = 39.1
    CulmenDepth_mm: float = 18.7
    FlipperLength_mm: float = 181.0
    BodyMass_g: float = 3750.0
    Sex: str = "MALE"
    Delta_15_N: str = "NaN"
    Delta_13_C: str = "NaN"
    Comments: str = "Not enough blood for isotopes."


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/train")
async def train():
    try:
        data = process_to_train()
        data = encode_features(data)
        train_model(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return "Model trained"

@app.post("/do_inference")
async def do_inference(penguin: Penguin):

    try:
        island_Encoder = loadLabelEncoder()
        model = loadSVCModel()
        penguin_list = process_penguin(penguin, island_Encoder)

    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))
    return {str(inference_penguin(model, penguin_list))}

def loadLabelEncoder(file_name: str = 'Island_Encoder.joblib')->LabelEncoder():
    """
    Load label encoder
    input:
        file_name: Name of file encoded as joblib 
    output:
        loaded LabelEncoder Object
    """
    assert exists(file_name), 'File {file_name} not found'.format(file_name=file_name)
    assert file_name.endswith('.joblib'), 'File type is different to .joblib'
    return load(file_name)

def loadSVCModel(file_name: str ='penguin_model.joblib') -> svm.SVC():
    """
    Load SVC model
    input:
        file_name: Name of file encoded as joblib 
    output:
        loaded svm.SVC Object
    """

    assert exists(file_name), 'File {file_name} not found'.format(file_name=file_name)
    assert file_name.endswith('.joblib'), 'File type is different to .joblib'
    return load(file_name)

def process_penguin(penguin: Penguin, island_Encoder:LabelEncoder()) -> List:
    """
    From Pydantic Model process data to use SVC model, required as list
    input:
        penguin: Pydantic Model 
    output:
        list of fields required to do inference
    """
    penguin_dict = penguin.model_dump(include=["FlipperLength_mm",  "BodyMass_g",
                                               "CulmenLength_mm", "CulmenDepth_mm",
                                               "Island", "DateEgg"])
    penguin_df = pd.DataFrame([penguin_dict])
    penguin_df['DateEgg'] = penguin_df['DateEgg'].apply(lambda x: x.split('/')[0]).astype(int)
    penguin_df['Island'] = island_Encoder.transform(penguin_df['Island'])
    return [penguin_df.iloc[0]]

def inference_penguin(model: svm.SVC(), penguin: List):
    """
    do inference of saved model
    input:
        penguin: list of fields required to do inference 
    output:
        number of class predicted
    """
    return model.predict(penguin)[0]


def process_to_train(file_name: str='data/penguins_lter.csv') -> pd.DataFrame:
    """
    Load CSV and process data to train model


    """
    assert exists(file_name), 'File {file_name} not found'.format(file_name=file_name)
    assert file_name.endswith('.csv'), 'File type is different to .csv'
    data = pd.read_csv(file_name)
    data = data.rename(columns={"Flipper Length (mm)": "FlipperLength_mm",
                        "Body Mass (g)":"BodyMass_g",
                        "Culmen Length (mm)":"CulmenLength_mm",
                        "Culmen Depth (mm)":"CulmenDepth_mm",
                        "Date Egg":"DateEgg"})

    features = ["FlipperLength_mm",  "BodyMass_g",
                "CulmenLength_mm", "CulmenDepth_mm", 
                "Island", "DateEgg","Species"]

    data = data[features].dropna()
    data['DateEgg'] = data['DateEgg'].apply(lambda x: x.split('/')[0]).astype(int)
    return data

def encode_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Encode features
    """
    label_encoder = LabelEncoder() 

    for i in data.columns:
        if data[i].dtype == "object":
            label_encoder.fit_transform(list(data[i].values))
            data[i] = label_encoder.transform(data[i].values)
            if i=='Island':
                dump(label_encoder,'Island_Encoder.joblib')
    return data

def train_model(data: pd.DataFrame):
    x = data.drop(columns=['Species'])
    y = data['Species']

    X_train, X_test, y_train, y_test = train_test_split(x,
                                                         y, random_state=42, 
                                                         test_size=.2, stratify=y)
    clf = svm.SVC()
    clf.fit(x, y)
    dump(clf, 'penguin_model.joblib')