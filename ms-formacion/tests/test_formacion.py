import pytest
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/tb_formacion_test'
    with app.test_client() as client:
        yield client


def auth_headers(role='university', user_id=3):
    import jwt
    token = jwt.encode(
        {'sub': user_id, 'role': role},
        key='secret',
        algorithm='HS256'
    )
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

class TestFormaciones:
    def test_listar_formaciones(self, client):
        response = client.get('/api/formaciones/')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

    def test_crear_formacion_exitosa(self, client):
        payload = {
            'titulo': 'Bootcamp de Prueba',
            'descripcion': 'Descripción de prueba',
            'tipo': 'bootcamp',
            'modalidad': 'virtual',
            'duracion_semanas': 8,
            'universidad_user_id': 3,
        }
        response = client.post(
            '/api/formaciones/',
            data=json.dumps(payload),
            headers=auth_headers(),
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert '_id' in data['data']

    def test_crear_formacion_falla_sin_auth(self, client):
        payload = {
            'titulo': 'Test',
            'descripcion': 'Test',
            'tipo': 'bootcamp',
            'modalidad': 'virtual',
            'duracion_semanas': 8,
            'universidad_user_id': 3,
        }
        response = client.post('/api/formaciones/', data=json.dumps(payload),
                               content_type='application/json')
        assert response.status_code == 401

    def test_crear_formacion_falla_role_incorrecto(self, client):
        payload = {
            'titulo': 'Test',
            'descripcion': 'Test',
            'tipo': 'bootcamp',
            'modalidad': 'virtual',
            'duracion_semanas': 8,
            'universidad_user_id': 3,
        }
        response = client.post(
            '/api/formaciones/',
            data=json.dumps(payload),
            headers=auth_headers(role='student'),
        )
        assert response.status_code == 403

    def test_crear_formacion_falla_campos_requeridos(self, client):
        response = client.post(
            '/api/formaciones/',
            data=json.dumps({}),
            headers=auth_headers(),
        )
        assert response.status_code == 422

    def test_ver_formacion_no_existente(self, client):
        response = client.get('/api/formaciones/000000000000000000000000')
        assert response.status_code == 404


class TestAcuerdos:
    def test_solicitar_acuerdo_exitoso(self, client):
        payload = {
            'universidad_user_id': 3,
            'titulo': 'Acuerdo de Prueba',
            'descripcion': 'Descripción del acuerdo',
            'duracion_semanas': 10,
            'perfil_estudiante': 'Ingeniería de Sistemas',
        }
        response = client.post(
            '/api/acuerdos/',
            data=json.dumps(payload),
            headers=auth_headers(role='company', user_id=2),
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True

    def test_solicitar_acuerdo_falla_role_incorrecto(self, client):
        payload = {
            'universidad_user_id': 3,
            'titulo': 'Test',
            'descripcion': 'Test',
            'duracion_semanas': 10,
            'perfil_estudiante': 'Test',
        }
        response = client.post(
            '/api/acuerdos/',
            data=json.dumps(payload),
            headers=auth_headers(role='student'),
        )
        assert response.status_code == 403

    def test_listar_solicitudes_empresa(self, client):
        response = client.get(
            '/api/acuerdos/mis-solicitudes',
            headers=auth_headers(role='company', user_id=2),
        )
        assert response.status_code == 200

    def test_listar_acuerdos_recibidos_universidad(self, client):
        response = client.get(
            '/api/acuerdos/recibidos',
            headers=auth_headers(role='university', user_id=3),
        )
        assert response.status_code == 200