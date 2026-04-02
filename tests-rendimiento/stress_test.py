from locust import HttpUser, task, between
import random
import string


def random_email():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"stress_{suffix}@locust.com"


class EstresUsuario(HttpUser):
    """
    Prueba de estrés:
    - Empieza con 10 usuarios y sube hasta 200
    - Tiempo de espera muy corto entre requests
    - Busca el punto de quiebre del sistema
    """
    wait_time = between(0.1, 0.5)
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

    @task(5)
    def hit_gateway(self):
        self.client.get("/api/convocatorias")

    @task(3)
    def hit_auth(self):
        self.client.get("/api/auth/me", headers=self.auth_headers())

    @task(2)
    def hit_usuarios(self):
        self.client.get("/api/usuarios/universities", headers=self.auth_headers())

    @task(2)
    def hit_formaciones(self):
        self.client.get("/api/formaciones")

    @task(1)
    def hit_matching(self):
        self.client.get("/api/catalogo/estudiantes", headers=self.auth_headers())