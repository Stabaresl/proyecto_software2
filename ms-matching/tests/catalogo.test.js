const request = require('supertest');
const app     = require('../src/app');

const authHeaders = (role = 'company', userId = 2) => ({
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIyIiwicm9sZSI6ImNvbXBhbnkifQ.test',
    'X-User-Id':   String(userId),
    'X-User-Role': role,
});

describe('Catálogo', () => {
    test('Listar estudiantes requiere auth', async () => {
        const res = await request(app).get('/api/catalogo/estudiantes');
        expect(res.status).toBe(401);
    });

    test('Listar estudiantes con auth válida', async () => {
        const res = await request(app)
            .get('/api/catalogo/estudiantes')
            .set(authHeaders());
        expect(res.status).toBe(200);
        expect(res.body.success).toBe(true);
    });

    test('Crear o actualizar perfil estudiante', async () => {
        const res = await request(app)
            .post('/api/catalogo/perfil')
            .set(authHeaders('student', 1))
            .send({
                universidad:    'Universidad Nacional',
                carrera:        'Ingeniería de Sistemas',
                semestre:       7,
                habilidades:    ['Python', 'React'],
                disponibilidad: 'part_time',
                promedio:       4.2,
                ubicacion:      'Bogotá',
            });
        expect(res.status).toBe(201);
        expect(res.body.success).toBe(true);
    });

    test('Agregar favorito requiere role company', async () => {
        const res = await request(app)
            .post('/api/catalogo/favoritos')
            .set(authHeaders('student', 1))
            .send({ estudiante_user_id: 1 });
        expect(res.status).toBe(403);
    });

    test('Agregar favorito falla sin estudiante_user_id', async () => {
        const res = await request(app)
            .post('/api/catalogo/favoritos')
            .set(authHeaders())
            .send({});
        expect(res.status).toBe(422);
    });

    test('Listar favoritos como empresa', async () => {
        const res = await request(app)
            .get('/api/catalogo/favoritos')
            .set(authHeaders());
        expect(res.status).toBe(200);
        expect(res.body.success).toBe(true);
    });
});

describe('Matching', () => {
    test('Sugerir candidatos falla sin body', async () => {
        const res = await request(app)
            .post('/api/matching/sugerir')
            .set(authHeaders())
            .send({});
        expect(res.status).toBe(422);
    });

    test('Sugerir candidatos exitoso', async () => {
        const res = await request(app)
            .post('/api/matching/sugerir')
            .set(authHeaders())
            .send({
                habilidades:    ['Python'],
                disponibilidad: 'part_time',
                semestre_minimo: 5,
            });
        expect(res.status).toBe(200);
        expect(res.body.success).toBe(true);
    });

    test('Sugerir candidatos falla role student', async () => {
        const res = await request(app)
            .post('/api/matching/sugerir')
            .set(authHeaders('student', 1))
            .send({ habilidades: ['Python'] });
        expect(res.status).toBe(403);
    });
});