from locust import HttpUser, task, between, events
import random
import string

def random_email():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{suffix}@locust.com"


class UsuarioEstudiante(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"

    def on_start(self):
        self.email    = random_email()
        self.password = "Password123*"

        # Registrar usuario ficticio
        self.client.post("/api/auth/register", json={
            "email":                 self.email,
            "password":              self.password,
            "password_confirmation": self.password,
            "role":                  "student",
        })

        # Login
        res = self.client.post("/api/auth/login", json={
            "email":    self.email,
            "password": self.password,
        })
        self.token = res.json().get("token") if res.status_code == 200 else None
        self.user_id = res.json().get("user", {}).get("id") if res.status_code == 200 else None

    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(3)
    def listar_convocatorias(self):
        self.client.get("/api/convocatorias")

    @task(2)
    def ver_convocatoria(self):
        self.client.get("/api/convocatorias/1", name="/api/convocatorias/[id]")

    @task(2)
    def mis_postulaciones(self):
        self.client.get("/api/mis-postulaciones", headers=self.auth_headers())

    @task(1)
    def ver_perfil(self):
        self.client.get("/api/auth/me", headers=self.auth_headers())

    @task(1)
    def listar_formaciones(self):
        self.client.get("/api/formaciones")

    @task(1)
    def ver_notificaciones(self):
        self.client.get("/api/notificaciones", headers=self.auth_headers())


class UsuarioEmpresa(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"

    def on_start(self):
        self.email    = random_email()
        self.password = "Password123*"

        self.client.post("/api/auth/register", json={
            "email":                 self.email,
            "password":              self.password,
            "password_confirmation": self.password,
            "role":                  "company",
        })

        res = self.client.post("/api/auth/login", json={
            "email":    self.email,
            "password": self.password,
        })
        self.token   = res.json().get("token") if res.status_code == 200 else None
        self.user_id = res.json().get("user", {}).get("id") if res.status_code == 200 else None

    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(3)
    def listar_convocatorias(self):
        self.client.get("/api/convocatorias")

    @task(2)
    def mis_convocatorias(self):
        self.client.get("/api/mis-convocatorias", headers=self.auth_headers())

    @task(2)
    def catalogo_estudiantes(self):
        self.client.get("/api/catalogo/estudiantes", headers=self.auth_headers())

    @task(1)
    def mis_solicitudes(self):
        self.client.get("/api/mis-solicitudes", headers=self.auth_headers())

    @task(1)
    def ver_perfil(self):
        self.client.get("/api/auth/me", headers=self.auth_headers())


class UsuarioUniversidad(HttpUser):
    wait_time = between(2, 4)
    host = "http://localhost:8000"

    def on_start(self):
        self.email    = random_email()
        self.password = "Password123*"

        self.client.post("/api/auth/register", json={
            "email":                 self.email,
            "password":              self.password,
            "password_confirmation": self.password,
            "role":                  "university",
        })

        res = self.client.post("/api/auth/login", json={
            "email":    self.email,
            "password": self.password,
        })
        self.token   = res.json().get("token") if res.status_code == 200 else None
        self.user_id = res.json().get("user", {}).get("id") if res.status_code == 200 else None

    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(3)
    def listar_formaciones(self):
        self.client.get("/api/formaciones")

    @task(2)
    def acuerdos_recibidos(self):
        self.client.get("/api/recibidos", headers=self.auth_headers())

    @task(1)
    def listar_estudiantes(self):
        self.client.get("/api/usuarios/students", headers=self.auth_headers())