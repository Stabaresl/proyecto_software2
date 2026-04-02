from locust import HttpUser, task, between
import random
import string


def random_email():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"capacity_{suffix}@locust.com"


class CapacidadUsuario(HttpUser):
    wait_time = between(1, 2)
    host = "http://localhost:8000"

    def on_start(self):
        self.email    = random_email()
        self.password = "Password123*"
        self.token    = None

        # Registrar
        reg = self.client.post("/api/auth/register", json={
            "email":                 self.email,
            "password":              self.password,
            "password_confirmation": self.password,
            "role":                  "student",
        }, timeout=30)

        # Login
        if reg.status_code == 201:
            res = self.client.post("/api/auth/login", json={
                "email":    self.email,
                "password": self.password,
            }, timeout=30)
            if res.status_code == 200:
                self.token = res.json().get("token")

    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(4)
    def listar_convocatorias(self):
        self.client.get("/api/convocatorias", timeout=30)

    @task(3)
    def ver_perfil(self):
        self.client.get("/api/auth/me", headers=self.auth_headers(), timeout=30)

    @task(2)
    def listar_formaciones(self):
        self.client.get("/api/formaciones", timeout=30)

    @task(2)
    def mis_postulaciones(self):
        self.client.get("/api/mis-postulaciones", headers=self.auth_headers(), timeout=30)

    @task(1)
    def catalogo(self):
        self.client.get("/api/catalogo/estudiantes", headers=self.auth_headers(), timeout=30)