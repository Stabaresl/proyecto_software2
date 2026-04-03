# TalentBridge — Documentación de Endpoints

**Base URL:** `http://localhost:8000/api`  
**Autenticación:** Header `Authorization: Bearer <token>`

> ⚠️ **Importante:** Todas las peticiones deben pasar por el API Gateway (`:8000`). No se debe llamar directamente a ningún microservicio.

---

## Orden recomendado para pruebas

Para evitar errores por dependencias entre endpoints, sigue este orden:

1. Registrar los 4 usuarios (student, company, university, state)
2. Login con cada uno y guardar sus tokens
3. Crear la universidad en `ms-usuarios`
4. Crear los perfiles de cada actor
5. Sincronizar perfil del estudiante en el catálogo
6. Crear y activar una convocatoria (company o state)
7. Postularse a la convocatoria (student)
8. Gestionar postulaciones (company o state)
9. Solicitar y responder acuerdos
10. Registrar certificaciones
11. Probar notificaciones

---

## 1. AUTH — ms-gateway (Laravel · :8000)

### POST `/auth/register`
Registra un nuevo usuario. **No requiere autenticación.**

```json
{
    "email": "estudiante@test.com",
    "password": "Password123*",
    "password_confirmation": "Password123*",
    "role": "student"
}
```

> Registra los 4 actores usando estos bodies:

```json
{ "email": "empresa@test.com", "password": "Password123*", "password_confirmation": "Password123*", "role": "company" }
```
```json
{ "email": "universidad@test.com", "password": "Password123*", "password_confirmation": "Password123*", "role": "university" }
```
```json
{ "email": "estado@test.com", "password": "Password123*", "password_confirmation": "Password123*", "role": "state" }
```

> `role` acepta: `student` · `company` · `university` · `state`

**Respuesta exitosa (201):**
```json
{
    "success": true,
    "message": "Usuario registrado correctamente.",
    "token": "eyJ0eXAiOiJKV1Qi...",
    "user": { "id": 1, "email": "estudiante@test.com", "role": "student", "status": "active" }
}
```

---

### POST `/auth/login`
Inicia sesión. **No requiere autenticación.**

```json
{
    "email": "estudiante@test.com",
    "password": "Password123*"
}
```

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "message": "Login exitoso.",
    "token": "eyJ0eXAiOiJKV1Qi...",
    "user": { "id": 1, "email": "estudiante@test.com", "role": "student", "status": "active" }
}
```

> Guarda el token — lo necesitarás en todos los endpoints protegidos como `Authorization: Bearer <token>`

---

### GET `/auth/me`
Perfil del usuario autenticado. ✅ **Auth requerida.**

> Sin body.

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "user": { "id": 1, "email": "estudiante@test.com", "role": "student", "status": "active", "created_at": "2026-04-01T00:00:00Z" }
}
```

---

### POST `/auth/logout`
Cierra la sesión. ✅ **Auth requerida.**

> Sin body. El token queda invalidado en la blacklist.

**Respuesta exitosa (200):**
```json
{ "success": true, "message": "Sesión cerrada correctamente." }
```

---

### POST `/auth/forgot-password`
Solicita recuperación de contraseña. **No requiere autenticación.**

```json
{ "email": "estudiante@test.com" }
```

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "message": "Si el correo existe, recibirás instrucciones para restablecer tu contraseña.",
    "dev_token": "abc123xyz..."
}
```

> `dev_token` solo aparece en entorno `local`. Cópialo para el siguiente endpoint.

---

### POST `/auth/reset-password`
Restablece la contraseña. **No requiere autenticación.**

> Prerequisito: haber llamado `forgot-password` y copiar el `dev_token`.

```json
{
    "email": "estudiante@test.com",
    "token": "token_copiado_del_dev_token",
    "password": "NuevoPassword123*",
    "password_confirmation": "NuevoPassword123*"
}
```

**Respuesta exitosa (200):**
```json
{ "success": true, "message": "Contraseña restablecida correctamente." }
```

---

## 2. USUARIOS — ms-usuarios (Django · PostgreSQL · :8001)

> Todos los endpoints requieren ✅ **Auth**.  
> Se acceden como `/api/usuarios/{path}` a través del gateway.

---

### POST `/usuarios/universities`
Crea una universidad. ✅ **Auth requerida.**

> Prerrequisito: estar autenticado con cualquier rol.

```json
{
    "name": "Universidad Nacional de Colombia",
    "programs": ["Ingeniería de Sistemas", "Medicina", "Derecho"],
    "research_groups": ["Grupo de IA", "Semillero de Ciberseguridad"]
}
```

**Respuesta exitosa (201):**
```json
{
    "success": true,
    "data": { "id": 1, "name": "Universidad Nacional de Colombia", "programs": [...], "research_groups": [...] }
}
```

> Guarda el `id` de la universidad — lo necesitarás al crear el perfil de estudiante y los acuerdos.

---

### GET `/usuarios/universities`
Lista todas las universidades. ✅ **Auth requerida.**

> Sin body.

---

### GET `/usuarios/universities/{id}`
Obtiene una universidad. ✅ **Auth requerida.**

> `{id}` es el id interno de PostgreSQL.  
> Ejemplo: `/api/usuarios/universities/1`

---

### PUT `/usuarios/universities/{id}/update`
Actualiza una universidad. ✅ **Auth requerida.**

```json
{
    "programs": ["Ingeniería de Sistemas", "Medicina", "Derecho", "Economía"]
}
```

---

### POST `/usuarios/profiles`
Crea el perfil de un actor. ✅ **Auth requerida.**

> El `gateway_user_id` debe ser el `id` que devolvió el register/login del actor correspondiente.

**Perfil estudiante** — usar token de `student`. El `university` debe ser el `id` de una universidad existente en PostgreSQL:
```json
{
    "role": "student",
    "gateway_user_id": 1,
    "first_name": "Santiago",
    "last_name": "García",
    "phone": "3001234567",
    "university": 1,
    "academic_info": {
        "career": "Ingeniería de Sistemas",
        "semester": 7,
        "gpa": 4.2
    },
    "skills": ["Python", "Django", "JavaScript", "React"],
    "certifications": ["AWS Cloud Practitioner"],
    "languages": [
        { "lang": "Español", "level": "nativo" },
        { "lang": "Inglés", "level": "B2" }
    ],
    "availability": "part_time",
    "portfolio_url": "https://github.com/santiago"
}
```

> `availability` acepta: `full_time` · `part_time` · `weekends` · `remote`

**Perfil empresa** — usar token de `company`:
```json
{
    "role": "company",
    "gateway_user_id": 2,
    "name": "Tech Solutions SAS",
    "sector": "Tecnología",
    "size": "small",
    "description": "Empresa de desarrollo de software",
    "website": "https://techsolutions.com"
}
```

> `size` acepta: `micro` · `small` · `medium` · `large`

**Perfil universidad** — usar token de `university`:
```json
{
    "role": "university",
    "gateway_user_id": 3,
    "name": "Universidad Nacional de Colombia",
    "programs": ["Ingeniería de Sistemas"],
    "research_groups": ["Grupo de IA"]
}
```

**Perfil estado** — usar token de `state`:
```json
{
    "role": "state",
    "gateway_user_id": 4,
    "name": "Minciencias",
    "description": "Ministerio de Ciencia, Tecnología e Innovación"
}
```

---

### GET `/usuarios/students`
Lista todos los estudiantes. ✅ **Auth requerida.**

> Sin body.

---

### GET `/usuarios/students/{gateway_user_id}`
Obtiene el perfil de un estudiante. ✅ **Auth requerida.**

> `{gateway_user_id}` es el `id` del usuario en el gateway.  
> Ejemplo: `/api/usuarios/students/1`

---

### PUT `/usuarios/students/{gateway_user_id}/update`
Actualiza el perfil de un estudiante. ✅ **Auth requerida.**

> Prerrequisito: el perfil del estudiante debe existir.

```json
{
    "skills": ["Python", "Django", "React", "Docker"],
    "availability": "full_time",
    "academic_info": { "career": "Ingeniería de Sistemas", "semester": 8, "gpa": 4.5 }
}
```

---

### GET `/usuarios/companies`
Lista todas las empresas. ✅ **Auth requerida.**

> Sin body.

---

### GET `/usuarios/companies/{gateway_user_id}`
Obtiene el perfil de una empresa. ✅ **Auth requerida.**

> Ejemplo: `/api/usuarios/companies/2`

---

### PUT `/usuarios/companies/{gateway_user_id}/update`
Actualiza el perfil de una empresa. ✅ **Auth requerida.**

```json
{
    "sector": "Fintech",
    "size": "medium",
    "description": "Empresa de tecnología financiera"
}
```

---

### GET `/usuarios/government-entities`
Lista todas las entidades gubernamentales. ✅ **Auth requerida.**

> Sin body.

---

### GET `/usuarios/government-entities/{gateway_user_id}`
Obtiene el perfil de una entidad gubernamental. ✅ **Auth requerida.**

> Ejemplo: `/api/usuarios/government-entities/4`

---

### PUT `/usuarios/government-entities/{gateway_user_id}/update`
Actualiza una entidad gubernamental. ✅ **Auth requerida.**

```json
{
    "description": "Ministerio de Ciencia, Tecnología e Innovación de Colombia",
    "authorized": true
}
```

---

## 3. CONVOCATORIAS — ms-convocatorias (Laravel · MySQL · :8002)

---

### GET `/convocatorias`
Lista todas las convocatorias. **No requiere autenticación.**

> Sin body. Soporta filtros:
> - `/convocatorias?tipo=practica`
> - `/convocatorias?estado=activa`
> - `/convocatorias?publicador_tipo=company`

---

### GET `/convocatorias/{id}`
Obtiene una convocatoria. **No requiere autenticación.**

> `{id}` es el id de MySQL.  
> Ejemplo: `/api/convocatorias/1`

---

### POST `/convocatorias`
Crea una convocatoria. ✅ **Auth requerida** (solo `company` o `state`).

> Las convocatorias se crean en estado `borrador`. Debes cambiar el estado a `activa` para que los estudiantes puedan postularse.

```json
{
    "titulo": "Práctica en Desarrollo Web",
    "descripcion": "Buscamos estudiantes de sistemas para práctica profesional en desarrollo frontend y backend.",
    "tipo": "practica",
    "cupos": 3,
    "fecha_inicio": "2026-04-10",
    "fecha_cierre": "2026-06-10",
    "requisitos": {
        "semestre_minimo": 6,
        "carrera": "Ingeniería de Sistemas",
        "habilidades": ["JavaScript", "React"]
    },
    "condiciones": {
        "duracion_meses": 6,
        "modalidad": "hibrida",
        "remuneracion": true
    }
}
```

> `tipo` acepta: `practica` · `empleo` · `proyecto` · `beca` · `reto_nacional` · `investigacion`

**Respuesta exitosa (201):**
```json
{
    "success": true,
    "message": "Convocatoria creada.",
    "data": { "id": 1, "titulo": "Práctica en Desarrollo Web", "estado": "borrador", "..." : "..." }
}
```

> Guarda el `id` — lo necesitarás para cambiar el estado y recibir postulaciones.

---

### PATCH `/convocatorias/{id}/estado`
Cambia el estado de una convocatoria. ✅ **Auth requerida.**

> Solo el usuario que creó la convocatoria puede cambiar su estado.  
> **Debes activar la convocatoria antes de que los estudiantes puedan postularse.**

```json
{ "estado": "activa" }
```

> `estado` acepta: `borrador` · `activa` · `pausada` · `cerrada`

---

### PUT `/convocatorias/{id}`
Actualiza una convocatoria. ✅ **Auth requerida.**

> Solo el creador puede editarla.

```json
{
    "titulo": "Práctica en Desarrollo Web y Mobile",
    "cupos": 5,
    "fecha_cierre": "2026-07-10"
}
```

---

### GET `/mis-convocatorias`
Lista las convocatorias del usuario autenticado. ✅ **Auth requerida** (solo `company` o `state`).

> Sin body.

---

### POST `/convocatorias/{id}/postular`
Postularse a una convocatoria. ✅ **Auth requerida** (solo `student`).

> **Prerrequisitos:**
> - La convocatoria debe estar en estado `activa`
> - La convocatoria debe tener cupos disponibles
> - El estudiante no puede postularse dos veces a la misma convocatoria

```json
{
    "carta_presentacion": "Soy estudiante de séptimo semestre con experiencia en React y Node.js. Me interesa esta práctica porque...",
    "documentos": [
        { "nombre": "Hoja de Vida", "url": "https://drive.google.com/mi-cv", "tipo": "cv" },
        { "nombre": "Carta de Presentación", "url": "https://drive.google.com/mi-carta", "tipo": "carta" }
    ]
}
```

> `tipo` de documento acepta: `cv` · `carta` · `certificado` · `otro`

---

### GET `/mis-postulaciones`
Lista las postulaciones del estudiante autenticado. ✅ **Auth requerida** (solo `student`).

> Sin body.

---

### GET `/convocatorias/{id}/postulaciones`
Lista las postulaciones de una convocatoria. ✅ **Auth requerida.**

> Solo el publicador de esa convocatoria puede ver sus postulaciones.  
> Ejemplo: `/api/convocatorias/1/postulaciones`

---

### PATCH `/postulaciones/{id}/estado`
Cambia el estado de una postulación. ✅ **Auth requerida.**

> Solo el publicador de la convocatoria puede cambiar el estado.  
> El `{id}` es el id de la postulación en MySQL.

```json
{ "estado": "preseleccionado" }
```

> `estado` acepta: `en_revision` · `preseleccionado` · `seleccionado` · `rechazado`

---

## 4. FORMACIÓN — ms-formacion (Flask · MongoDB · :8003)

---

### GET `/formaciones`
Lista todos los programas de formación. **No requiere autenticación.**

> Sin body. Soporta filtros:
> - `/formaciones?tipo=bootcamp`
> - `/formaciones?modalidad=virtual`
> - `/formaciones?universidad_user_id=3`
> - `/formaciones?estado=publicado`

---

### GET `/formaciones/{_id}`
Obtiene un programa por su `_id` de MongoDB. **No requiere autenticación.**

> Ejemplo: `/api/formaciones/69cc8643c558312e4f32a99b`

---

### POST `/formaciones`
Crea un programa de formación. ✅ **Auth requerida** (solo `university`).

> El `universidad_user_id` debe ser el `gateway_user_id` de la universidad autenticada.

```json
{
    "titulo": "Bootcamp de Ciberseguridad",
    "descripcion": "Programa intensivo de 12 semanas en ciberseguridad ofensiva y defensiva.",
    "tipo": "bootcamp",
    "modalidad": "virtual",
    "duracion_semanas": 12,
    "universidad_user_id": 3,
    "requisitos_ingreso": ["Conocimientos básicos de redes", "Python básico"],
    "costo": 0.0,
    "condiciones_garantia": [
        "El estudiante no puede abandonar el programa antes de la semana 8",
        "Asistencia mínima del 90%"
    ]
}
```

> `tipo` acepta: `curso` · `diplomado` · `bootcamp` · `certificacion`  
> `modalidad` acepta: `presencial` · `virtual` · `hibrida`

**Respuesta exitosa (201):**
```json
{
    "success": true,
    "message": "Programa creado.",
    "data": { "_id": "69cc8643c558312e4f32a99b", "titulo": "Bootcamp de Ciberseguridad", "estado": "borrador" }
}
```

> Guarda el `_id` — lo necesitarás para actualizarlo y registrar certificaciones.

---

### PUT `/formaciones/{_id}`
Actualiza un programa. ✅ **Auth requerida** (solo la universidad que lo creó).

> Prerrequisito: el programa debe existir y el usuario autenticado debe ser quien lo creó.

```json
{
    "estado": "publicado",
    "costo": 150000,
    "condiciones_garantia": ["Asistencia mínima del 85%"]
}
```

> `estado` acepta: `borrador` · `publicado` · `cerrado`

---

### POST `/formaciones/certificaciones`
Registra una certificación obtenida por un estudiante. ✅ **Auth requerida** (solo `university`).

> **Prerrequisitos:**
> - El programa debe existir (usar el `_id` de MongoDB)
> - El `estudiante_user_id` debe ser el `gateway_user_id` del estudiante

```json
{
    "estudiante_user_id": 1,
    "formacion_id": "69cc8643c558312e4f32a99b",
    "nombre_certificacion": "Ciberseguridad Ofensiva - Nivel Básico",
    "fecha_obtencion": "2026-03-30"
}
```

---

### GET `/formaciones/certificaciones/{estudiante_user_id}`
Lista las certificaciones de un estudiante. ✅ **Auth requerida.**

> `{estudiante_user_id}` es el `gateway_user_id` del estudiante.  
> Ejemplo: `/api/formaciones/certificaciones/1`

---

### POST `/acuerdos`
Solicita un acuerdo de formación a una universidad. ✅ **Auth requerida** (solo `company`).

> El `universidad_user_id` debe ser el `gateway_user_id` de una universidad existente en el gateway.

```json
{
    "universidad_user_id": 3,
    "titulo": "Programa de Formación en Desarrollo Web",
    "descripcion": "Necesitamos estudiantes formados en React y Node.js para vincularlos en prácticas al finalizar.",
    "habilidades_requeridas": ["React", "Node.js", "MySQL"],
    "duracion_semanas": 10,
    "perfil_estudiante": "Estudiantes de ingeniería de sistemas de semestre 6 en adelante",
    "condiciones": [
        "La universidad garantiza que los estudiantes no abandonarán el programa",
        "Certificación al finalizar"
    ]
}
```

**Respuesta exitosa (201):**
```json
{
    "success": true,
    "message": "Solicitud enviada.",
    "data": { "_id": "69cc8643c558312e4f32a99c", "estado": "pendiente", "..." : "..." }
}
```

> Guarda el `_id` — la universidad lo necesita para responder el acuerdo.

---

### GET `/mis-solicitudes`
Lista los acuerdos solicitados por la empresa autenticada. ✅ **Auth requerida** (solo `company`).

> Sin body.

---

### GET `/recibidos`
Lista los acuerdos recibidos por la universidad autenticada. ✅ **Auth requerida** (solo `university`).

> Sin body.

---

### PATCH `/acuerdos/{_id}/responder`
Responde a un acuerdo. ✅ **Auth requerida** (solo la universidad receptora).

> **Prerrequisitos:**
> - El acuerdo debe estar en estado `pendiente`
> - El `{_id}` es el `_id` del acuerdo en MongoDB
> - Solo la universidad que recibió el acuerdo puede responderlo

```json
{
    "accion": "aceptar",
    "respuesta": "Aceptamos la solicitud. El programa iniciará el 15 de abril."
}
```

> `accion` acepta: `aceptar` · `rechazar`

---

## 5. MATCHING — ms-matching (Express · MySQL · :8004)

---

### POST `/catalogo/perfil`
Sincroniza el perfil del usuario en el catálogo de matching. ✅ **Auth requerida** (cualquier rol).

> Debe llamarse después de crear o actualizar el perfil en `ms-usuarios` para que el catálogo quede actualizado. El `gateway_user_id` y el `role` se toman automáticamente del token.

```json
{
    "universidad": "Universidad Nacional de Colombia",
    "carrera": "Ingeniería de Sistemas",
    "semestre": 7,
    "habilidades": ["Python", "Django", "JavaScript", "React"],
    "idiomas": ["Español", "Inglés B2"],
    "disponibilidad": "part_time",
    "promedio": 4.2,
    "ubicacion": "Bogotá",
    "certificaciones": ["AWS Cloud Practitioner"]
}
```

---

### GET `/catalogo/estudiantes`
Lista estudiantes del catálogo con filtros. ✅ **Auth requerida** (solo `company`, `state` o `university`).

> Sin body. Soporta filtros:
> - `/catalogo/estudiantes?habilidad=Python`
> - `/catalogo/estudiantes?universidad=Nacional`
> - `/catalogo/estudiantes?disponibilidad=part_time`
> - `/catalogo/estudiantes?semestre_min=6`
> - `/catalogo/estudiantes?promedio_min=3.5`
> - `/catalogo/estudiantes?ubicacion=Bogotá`

---

### GET `/catalogo/estudiantes/{gateway_user_id}`
Obtiene el perfil de catálogo de un estudiante. ✅ **Auth requerida.**

> Prerrequisito: el estudiante debe haber sincronizado su perfil con `POST /catalogo/perfil`.  
> Ejemplo: `/api/catalogo/estudiantes/1`

---

### POST `/matching/sugerir`
Sugiere candidatos según criterios. ✅ **Auth requerida** (solo `company` o `state`).

> El algoritmo calcula un score de 0 a 100 por estudiante según coincidencia de habilidades, disponibilidad, semestre y promedio.

```json
{
    "habilidades": ["Python", "React", "Django"],
    "disponibilidad": "part_time",
    "semestre_minimo": 5,
    "promedio_minimo": 3.5
}
```

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "total": 2,
    "data": [
        { "perfil": { "id": 1, "carrera": "Ingeniería de Sistemas", "habilidades": ["Python", "React"] }, "score": 85 },
        { "perfil": { "id": 2, "carrera": "Ingeniería de Sistemas", "habilidades": ["Python"] }, "score": 50 }
    ]
}
```

---

### POST `/catalogo/favoritos`
Agrega un estudiante a favoritos. ✅ **Auth requerida** (solo `company`).

> El `estudiante_user_id` es el `gateway_user_id` del estudiante.  
> Prerrequisito: el estudiante debe existir en el catálogo.

```json
{
    "estudiante_user_id": 1,
    "nota": "Perfil muy completo, contactar para la práctica de desarrollo web."
}
```

---

### GET `/catalogo/favoritos`
Lista los favoritos de la empresa autenticada. ✅ **Auth requerida** (solo `company`).

> Sin body.

---

### DELETE `/catalogo/favoritos/{estudiante_user_id}`
Elimina un favorito. ✅ **Auth requerida** (solo `company`).

> Prerrequisito: el favorito debe existir.  
> Ejemplo: `/api/catalogo/favoritos/1`

---

## 6. NOTIFICACIONES — ms-notificaciones (Express · MongoDB · :8005)

---

### POST `/notificaciones`
Crea una notificación. **No requiere autenticación** (es llamado internamente por otros microservicios).

```json
{
    "destinatario_user_id": 1,
    "tipo": "general",
    "titulo": "Bienvenido a TalentBridge",
    "mensaje": "Tu cuenta ha sido creada exitosamente.",
    "metadata": {}
}
```

> `tipo` acepta: `postulacion_estado` · `nueva_convocatoria` · `perfil_visitado` · `acuerdo_respuesta` · `grupo_seleccionado` · `convocatoria_por_cerrar` · `certificacion_registrada` · `general`

---

### GET `/notificaciones`
Lista las notificaciones del usuario autenticado. ✅ **Auth requerida.**

> Sin body. Filtro disponible:
> - `/notificaciones?no_leidas=true`

---

### GET `/notificaciones/no-leidas/count`
Cuenta las notificaciones no leídas. ✅ **Auth requerida.**

> Sin body.

**Respuesta exitosa (200):**
```json
{ "success": true, "total": 3 }
```

---

### PATCH `/notificaciones/{_id}/leer`
Marca una notificación como leída. ✅ **Auth requerida.**

> `{_id}` es el `_id` de la notificación en MongoDB.  
> Prerrequisito: la notificación debe existir y pertenecer al usuario autenticado.  
> Sin body. Ejemplo: `/api/notificaciones/69cc8643c558312e4f32a99b/leer`

---

### PATCH `/notificaciones/marcar-todas`
Marca todas las notificaciones como leídas. ✅ **Auth requerida.**

> Sin body.

---

### GET `/notificaciones/preferencias`
Obtiene las preferencias de notificación. ✅ **Auth requerida.**

> Sin body. Si no existen preferencias para el usuario, se crean automáticamente con valores por defecto.

---

### PUT `/notificaciones/preferencias`
Actualiza las preferencias de notificación. ✅ **Auth requerida.**

```json
{
    "email_activo": false,
    "push_activo": true,
    "tipos_activos": [
        "postulacion_estado",
        "nueva_convocatoria",
        "acuerdo_respuesta"
    ]
}
```

---

## Resumen de endpoints

| Microservicio | Total | Públicos | Protegidos |
|---|---|---|---|
| ms-gateway (Auth) | 6 | 4 | 2 |
| ms-usuarios | 12 | 0 | 12 |
| ms-convocatorias | 10 | 2 | 8 |
| ms-formacion | 9 | 2 | 7 |
| ms-matching | 7 | 0 | 7 |
| ms-notificaciones | 8 | 1 | 7 |
| **Total** | **52** | **9** | **43** |
