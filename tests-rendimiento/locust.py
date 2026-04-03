from locust import HttpUser, task, between
import random
import string

def random_email():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{suffix}@locust.com"


class UsuarioEstudiante(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"

    def on_start(self):
        self.email               = random_email()
        self.password            = "Password123*"
        self.token               = None
        self.user_id             = None
        self.convocatoria_activa_id = None

        reg = self.client.post("/api/auth/register", json={
            "email":                 self.email,
            "password":              self.password,
            "password_confirmation": self.password,
            "role":                  "student",
        }, timeout=30)

        if reg.status_code == 201:
            res = self.client.post("/api/auth/login", json={
                "email":    self.email,
                "password": self.password,
            }, timeout=30)
            if res.status_code == 200:
                self.token   = res.json().get("token")
                self.user_id = res.json().get("user", {}).get("id")

                conv_res = self.client.get("/api/convocatorias?estado=activa", timeout=30)
                if conv_res.status_code == 200:
                    data = conv_res.json().get("data", [])
                    if data:
                        self.convocatoria_activa_id = data[0].get("id")

    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(3)
    def listar_convocatorias(self):
        self.client.get("/api/convocatorias", timeout=30)

    @task(2)
    def ver_convocatoria(self):
        if not self.convocatoria_activa_id:
            return
        self.client.get(
            f"/api/convocatorias/{self.convocatoria_activa_id}",
            name="/api/convocatorias/[id]",
            timeout=30,
        )

    @task(2)
    def mis_postulaciones(self):
        if not self.token:
            return
        self.client.get("/api/mis-postulaciones", headers=self.auth_headers(), timeout=30)

    @task(1)
    def postularse(self):
        if not self.token or not self.convocatoria_activa_id:
            return
        self.client.post(
            f"/api/convocatorias/{self.convocatoria_activa_id}/postular",
            name="/api/convocatorias/[id]/postular",
            headers=self.auth_headers(),
            json={"carta_presentacion": "Postulación de prueba de carga."},
            timeout=30,
        )

    @task(1)
    def ver_perfil(self):
        if not self.token:
            return
        self.client.get("/api/auth/me", headers=self.auth_headers(), timeout=30)

    @task(1)
    def listar_formaciones(self):
        self.client.get("/api/formaciones", timeout=30)

    @task(1)
    def ver_notificaciones(self):
        if not self.token:
            return
        self.client.get("/api/notificaciones", headers=self.auth_headers(), timeout=30)

    @task(1)
    def contar_no_leidas(self):
        if not self.token:
            return
        self.client.get("/api/notificaciones/no-leidas/count", headers=self.auth_headers(), timeout=30)

    @task(1)
    def ver_preferencias_notificaciones(self):
        if not self.token:
            return
        self.client.get("/api/notificaciones/preferencias", headers=self.auth_headers(), timeout=30)


class UsuarioEmpresa(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"

    def on_start(self):
        self.email              = random_email()
        self.password           = "Password123*"
        self.token              = None
        self.user_id            = None
        self.mi_convocatoria_id = None

        reg = self.client.post("/api/auth/register", json={
            "email":                 self.email,
            "password":              self.password,
            "password_confirmation": self.password,
            "role":                  "company",
        }, timeout=30)

        if reg.status_code == 201:
            res = self.client.post("/api/auth/login", json={
                "email":    self.email,
                "password": self.password,
            }, timeout=30)
            if res.status_code == 200:
                self.token   = res.json().get("token")
                self.user_id = res.json().get("user", {}).get("id")

                conv = self.client.post("/api/convocatorias", headers=self.auth_headers(), json={
                    "titulo":       "Convocatoria de prueba de carga",
                    "descripcion":  "Generada automáticamente por Locust",
                    "tipo":         "practica",
                    "cupos":        5,
                    "fecha_inicio": "2026-05-01",
                    "fecha_cierre": "2026-08-01",
                }, timeout=30)

                if conv.status_code == 201:
                    self.mi_convocatoria_id = conv.json().get("data", {}).get("id")
                    if self.mi_convocatoria_id:
                        self.client.patch(
                            f"/api/convocatorias/{self.mi_convocatoria_id}/estado",
                            headers=self.auth_headers(),
                            json={"estado": "activa"},
                            timeout=30,
                        )

    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(3)
    def listar_convocatorias(self):
        self.client.get("/api/convocatorias", timeout=30)

    @task(2)
    def mis_convocatorias(self):
        if not self.token:
            return
        self.client.get("/api/mis-convocatorias", headers=self.auth_headers(), timeout=30)

    @task(2)
    def catalogo_estudiantes(self):
        if not self.token:
            return
        self.client.get("/api/catalogo/estudiantes", headers=self.auth_headers(), timeout=30)

    @task(2)
    def ver_postulaciones_convocatoria(self):
        if not self.token or not self.mi_convocatoria_id:
            return
        self.client.get(
            f"/api/convocatorias/{self.mi_convocatoria_id}/postulaciones",
            name="/api/convocatorias/[id]/postulaciones",
            headers=self.auth_headers(),
            timeout=30,
        )

    @task(1)
    def crear_convocatoria(self):
        if not self.token:
            return
        conv = self.client.post("/api/convocatorias", headers=self.auth_headers(), json={
            "titulo":       "Convocatoria adicional de carga",
            "descripcion":  "Generada por Locust en task",
            "tipo":         "empleo",
            "cupos":        3,
            "fecha_inicio": "2026-05-01",
            "fecha_cierre": "2026-08-01",
        }, timeout=30)
        if conv.status_code == 201:
            nuevo_id = conv.json().get("data", {}).get("id")
            if nuevo_id and not self.mi_convocatoria_id:
                self.mi_convocatoria_id = nuevo_id

    @task(1)
    def solicitar_acuerdo(self):
        if not self.token:
            return
        self.client.post("/api/acuerdos", headers=self.auth_headers(), json={
            "universidad_user_id": 3,
            "titulo":              "Acuerdo de prueba de carga",
            "descripcion":         "Generado por Locust",
            "duracion_semanas":    8,
            "perfil_estudiante":   "Ingeniería de Sistemas",
        }, timeout=30)

    @task(1)
    def mis_solicitudes(self):
        if not self.token:
            return
        self.client.get("/api/mis-solicitudes", headers=self.auth_headers(), timeout=30)

    @task(1)
    def sugerir_candidatos(self):
        if not self.token:
            return
        self.client.post("/api/matching/sugerir", headers=self.auth_headers(), json={
            "habilidades":    ["Python", "React"],
            "disponibilidad": "part_time",
        }, timeout=30)

    @task(1)
    def agregar_favorito(self):
        if not self.token:
            return
        self.client.post("/api/catalogo/favoritos", headers=self.auth_headers(), json={
            "estudiante_user_id": 1,
            "nota":               "Perfil interesante",
        }, timeout=30)

    @task(1)
    def listar_favoritos(self):
        if not self.token:
            return
        self.client.get("/api/catalogo/favoritos", headers=self.auth_headers(), timeout=30)

    @task(1)
    def ver_perfil(self):
        if not self.token:
            return
        self.client.get("/api/auth/me", headers=self.auth_headers(), timeout=30)


class UsuarioUniversidad(HttpUser):
    wait_time = between(2, 4)
    host = "http://localhost:8000"

    def on_start(self):
        self.email    = random_email()
        self.password = "Password123*"
        self.token    = None
        self.user_id  = None

        reg = self.client.post("/api/auth/register", json={
            "email":                 self.email,
            "password":              self.password,
            "password_confirmation": self.password,
            "role":                  "university",
        }, timeout=30)

        if reg.status_code == 201:
            res = self.client.post("/api/auth/login", json={
                "email":    self.email,
                "password": self.password,
            }, timeout=30)
            if res.status_code == 200:
                self.token   = res.json().get("token")
                self.user_id = res.json().get("user", {}).get("id")

    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(3)
    def listar_formaciones(self):
        self.client.get("/api/formaciones", timeout=30)

    @task(2)
    def acuerdos_recibidos(self):
        if not self.token:
            return
        self.client.get("/api/recibidos", headers=self.auth_headers(), timeout=30)

    @task(2)
    def crear_formacion(self):
        if not self.token:
            return
        self.client.post("/api/formaciones", headers=self.auth_headers(), json={
            "titulo":              "Bootcamp de prueba de carga",
            "descripcion":         "Generado por Locust",
            "tipo":                "bootcamp",
            "modalidad":           "virtual",
            "duracion_semanas":    8,
            "universidad_user_id": self.user_id or 3,
        }, timeout=30)

    @task(1)
    def listar_estudiantes(self):
        if not self.token:
            return
        self.client.get("/api/usuarios/students", headers=self.auth_headers(), timeout=30)

    @task(1)
    def listar_universidades(self):
        if not self.token:
            return
        self.client.get("/api/usuarios/universities", headers=self.auth_headers(), timeout=30)

    @task(1)
    def ver_notificaciones(self):
        if not self.token:
            return
        self.client.get("/api/notificaciones", headers=self.auth_headers(), timeout=30)

    @task(1)
    def ver_perfil(self):
        if not self.token:
            return
        self.client.get("/api/auth/me", headers=self.auth_headers(), timeout=30)