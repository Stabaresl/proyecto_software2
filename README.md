# TalentBridge

Plataforma digital basada en arquitectura de microservicios que conecta estudiantes universitarios, empresas, universidades y entidades del Estado. Permite a los estudiantes construir perfiles profesionales y postularse a convocatorias, a las empresas encontrar y contratar talento calificado, a las universidades potenciar la empleabilidad de sus estudiantes, y al Estado impulsar el desarrollo a través de proyectos e investigación.

---

## Arquitectura general

El sistema está compuesto por 6 microservicios independientes que se comunican exclusivamente a través del API Gateway. Ningún cliente externo debe llamar directamente a un microservicio.

```
Cliente (Frontend React :5173)
          │
          ▼
  API Gateway :8000  ← único punto de entrada
          │
          ├──→ ms-usuarios       :8001  (Django + PostgreSQL)
          ├──→ ms-convocatorias  :8002  (Laravel + MySQL)
          ├──→ ms-formacion      :8003  (Flask + MongoDB)
          ├──→ ms-matching       :8004  (Express + MySQL)
          └──→ ms-notificaciones :8005  (Express + MongoDB)
```

| Microservicio | Framework | Base de datos | Puerto |
|---|---|---|---|
| ms-gateway | Laravel | MySQL (tb_gateway) | 8000 |
| ms-usuarios | Django | PostgreSQL (tb_usuarios) | 8001 |
| ms-convocatorias | Laravel | MySQL (tb_convocatorias) | 8002 |
| ms-formacion | Flask | MongoDB (tb_formacion) | 8003 |
| ms-matching | Express | MySQL (tb_matching) | 8004 |
| ms-notificaciones | Express | MongoDB (tb_notificaciones) | 8005 |
| frontend | React + Vite | — | 5173 |

---

## Requisitos previos

Antes de iniciar asegúrate de tener instalado:

- PHP >= 8.2 y Composer
- Python >= 3.10
- Node.js >= 18 y npm
- MySQL >= 8.0
- PostgreSQL >= 14
- MongoDB >= 6.0

---

## Instalación y despliegue

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/talentbridge.git
cd talentbridge
```

### Paso 2 — Crear las bases de datos

**MySQL:**
```bash
mysql -u root -p
```
```sql
CREATE DATABASE tb_gateway CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE tb_convocatorias CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE tb_matching CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

**PostgreSQL:**
```bash
psql -U postgres
```
```sql
CREATE DATABASE tb_usuarios;
\q
```

**MongoDB:** Se crea automáticamente al insertar el primer documento.

---

### Paso 3 — ms-gateway (Laravel · :8000)

```bash
cd ms-gateway
composer install
cp .env.example .env
```

Edita `.env` con tus credenciales:
```env
APP_NAME=TalentBridge-Gateway
APP_ENV=local
APP_KEY=                        # se genera en el siguiente paso
APP_DEBUG=true
APP_URL=http://localhost:8000

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=tb_gateway
DB_USERNAME=root
DB_PASSWORD=tu_password

CACHE_STORE=file
SESSION_DRIVER=file

MS_USUARIOS_URL=http://localhost:8001
MS_CONVOCATORIAS_URL=http://localhost:8002
MS_FORMACION_URL=http://localhost:8003
MS_MATCHING_URL=http://localhost:8004
MS_NOTIFICACIONES_URL=http://localhost:8005
```

```bash
php artisan key:generate
php artisan jwt:secret
php artisan migrate
php artisan serve --port=8000
```

---

### Paso 4 — ms-usuarios (Django · :8001)

```bash
cd ms-usuarios
python -m venv venv
source venv/Scripts/activate    # Windows Git Bash
# source venv/bin/activate       # Linux/Mac
pip install -r requirements.txt
```

Crea el archivo `.env` en la raíz de `ms-usuarios`:
```env
DEBUG=True
SECRET_KEY=django-insecure-talentbridge-usuarios-2024
DB_NAME=tb_usuarios
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=127.0.0.1
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

```bash
python manage.py migrate
python manage.py runserver 8001
```

---

### Paso 5 — ms-convocatorias (Laravel · :8002)

```bash
cd ms-convocatorias
composer install
cp .env.example .env
```

Edita `.env`:
```env
APP_NAME=TalentBridge-Convocatorias
APP_ENV=local
APP_DEBUG=true
APP_URL=http://localhost:8002

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=tb_convocatorias
DB_USERNAME=root
DB_PASSWORD=tu_password

CACHE_STORE=file
SESSION_DRIVER=file

MS_GATEWAY_URL=http://localhost:8000
```

```bash
php artisan key:generate
php artisan jwt:secret
php artisan migrate
php artisan serve --port=8002
```

---

### Paso 6 — ms-formacion (Flask · :8003)

```bash
cd ms-formacion
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

Crea el archivo `.env`:
```env
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=8003
SECRET_KEY=talentbridge-formacion-secret-2024
MONGO_URI=mongodb://localhost:27017/tb_formacion
MS_GATEWAY_URL=http://localhost:8000
```

```bash
python run.py
```

---

### Paso 7 — ms-matching (Express · :8004)

```bash
cd ms-matching
npm install
```

Crea el archivo `.env`:
```env
PORT=8004
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=tb_matching
DB_USER=root
DB_PASSWORD=tu_password
MS_GATEWAY_URL=http://localhost:8000
MS_USUARIOS_URL=http://localhost:8001
```

```bash
npm run dev
```

---

### Paso 8 — ms-notificaciones (Express · :8005)

```bash
cd ms-notificaciones
npm install
```

Crea el archivo `.env`:
```env
PORT=8005
MONGO_URI=mongodb://localhost:27017/tb_notificaciones
MS_GATEWAY_URL=http://localhost:8000
```

```bash
npm run dev
```

---

### Paso 9 — Frontend (React · :5173)

```bash
cd frontend
npm install
```

Crea el archivo `.env`:
```env
VITE_API_URL=http://localhost:8000/api
```

```bash
npm run dev
```

---

## Verificar que todos los servicios están corriendo

Abre 7 terminales simultáneas y ejecuta cada comando en su carpeta correspondiente. Puedes verificar que cada servicio responde correctamente:

```bash
curl http://localhost:8000/api/convocatorias    # Gateway → ms-convocatorias
curl http://localhost:8003/api/formaciones/     # ms-formacion directo
curl http://localhost:8004/api/health           # ms-matching health check
curl http://localhost:8005/api/health           # ms-notificaciones health check
```

---

## Pruebas

### Pruebas unitarias

**ms-gateway (Laravel):**
```bash
cd ms-gateway
php artisan test
```

**ms-convocatorias (Laravel):**
```bash
cd ms-convocatorias
php artisan test
```

**ms-usuarios (Django):**
```bash
cd ms-usuarios
source venv/Scripts/activate
pytest tests/ -v
```

**ms-formacion (Flask):**
```bash
cd ms-formacion
source venv/Scripts/activate
pytest tests/ -v
```

**ms-matching (Express):**
```bash
cd ms-matching
npm test
```

**ms-notificaciones (Express):**
```bash
cd ms-notificaciones
npm test
```

---

### Pruebas de rendimiento

> Asegúrate de tener todos los microservicios corriendo antes de ejecutar las pruebas de rendimiento.

```bash
cd tests-rendimiento
```

**Prueba de capacidad — Fase 1 (10 usuarios):**
```bash
locust -f capacity_test.py --headless --users 10 --spawn-rate 2 --run-time 3m --host http://localhost:8000 --csv=capacity_10
```

**Prueba de capacidad — Fase 2 (25 usuarios):**
```bash
locust -f capacity_test.py --headless --users 25 --spawn-rate 5 --run-time 3m --host http://localhost:8000 --csv=capacity_25
```

**Prueba de capacidad — Fase 3 (50 usuarios):**
```bash
locust -f capacity_test.py --headless --users 50 --spawn-rate 10 --run-time 3m --host http://localhost:8000 --csv=capacity_50
```

**Prueba de carga (50 usuarios, 2 minutos):**
```bash
locust -f load_test.py --headless --users 50 --spawn-rate 5 --run-time 2m --host http://localhost:8000 --csv=resultados_carga
```

**Prueba de estrés (200 usuarios, 3 minutos):**
```bash
locust -f stress_test.py --headless --users 200 --spawn-rate 10 --run-time 3m --host http://localhost:8000 --csv=resultados_estres
```

**Prueba con interfaz visual:**
```bash
locust -f locust.py --host http://localhost:8000
```
Luego abre `http://localhost:8089` en el navegador.

---

## Documentación

- [Documentación de endpoints](docs/endpoints.md) — todos los endpoints con ejemplos de request y response
- [Diagrama de arquitectura](docs/arquitectura.png) — diagrama visual del sistema

---

## Estructura del repositorio

```
talentbridge/
├── ms-gateway/              ← API Gateway (Laravel)
├── ms-usuarios/             ← Microservicio usuarios (Django)
├── ms-convocatorias/        ← Microservicio convocatorias (Laravel)
├── ms-formacion/            ← Microservicio formación (Flask)
├── ms-matching/             ← Microservicio matching (Express)
├── ms-notificaciones/       ← Microservicio notificaciones (Express)
├── frontend/                ← Interfaz de usuario (React + Vite)
├── tests-rendimiento/       ← Pruebas de carga, capacidad y estrés (Locust)
├── docs/
│   ├── endpoints.md         ← Documentación de endpoints
│   └── arquitectura.png     ← Diagrama de arquitectura
└── README.md
```

---

## Actores del sistema

| Actor | Rol | Acciones principales |
|---|---|---|
| Estudiante | Busca oportunidades | Completar perfil, postularse a convocatorias, inscribirse en programas de formación |
| Empresa | Publica oportunidades | Crear convocatorias, explorar catálogo de talento, solicitar programas de formación a universidades |
| Universidad | Gestiona estudiantes | Validar estudiantes, publicar programas de formación, responder acuerdos con empresas |
| Estado | Regula y financia | Publicar proyectos de investigación, becas y retos nacionales, validar instituciones |

---

## Variables de entorno

Cada microservicio requiere su propio archivo `.env`. Los archivos `.env.example` están disponibles en cada carpeta como referencia. **Nunca subas archivos `.env` al repositorio.**
