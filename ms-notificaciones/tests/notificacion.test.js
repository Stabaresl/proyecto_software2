const request    = require('supertest');
const mongoose   = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');

let app;
let mongoServer;

beforeAll(async () => {
    mongoServer = await MongoMemoryServer.create();
    const uri   = mongoServer.getUri();
    await mongoose.connect(uri);

    process.env.MONGO_URI = uri;
    app = require('../src/app');
}, 30000);

afterAll(async () => {
    await mongoose.disconnect();
    await mongoServer.stop();
});

afterEach(async () => {
    const collections = mongoose.connection.collections;
    for (const key in collections) {
        await collections[key].deleteMany({});
    }
});

const authHeaders = (userId = 1) => ({
    'X-User-Id':   String(userId),
    'X-User-Role': 'student',
});

describe('Notificaciones', () => {
    test('Crear notificación exitosa', async () => {
        const res = await request(app)
            .post('/api/notificaciones')
            .send({
                destinatario_user_id: 1,
                tipo:    'general',
                titulo:  'Prueba',
                mensaje: 'Mensaje de prueba',
            });
        expect(res.status).toBe(201);
        expect(res.body.success).toBe(true);
    }, 10000);

    test('Crear notificación falla sin campos requeridos', async () => {
        const res = await request(app)
            .post('/api/notificaciones')
            .send({});
        expect(res.status).toBe(422);
    }, 10000);

    test('Listar notificaciones requiere auth', async () => {
        const res = await request(app).get('/api/notificaciones');
        expect(res.status).toBe(401);
    }, 10000);

    test('Listar notificaciones con auth', async () => {
        const res = await request(app)
            .get('/api/notificaciones')
            .set(authHeaders());
        expect(res.status).toBe(200);
        expect(res.body.success).toBe(true);
    }, 10000);

    test('Contar no leídas con auth', async () => {
        const res = await request(app)
            .get('/api/notificaciones/no-leidas/count')
            .set(authHeaders());
        expect(res.status).toBe(200);
        expect(res.body).toHaveProperty('total');
    }, 10000);

    test('Ver preferencias con auth', async () => {
        const res = await request(app)
            .get('/api/notificaciones/preferencias')
            .set(authHeaders());
        expect(res.status).toBe(200);
        expect(res.body.success).toBe(true);
    }, 10000);

    test('Actualizar preferencias', async () => {
        const res = await request(app)
            .put('/api/notificaciones/preferencias')
            .set(authHeaders())
            .send({ email_activo: false, push_activo: true });
        expect(res.status).toBe(200);
        expect(res.body.success).toBe(true);
    }, 10000);

    test('Marcar todas como leídas', async () => {
        const res = await request(app)
            .patch('/api/notificaciones/marcar-todas')
            .set(authHeaders());
        expect(res.status).toBe(200);
        expect(res.body.success).toBe(true);
    }, 10000);
});