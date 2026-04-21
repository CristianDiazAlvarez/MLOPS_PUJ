from locust import HttpUser, between, task


class PredictUser(HttpUser):
    wait_time = between(0.01, 0.05)

    @task
    def predict(self):
        self.client.get("/predict", name="/predict")
