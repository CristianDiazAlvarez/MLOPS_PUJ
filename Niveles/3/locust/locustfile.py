from locust import HttpUser, task, between


class UsuarioDeCarga(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def hacer_inferencia(self):
        payload = {
            "feature1": 5.3,
            "feature2": 2.1,
            "feature3": 0.8
        }
        # catch_response permite decidir explícitamente si Locust debe registrar
        # la petición como éxito o como fallo.
        with self.client.post(
            "/predict", json=payload, name="/predict", catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"HTTP {response.status_code}: {response.text[:200]}"
                )
                return

            try:
                body = response.json()
            except ValueError:
                response.failure("La respuesta no contiene JSON válido")
                return

            if "resultado" not in body:
                response.failure("La respuesta no contiene el campo 'resultado'")
                return

            response.success()
