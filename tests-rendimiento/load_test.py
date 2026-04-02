from locust import HttpUser, task, constant
import random
import string


def random_email():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"load_{suffix}@locust.com"


class CargaNormal(HttpUser):
    """
    Prueba de carga normal:
    - 50 usuarios simultáneos
    - Tiempo de espera constante de 1 segundo
    - Simula uso normal del sistema durante 2 minutos
    """
    wait_time = constant(1)
    host = "http://localhost:8000"

    def on_start(self):
        self.email    = random_email()
        self.password = "Password123*"

        self.client.post("/api/auth/register", json={
            "email":                 self.email,
            "password":              self.password,
            "password_confirmation": self.password,
            "role":                  "student",
        })

        res = self.client.post("/api/auth/login", json={
            "email":    self.email,
            "password": self.password,
        })
        self.token = res.json().get("token") if res.status_code == 200 else None

    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(4)
    def endpoint_publico(self):
        self.client.get("/api/convocatorias")

    @task(3)
    def endpoint_auth_get(self):
        self.client.get("/api/auth/me", headers=self.auth_headers())

    @task(2)
    def endpoint_listado(self):
        self.client.get("/api/formaciones")

    @task(1)
    def endpoint_notificaciones(self):
        self.client.get("/api/notificaciones", headers=self.auth_headers())