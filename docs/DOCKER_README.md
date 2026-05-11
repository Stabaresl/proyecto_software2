# TalentBridge — Documentación de Contenerización y Orquestación

**Entrega #2 — Contenerización y Orquestación**  
Plataforma de conexión entre estudiantes, empresas, universidades y entidades del Estado.

---

## Tabla de contenido

1. [Arquitectura de contenedores](#1-arquitectura-de-contenedores)
2. [Requisitos previos](#2-requisitos-previos)
3. [Estructura de archivos Docker](#3-estructura-de-archivos-docker)
4. [Descripción de contenedores](#4-descripción-de-contenedores)
5. [Levantar los contenedores](#5-levantar-los-contenedores)
6. [Verificar el estado](#6-verificar-el-estado)
7. [Comandos de operación](#7-comandos-de-operación)
8. [Probar los servicios](#8-probar-los-servicios)
9. [Ejecutar pruebas unitarias](#9-ejecutar-pruebas-unitarias)
10. [Pruebas de rendimiento](#10-pruebas-de-rendimiento)
11. [Solución de problemas frecuentes](#11-solución-de-problemas-frecuentes)
12. [Variables de entorno](#12-variables-de-entorno)
13. [Notas de seguridad](#13-notas-de-seguridad)

---

## 1. Arquitectura de contenedores

El sistema está compuesto por **13 contenedores** divididos en tres grupos: bases de datos, microservicios y red interna compartida.

```
Host (puertos expuestos al exterior)
│
├── :8000  ms-gateway          → Laravel 11 + JWT  (API Gateway, único punto de entrada)
├── :8001  ms-usuarios         → Django 6 + DRF + PostgreSQL
├── :8002  ms-convocatorias    → Laravel 11 + JWT + MySQL
├── :8003  ms-formacion        → Flask 3 + PyMongo + MongoDB
├── :8004  ms-matching         → Express 5 + Sequelize + MySQL
├── :8005  ms-notificaciones   → Express 5 + Mongoose + MongoDB
│
├── :3310  mysql-gateway        → MySQL 8.0  (base de datos tb_gateway)
├── :3311  mysql-convocatorias  → MySQL 8.0  (base de datos tb_convocatorias)
├── :3312  mysql-matching       → MySQL 8.0  (base de datos tb_matching)
├── :5433  postgres-usuarios    → PostgreSQL 16 (base de datos tb_usuarios)
├── :27017 mongo-formacion      → MongoDB 7.0 (base de datos tb_formacion)
└── :27018 mongo-notificaciones → MongoDB 7.0 (base de datos tb_notificaciones)
```

### Red interna

Todos los contenedores se comunican entre sí a través de la red interna `talentbridge-net` usando sus **nombres de servicio** como hostname. Ningún cliente externo debe llamar directamente a un microservicio — todo pasa por el API Gateway en `:8000`.

```
Cliente externo
      │
      ▼
ms-gateway:8000  ←─── único punto de entrada
      │
      ├──→ ms-usuarios:8001
      ├──→ ms-convocatorias:8002
      ├──→ ms-formacion:8003
      ├──→ ms-matching:8004
      └──→ ms-notificaciones:8005
```

### Orden de arranque

Docker Compose gestiona el orden automáticamente mediante `depends_on` y `healthcheck`:

```
1. Bases de datos (MySQL ×3, PostgreSQL, MongoDB ×2)
2. Microservicios (cada uno espera a que su BD esté healthy)
3. ms-gateway (espera a que todos los microservicios estén listos)
```

---

## 2. Requisitos previos

| Herramienta | Versión mínima | Verificar |
|---|---|---|
| Docker | 24.0 | `docker --version` |
| Docker Compose | 2.20 | `docker compose version` |
| RAM disponible | 4 GB | — |

Instalar Docker: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

> Docker Compose ya viene incluido en Docker Desktop para Windows y Mac.

---

## 3. Estructura de archivos Docker

```
proyecto_software2/
│
├── docker-compose.yml              ← orquestación de los 13 contenedores
├── .env.example                    ← plantilla de variables (copiar a .env)
├── .env                            ← variables reales (NO subir al repo)
│
├── ms-gateway/
│   ├── Dockerfile                  ← PHP 8.3-cli + Composer + SQLite
│   └── docker-entrypoint.sh        ← espera MySQL, genera APP_KEY y JWT secret, migra
│
├── ms_usuarios/                    ← nombre con guión BAJO
│   ├── Dockerfile                  ← Python 3.13-slim + psycopg2
│   └── docker-entrypoint.sh        ← espera PostgreSQL, ejecuta migraciones
│
├── ms-convocatorias/
│   ├── Dockerfile                  ← PHP 8.3-cli + Composer + SQLite
│   └── docker-entrypoint.sh        ← espera MySQL, genera APP_KEY y JWT secret, migra
│
├── ms-formacion/
│   └── Dockerfile                  ← Python 3.13-slim, arranca run.py
│
├── ms-matching/
│   ├── Dockerfile                  ← Node 20-alpine, arranca src/server.js
│   └── docker-entrypoint.sh        ← espera MySQL antes de arrancar Express
│
└── ms-notificaciones/
    └── Dockerfile                  ← Node 20-slim (Debian), arranca src/server.js
```

### ¿Por qué algunos tienen `docker-entrypoint.sh` y otros no?

| Servicio | ¿Tiene entrypoint? | Motivo |
|---|---|---|
| ms-gateway | Sí | Necesita generar APP_KEY, JWT secret y correr migraciones |
| ms-usuarios | Sí | Necesita esperar PostgreSQL activamente y correr migraciones |
| ms-convocatorias | Sí | Igual que ms-gateway |
| ms-formacion | No | Flask conecta Mongo de forma lazy, sin migraciones |
| ms-matching | Sí | Sequelize falla si MySQL no está listo al arrancar |
| ms-notificaciones | No | Mongoose reintenta la conexión automáticamente |

---

## 4. Descripción de contenedores

### Bases de datos

| Contenedor | Imagen | Base de datos | Puerto host |
|---|---|---|---|
| tb_mysql_gateway | mysql:8.0 | tb_gateway | 3310 |
| tb_mysql_convocatorias | mysql:8.0 | tb_convocatorias | 3311 |
| tb_mysql_matching | mysql:8.0 | tb_matching | 3312 |
| tb_postgres_usuarios | postgres:16-alpine | tb_usuarios | 5433 |
| tb_mongo_formacion | mongo:7.0 | tb_formacion | 27017 |
| tb_mongo_notificaciones | mongo:7.0 | tb_notificaciones | 27018 |

> Los puertos del host son distintos a los estándar (3306, 5432, 27017) para evitar conflictos con instalaciones locales existentes.

### Microservicios

| Contenedor | Imagen base | Framework | Puerto |
|---|---|---|---|
| tb_ms_gateway | php:8.3-cli | Laravel 11 | 8000 |
| tb_ms_usuarios | python:3.13-slim | Django 6 + DRF | 8001 |
| tb_ms_convocatorias | php:8.3-cli | Laravel 11 | 8002 |
| tb_ms_formacion | python:3.13-slim | Flask 3 | 8003 |
| tb_ms_matching | node:20-alpine | Express 5 | 8004 |
| tb_ms_notificaciones | node:20-slim | Express 5 | 8005 |

> `ms-notificaciones` usa `node:20-slim` (Debian) en lugar de Alpine porque `mongodb-memory-server` no tiene binarios para Alpine Linux.

---

## 5. Levantar los contenedores

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/Stabaresl/proyecto_software2.git
cd proyecto_software2
```

### Paso 2 — Configurar variables de entorno

```bash
cp .env.example .env
```

El `.env` por defecto funciona para desarrollo. Las claves `APP_KEY` de Laravel se generan automáticamente en el primer arranque.

### Paso 3 — Agregar el JWT secret al `.env`

El gateway necesita un JWT secret fijo para que las sesiones persistan entre reinicios. Agrégalo al `.env`:

```env
MS_GATEWAY_JWT_SECRET=tu_jwt_secret_aqui
```

> Si no tienes un secret generado, puedes usar cualquier cadena aleatoria de 64 caracteres o generarlo con: `openssl rand -base64 48`

Y en el `docker-compose.yml`, en el servicio `ms-gateway` bajo `environment`:

```yaml
JWT_SECRET: ${MS_GATEWAY_JWT_SECRET}
```

### Paso 4 — Construir las imágenes

```bash
docker compose build
```

Este proceso descarga las imágenes base y construye cada microservicio. Puede tardar varios minutos la primera vez.

### Paso 5 — Levantar todos los servicios

```bash
docker compose up -d
```

La bandera `-d` levanta los contenedores en segundo plano (detached mode).

---

## 6. Verificar el estado

```bash
docker compose ps
```

Resultado esperado con todos los servicios funcionando:

```
NAME                       STATUS
tb_mysql_gateway           Up (healthy)
tb_mysql_convocatorias     Up (healthy)
tb_mysql_matching          Up (healthy)
tb_postgres_usuarios       Up (healthy)
tb_mongo_formacion         Up (healthy)
tb_mongo_notificaciones    Up (healthy)
tb_ms_usuarios             Up (healthy)
tb_ms_convocatorias        Up
tb_ms_formacion            Up (healthy)
tb_ms_matching             Up (healthy)
tb_ms_notificaciones       Up (healthy)
tb_ms_gateway              Up
```

### Health checks rápidos

```bash
curl http://localhost:8004/api/health
curl http://localhost:8005/api/health
curl http://localhost:8003/api/formaciones/
```

---

## 7. Comandos de operación

### Ver logs

```bash
# Todos los servicios en tiempo real
docker compose logs -f

# Un servicio específico
docker compose logs -f ms-gateway
docker compose logs -f ms-usuarios
docker compose logs -f ms-matching

# Últimas 50 líneas
docker compose logs --tail=50 ms-gateway
```

### Reiniciar servicios

```bash
# Reiniciar un servicio
docker compose restart ms-matching

# Detener todo (conserva datos en volúmenes)
docker compose down

# Detener y borrar todos los datos
docker compose down -v
```

### Entrar a un contenedor

```bash
docker exec -it tb_ms_gateway bash
docker exec -it tb_ms_usuarios bash
docker exec -it tb_ms_formacion bash
docker exec -it tb_ms_matching sh
```

### Acceso directo a bases de datos

```bash
# MySQL - Gateway
mysql -h 127.0.0.1 -P 3310 -u root -ptalentbridge2024 tb_gateway

# MySQL - Convocatorias
mysql -h 127.0.0.1 -P 3311 -u root -ptalentbridge2024 tb_convocatorias

# MySQL - Matching
mysql -h 127.0.0.1 -P 3312 -u root -ptalentbridge2024 tb_matching

# PostgreSQL - Usuarios
psql -h 127.0.0.1 -p 5433 -U postgres -d tb_usuarios

# MongoDB - Formacion
mongosh --port 27017 tb_formacion

# MongoDB - Notificaciones
mongosh --port 27018 tb_notificaciones
```

### Ejecutar migraciones manualmente

```bash
docker exec tb_ms_gateway php artisan migrate
docker exec tb_ms_convocatorias php artisan migrate
docker exec tb_ms_usuarios python manage.py migrate
```

### Reconstruir desde cero

```bash
docker compose down -v --rmi local
docker compose build --no-cache
docker compose up -d
```

---

## 8. Probar los servicios

**Base URL:** `http://localhost:8000/api`  
**Herramienta recomendada:** Postman, Insomnia o Thunder Client

> Todas las peticiones deben pasar por el API Gateway (`:8000`). No llamar directamente a los microservicios.

### Flujo completo de prueba

#### 1. Registrar un usuario

```
POST http://localhost:8000/api/auth/register
Content-Type: application/json

{
    "email": "estudiante@test.com",
    "password": "Password123*",
    "password_confirmation": "Password123*",
    "role": "student"
}
```

`role` acepta: `student` · `company` · `university` · `state`

**Respuesta exitosa (201):**
```json
{
    "success": true,
    "token": "eyJ0eXAiOiJKV1Qi...",
    "user": { "id": 1, "email": "estudiante@test.com", "role": "student", "status": "active" }
}
```

#### 2. Iniciar sesión

```
POST http://localhost:8000/api/auth/login
Content-Type: application/json

{
    "email": "estudiante@test.com",
    "password": "Password123*"
}
```

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "token": "eyJ0eXAiOiJKV1Qi...",
    "user": { "id": 1, "email": "estudiante@test.com", "role": "student" }
}
```

> Guarda el `token`. Todos los endpoints protegidos lo requieren en el header: `Authorization: Bearer <token>`

#### 3. Endpoints protegidos (requieren token)

```
# Perfil del usuario autenticado
GET http://localhost:8000/api/auth/me

# Listar convocatorias
GET http://localhost:8000/api/convocatorias

# Listar programas de formación
GET http://localhost:8000/api/formaciones/

# Catálogo de estudiantes
GET http://localhost:8000/api/catalogo/estudiantes

# Notificaciones
GET http://localhost:8000/api/notificaciones
```

#### 4. Cerrar sesión

```
POST http://localhost:8000/api/auth/logout
Authorization: Bearer <token>
```

### Resumen de endpoints por microservicio

| Microservicio | Total | Públicos | Protegidos |
|---|---|---|---|
| ms-gateway (Auth) | 6 | 4 | 2 |
| ms-usuarios | 12 | 0 | 12 |
| ms-convocatorias | 10 | 2 | 8 |
| ms-formacion | 9 | 2 | 7 |
| ms-matching | 7 | 0 | 7 |
| ms-notificaciones | 8 | 1 | 7 |
| **Total** | **52** | **9** | **43** |

> La documentación completa de todos los endpoints con ejemplos de request y response está en `docs/endpoints.md`.

---

## 9. Ejecutar pruebas unitarias

Todos los tests corren **dentro de los contenedores** sin afectar los datos de desarrollo, ya que cada suite usa su propia base de datos aislada (SQLite en memoria para Laravel, mocks para Python y Node).

### ms-gateway (Laravel — PHPUnit)

```bash
# Paso previo necesario (solo una vez por sesión):
docker exec tb_ms_gateway bash -c "touch /var/www/ms-gateway/.env"

# Correr tests
docker exec tb_ms_gateway php artisan test --testsuite=Feature
```

**Resultado esperado:**
```
PASS  Tests\Feature\AuthTest
  ✓ register exitoso
  ✓ register falla email duplicado
  ✓ register falla role invalido
  ✓ register falla passwords no coinciden
  ✓ login exitoso
  ✓ login falla credenciales incorrectas
  ✓ login falla cuenta inactiva
  ✓ forgot password email existente
  ✓ forgot password email no existente
  ✓ me requiere autenticacion
  ✓ logout requiere autenticacion

Tests: 11 passed (22 assertions)
```

### ms-convocatorias (Laravel — PHPUnit)

```bash
docker exec tb_ms_convocatorias bash -c "touch /var/www/ms-convocatorias/.env"
docker exec tb_ms_convocatorias php artisan test --testsuite=Feature
```

### ms-usuarios (Django — pytest)

```bash
docker exec tb_ms_usuarios pytest tests/ -v
```

### ms-formacion (Flask — pytest)

```bash
docker exec tb_ms_formacion pytest tests/ -v
```

**Resultado esperado:**
```
tests/test_formacion.py::TestFormaciones::test_listar_formaciones PASSED
tests/test_formacion.py::TestFormaciones::test_crear_formacion_exitosa PASSED
tests/test_formacion.py::TestFormaciones::test_crear_formacion_falla_sin_auth PASSED
tests/test_formacion.py::TestFormaciones::test_crear_formacion_falla_role_incorrecto PASSED
tests/test_formacion.py::TestFormaciones::test_crear_formacion_falla_campos_requeridos PASSED
tests/test_formacion.py::TestFormaciones::test_ver_formacion_no_existente PASSED
tests/test_formacion.py::TestAcuerdos::test_solicitar_acuerdo_exitoso PASSED
tests/test_formacion.py::TestAcuerdos::test_solicitar_acuerdo_falla_role_incorrecto PASSED
tests/test_formacion.py::TestAcuerdos::test_listar_solicitudes_empresa PASSED
tests/test_formacion.py::TestAcuerdos::test_listar_acuerdos_recibidos_universidad PASSED

10 passed in 0.37s
```

### ms-matching (Express — Jest)

```bash
docker exec tb_ms_matching npm test
```

### ms-notificaciones (Express — Jest)

```bash
docker exec tb_ms_notificaciones npm test
```

---

## 10. Pruebas de rendimiento

Con todos los contenedores corriendo, ejecutar desde la carpeta `tests-rendimiento/`:

```bash
pip install locust
cd tests-rendimiento
```

### Pruebas de capacidad

```bash
# Fase 1 — 10 usuarios simultáneos
locust -f capacity_test.py --headless --users 10 --spawn-rate 2 \
  --run-time 3m --host http://localhost:8000 --csv=capacity_10

# Fase 2 — 25 usuarios simultáneos
locust -f capacity_test.py --headless --users 25 --spawn-rate 5 \
  --run-time 3m --host http://localhost:8000 --csv=capacity_25

# Fase 3 — 50 usuarios simultáneos
locust -f capacity_test.py --headless --users 50 --spawn-rate 10 \
  --run-time 3m --host http://localhost:8000 --csv=capacity_50
```

### Prueba de carga

```bash
locust -f load_test.py --headless --users 50 --spawn-rate 5 \
  --run-time 2m --host http://localhost:8000 --csv=resultados_carga
```

### Prueba de estrés

```bash
locust -f stress_test.py --headless --users 200 --spawn-rate 10 \
  --run-time 3m --host http://localhost:8000 --csv=resultados_estres
```

### Interfaz visual

```bash
locust -f locust.py --host http://localhost:8000
```

Luego abrir `http://localhost:8089` en el navegador.

---

## 11. Solución de problemas frecuentes

### Error: `Secret is not set` en el login

El JWT secret de Laravel no está configurado. Agrégalo al `.env` raíz:

```env
MS_GATEWAY_JWT_SECRET=tu_secret_aqui
```

Y en `docker-compose.yml` bajo `ms-gateway > environment`:

```yaml
JWT_SECRET: ${MS_GATEWAY_JWT_SECRET}
```

Luego reinicia sin reconstruir:

```bash
docker compose down
docker compose up -d
```

### Error: `file_get_contents(.env): Failed to open stream` en los tests de Laravel

El archivo `.env` no existe dentro del contenedor. Créalo vacío:

```bash
# ms-gateway
docker exec tb_ms_gateway bash -c "touch /var/www/ms-gateway/.env"

# ms-convocatorias
docker exec tb_ms_convocatorias bash -c "touch /var/www/ms-convocatorias/.env"
```

### Error: `no such service: ms_usuarios`

El nombre del servicio en `docker-compose.yml` usa guión normal, no guión bajo:

```bash
# ❌ Incorrecto
docker compose logs ms_usuarios

# ✅ Correcto
docker compose logs ms-usuarios
```

### Error: `Unknown/unsupported linux "alpine"` en tests de notificaciones

`mongodb-memory-server` no soporta Alpine Linux. El `Dockerfile` de `ms-notificaciones` debe usar `node:20-slim` en lugar de `node:20-alpine`. Reconstruye:

```bash
docker compose build ms-notificaciones
```

### Un servicio queda en estado `unhealthy`

```bash
# Ver qué está fallando
docker compose logs ms-matching

# Forzar reinicio
docker compose restart ms-matching
```

### Permisos denegados en storage/ (Laravel)

```bash
docker exec tb_ms_gateway chmod -R 775 storage bootstrap/cache
docker exec tb_ms_convocatorias chmod -R 775 storage bootstrap/cache
```

### Puerto ya en uso en el host

Edita `docker-compose.yml` cambiando el puerto externo (lado izquierdo):

```yaml
ports:
  - "3320:3306"   # en vez de "3310:3306"
```

### Reset completo del entorno

```bash
docker compose down -v --rmi local
docker compose build --no-cache
docker compose up -d
```

---

## 12. Variables de entorno

El archivo `.env` raíz controla todas las contraseñas e inyecta los valores a todos los contenedores. Los `.env` individuales de cada microservicio solo aplican cuando se corre sin Docker.

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `MYSQL_ROOT_PASSWORD` | Contraseña root para las 3 instancias MySQL | `talentbridge2024` |
| `POSTGRES_USER` | Usuario PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | Contraseña PostgreSQL | `talentbridge2024` |
| `MS_GATEWAY_APP_KEY` | Clave de cifrado Laravel gateway | *(se genera automáticamente)* |
| `MS_CONVOCATORIAS_APP_KEY` | Clave de cifrado Laravel convocatorias | *(se genera automáticamente)* |
| `MS_GATEWAY_JWT_SECRET` | Secret para firmar tokens JWT | *(requerido, definir manualmente)* |
| `DJANGO_SECRET_KEY` | Clave secreta Django | `django-insecure-...` |
| `FLASK_SECRET_KEY` | Clave secreta Flask | `talentbridge-formacion-...` |
| `EMAIL_HOST` | Servidor SMTP para notificaciones | *(vacío = modo simulado)* |
| `EMAIL_USER` | Usuario SMTP | *(vacío)* |
| `EMAIL_PASS` | Contraseña SMTP | *(vacío)* |

> Si `EMAIL_HOST` está vacío, `ms-notificaciones` simula el envío de emails imprimiendo en consola. No hay error, simplemente no envía emails reales.

---

## 13. Notas de seguridad

Las siguientes recomendaciones aplican especialmente para entornos de producción:

- Cambiar **todas** las contraseñas del `.env.example` antes de desplegar.
- El archivo `.env` nunca debe subirse al repositorio. Verificar que está en `.gitignore`.
- Eliminar la sección `ports` de cada base de datos en `docker-compose.yml` para no exponerlas al host en producción.
- Usar `APP_DEBUG=false` en los servicios Laravel, `DEBUG=False` en Django y `FLASK_DEBUG=False` en Flask.
- Generar claves fuertes con: `openssl rand -base64 48`
- Rotar el `JWT_SECRET` periódicamente (invalida todos los tokens activos).
- En producción, usar un reverse proxy (Nginx o Traefik) con HTTPS delante del gateway.