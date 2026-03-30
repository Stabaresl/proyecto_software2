from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas.formacion_schema import FormacionSchema, FormacionUpdateSchema
from app.services import formacion_service
from app.utils.auth import token_required, role_required

formacion_bp = Blueprint('formacion', __name__)

@formacion_bp.route('/', methods=['GET'])
def listar():
    filtros = request.args.to_dict()
    data = formacion_service.listar_formaciones(filtros)
    return jsonify({'success': True, 'data': data})


@formacion_bp.route('/<formacion_id>', methods=['GET'])
def obtener(formacion_id):
    doc = formacion_service.obtener_formacion(formacion_id)
    if not doc:
        return jsonify({'success': False, 'message': 'Programa no encontrado.'}), 404
    return jsonify({'success': True, 'data': doc})


@formacion_bp.route('/', methods=['POST'])
@token_required
@role_required('university')
def crear():
    schema = FormacionSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({'success': False, 'errors': e.messages}), 422

    doc = formacion_service.crear_formacion(data, int(request.auth_user_id))
    return jsonify({'success': True, 'message': 'Programa creado.', 'data': doc}), 201


@formacion_bp.route('/<formacion_id>', methods=['PUT'])
@token_required
@role_required('university')
def actualizar(formacion_id):
    schema = FormacionUpdateSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({'success': False, 'errors': e.messages}), 422

    doc, error = formacion_service.actualizar_formacion(formacion_id, data, int(request.auth_user_id))
    if error:
        return jsonify({'success': False, 'message': error}), 400
    return jsonify({'success': True, 'message': 'Programa actualizado.', 'data': doc})


@formacion_bp.route('/certificaciones', methods=['POST'])
@token_required
@role_required('university')
def registrar_certificacion():
    body = request.get_json()
    if not body.get('estudiante_user_id') or not body.get('formacion_id') or not body.get('nombre_certificacion'):
        return jsonify({'success': False, 'message': 'Faltan campos requeridos.'}), 422

    doc = formacion_service.registrar_certificacion(body)
    return jsonify({'success': True, 'message': 'Certificación registrada.', 'data': doc}), 201


@formacion_bp.route('/certificaciones/<int:estudiante_user_id>', methods=['GET'])
@token_required
def listar_certificaciones(estudiante_user_id):
    data = formacion_service.listar_certificaciones_estudiante(estudiante_user_id)
    return jsonify({'success': True, 'data': data})