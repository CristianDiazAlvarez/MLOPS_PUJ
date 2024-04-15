from locust import HttpUser, task, constant
from pydantic import BaseModel

class CoverType(BaseModel):
    Elevation: float = 3154
    Aspect: float = 351
    Slope: float = 13
    Horizontal_Distance_To_Hydrology: str = "658"
    Vertical_Distance_To_Hydrology: str = "191"
    Horizontal_Distance_To_Roadways: str = "6164"
    Hillshade_9am: str = "172"
    Hillshade_Noon: str = "233"
    Hillshade_3pm: str = "200"
    Horizontal_Distance_To_Fire_Points: str = "1473"
    Wilderness_Area_Cache: int = 0
    Wilderness_Area_Commanche: int = 0
    Wilderness_Area_Neota: int = 0
    Wilderness_Area_Rawah: int = 0
    Soil_Type_C2702: int = 0
    Soil_Type_C2703: int = 0
    Soil_Type_C2704: int = 0
    Soil_Type_C2705: int = 0
    Soil_Type_C2706: int = 0
    Soil_Type_C2717: int = 0
    Soil_Type_C3501: int = 0
    Soil_Type_C3502: int = 0
    Soil_Type_C4201: int = 0
    Soil_Type_C4703: int = 0
    Soil_Type_C4704: int = 0
    Soil_Type_C4744: int = 0
    Soil_Type_C4758: int = 0
    Soil_Type_C5101: int = 0
    Soil_Type_C5151: int = 0
    Soil_Type_C6101: int = 0
    Soil_Type_C6102: int = 0
    Soil_Type_C6731: int = 0
    Soil_Type_C7101: int = 0
    Soil_Type_C7102: int = 0
    Soil_Type_C7103: int = 0
    Soil_Type_C7201: int = 0
    Soil_Type_C7202: int = 0
    Soil_Type_C7700: int = 0
    Soil_Type_C7701: int = 0
    Soil_Type_C7702: int = 0
    Soil_Type_C7709: int = 0
    Soil_Type_C7710: int = 0
    Soil_Type_C7745: int = 0
    Soil_Type_C7746: int = 1
    Soil_Type_C7755: int = 0
    Soil_Type_C7756: int = 0
    Soil_Type_C7757: int = 0
    Soil_Type_C7790: int = 0
    Soil_Type_C8703: int = 0
    Soil_Type_C8707: int = 0
    Soil_Type_C8708: int = 0
    Soil_Type_C8771: int = 0
    Soil_Type_C8772: int = 0
    Soil_Type_C8776: int = 0


class LoadTest(HttpUser):
    wait_time = constant(1)
    host = "http://inference:80"

    @task
    def predict(self):
        request_body = {
            "Elevation": 3154,
            "Aspect": 351,
            "Slope": 13,
            "Horizontal_Distance_To_Hydrology": "658",
            "Vertical_Distance_To_Hydrology": "191",
            "Horizontal_Distance_To_Roadways": "6164",
            "Hillshade_9am": "172",
            "Hillshade_Noon": "233",
            "Hillshade_3pm": "200",
            "Horizontal_Distance_To_Fire_Points": "1473",
            "Wilderness_Area_Cache": 0,
            "Wilderness_Area_Commanche": 0,
            "Wilderness_Area_Neota": 0,
            "Wilderness_Area_Rawah": 0,
            "Soil_Type_C2702": 0,
            "Soil_Type_C2703": 0,
            "Soil_Type_C2704": 0,
            "Soil_Type_C2705": 0,
            "Soil_Type_C2706": 0,
            "Soil_Type_C2717": 0,
            "Soil_Type_C3501": 0,
            "Soil_Type_C3502": 0,
            "Soil_Type_C4201": 0,
            "Soil_Type_C4703": 0,
            "Soil_Type_C4704": 0,
            "Soil_Type_C4744": 0,
            "Soil_Type_C4758": 0,
            "Soil_Type_C5101": 0,
            "Soil_Type_C5151": 0,
            "Soil_Type_C6101": 0,
            "Soil_Type_C6102": 0,
            "Soil_Type_C6731": 0,
            "Soil_Type_C7101": 0,
            "Soil_Type_C7102": 0,
            "Soil_Type_C7103": 0,
            "Soil_Type_C7201": 0,
            "Soil_Type_C7202": 0,
            "Soil_Type_C7700": 0,
            "Soil_Type_C7701": 0,
            "Soil_Type_C7702": 0,
            "Soil_Type_C7709": 0,
            "Soil_Type_C7710": 0,
            "Soil_Type_C7745": 0,
            "Soil_Type_C7746": 1,
            "Soil_Type_C7755": 0,
            "Soil_Type_C7756": 0,
            "Soil_Type_C7757": 0,
            "Soil_Type_C7790": 0,
            "Soil_Type_C8703": 0,
            "Soil_Type_C8707": 0,
            "Soil_Type_C8708": 0,
            "Soil_Type_C8771": 0,
            "Soil_Type_C8772": 0,
            "Soil_Type_C8776": 0
            }
        headers = {
            "Content-Type": "application/json",
        }
        self.client.post(
            "/predict?model_name=covertype", json=request_body, headers=headers
        )
