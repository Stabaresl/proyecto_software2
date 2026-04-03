import pytest
from django.test import TestCase, Client
import json


class TestUniversidades(TestCase):
    def setUp(self):
        self.client = Client()

    def test_crear_universidad_exitosa(self):
        response = self.client.post(
            '/api/universities/',
            data=json.dumps({
                'name': 'Universidad de Prueba',
                'programs': ['Ingeniería'],
                'research_groups': ['Grupo IA'],
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data['success'])

    def test_crear_universidad_falla_sin_nombre(self):
        response = self.client.post(
            '/api/universities/',
            data=json.dumps({}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 422)

    def test_listar_universidades(self):
        response = self.client.get('/api/universities/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)

    def test_ver_universidad_no_existente(self):
        response = self.client.get('/api/universities/9999/')
        self.assertEqual(response.status_code, 404)


class TestEstudiantes(TestCase):
    def setUp(self):
        self.client = Client()
        # Crear universidad para asociar
        res = self.client.post(
            '/api/universities/',
            data=json.dumps({'name': 'Universidad Test'}),
            content_type='application/json',
        )
        self.universidad_id = res.json()['data']['id']

    def test_crear_perfil_estudiante(self):
        response = self.client.post(
            '/api/profiles/',
            data=json.dumps({
                'role': 'student',
                'gateway_user_id': 1,
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'availability': 'part_time',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()['success'])

    def test_crear_perfil_falla_role_invalido(self):
        response = self.client.post(
            '/api/profiles/',
            data=json.dumps({'role': 'admin', 'gateway_user_id': 99}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_crear_perfil_falla_sin_role(self):
        response = self.client.post(
            '/api/profiles/',
            data=json.dumps({'gateway_user_id': 99}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_listar_estudiantes(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_ver_estudiante_no_existente(self):
        response = self.client.get('/api/students/9999/')
        self.assertEqual(response.status_code, 404)


class TestEmpresas(TestCase):
    def setUp(self):
        self.client = Client()

    def test_crear_perfil_empresa(self):
        response = self.client.post(
            '/api/profiles/',
            data=json.dumps({
                'role': 'company',
                'gateway_user_id': 2,
                'name': 'Empresa Test SAS',
                'sector': 'Tecnología',
                'size': 'small',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()['success'])

    def test_listar_empresas(self):
        response = self.client.get('/api/companies/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_ver_empresa_no_existente(self):
        response = self.client.get('/api/companies/9999/')
        self.assertEqual(response.status_code, 404)


class TestEntidadesGubernamentales(TestCase):
    def setUp(self):
        self.client = Client()

    def test_crear_perfil_estado(self):
        response = self.client.post(
            '/api/profiles/',
            data=json.dumps({
                'role': 'state',
                'gateway_user_id': 4,
                'name': 'Minciencias',
                'description': 'Ministerio de Ciencia',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()['success'])

    def test_listar_entidades(self):
        response = self.client.get('/api/government-entities/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])